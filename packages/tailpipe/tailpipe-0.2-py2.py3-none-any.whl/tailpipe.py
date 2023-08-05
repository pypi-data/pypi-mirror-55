"""A simple command-line tool for reading the output of all jobs
run in a Gitlab pipeline for the current git commit"""
__version__ = '0.2'
import sys
import time
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import click
from pypager.source import GeneratorSource
from pypager.pager import Pager
from prompt_toolkit import ANSI
from prompt_toolkit.formatted_text import to_formatted_text
from gitlab import Gitlab


def main():
    setup_output = []
    setup_output.append('Parsing project path from git remote url')
    click.echo(setup_output[-1])
    try:
        p = Popen(['git', 'remote', '-v'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        lines = output.decode('utf-8').splitlines()
        _, url, *_ = lines[0].split()
        project_path = urlparse(url).path[1:].replace('.git', '')
    except Exception as e:
        click.echo('Error getting git remotes.  Is this a git repository with a Gitlab remote configured?')
        sys.exit(1)

    try:
        setup_output.append('Retrieving commit ID of HEAD')
        click.echo(setup_output[-1])
        p = Popen(['git', 'rev-parse', 'HEAD'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        lines = output.decode('utf-8').splitlines()
        commit_id = lines[0]
    except Exception as e:
        click.echo('Error getting git commit ID.  Is this a git repository with a Gitlab remote configured?')
        sys.exit(1)

    setup_output.append('Authenticating with Gitlab API')
    click.echo(setup_output[-1])
    gl = Gitlab.from_config()

    try:
        gl.auth()
        setup_output.append(f'Searching for projects with path {project_path}')
        click.echo(setup_output[-1])
        project = gl.projects.get(project_path)

        setup_output.append(f'Searching for commit ID {commit_id}')
        click.echo(setup_output[-1])
        commit = project.commits.get(commit_id)

        last_pipeline = commit.last_pipeline
        if not last_pipeline:
            click.echo(f'No pipeline has run for commit ID {commit_id}')
            sys.exit(1)
        pipeline_id = last_pipeline['id']
        setup_output.append(f'Retrieving pipeline ID {pipeline_id}')
        click.echo(setup_output[-1])
        pipeline = project.pipelines.get(pipeline_id)
        pipeline_status = pipeline.attributes['status']
        pipeline_started = pipeline.attributes['started_at']
        pipeline_ref = pipeline.attributes['ref']
        setup_output.append(f'Pipeline status: "{pipeline_status}", ref: "{pipeline_ref}", started: {pipeline_started}')
        click.echo(setup_output[-1])

        jobs_meta = pipeline.jobs.list()
        setup_output.append(f'Found {len(jobs_meta)} jobs for pipeline. Tailing job logs...')
        click.echo(setup_output[-1])
        time.sleep(0.8)

        seen = {}
        output = []
        def tail():
            yield to_formatted_text('Pipeline Tail Setup\n', style='fg:ansiwhite bold')
            for output in setup_output:
                yield to_formatted_text(output + '\n')
            while jobs_meta:
                job_meta = jobs_meta.pop(0)
                job_id = job_meta.attributes['id']
                job = project.jobs.get(job_id)
                job_status = job.attributes['status']
                job_stage = job.attributes['stage']
                job_name = job.attributes['name']
                if not seen.get(job_id):
                    yield to_formatted_text(f'\nTailing job: {job_id}, pipeline: {pipeline_id}, stage: {job_stage}, name: {job_name}\n', style='fg:ansiwhite bold')
                    # Reset previous job output
                    previous_job_output = ''
                    seen[job_id] = job_status
                    yield to_formatted_text(f'Job status: "{job.attributes["status"]}"\n')
                elif job_status != seen[job_id]:
                    seen[job_id] = job_status
                    if previous_job_output == '':
                        yield to_formatted_text(f'Job status: "{job.attributes["status"]}"\n')

                if job_status == 'running':
                    # Put job back in queue
                    jobs_meta.insert(0, job_meta)
                if job_status in ('running', 'success'):
                    # Get latest job_output
                    job_output = job.trace().decode('utf-8')
                    # Set current output to latest job_output without previous, set previous to latest job_output
                    current_output, previous_job_output = job_output.replace(previous_job_output, ''), job_output
                    if current_output.strip():
                        yield ANSI('\n'.join(current_output.splitlines()) + '\n')._formatted_text
                    # Slow down repeated requests
                    time.sleep(2)
                elif job_status == 'failed':
                    # Get latest job_output
                    job_output = job.trace().decode('utf-8')
                    # Set current output to latest job_output without previous, set previous to latest job_output
                    current_output, previous_job_output = job_output.replace(previous_job_output, ''), job_output
                    if current_output.strip():
                        yield ANSI('\n'.join(current_output.splitlines()))._formatted_text
                elif job_status in ('pending', 'created'):
                    # Put job back in queue
                    jobs_meta.insert(0, job_meta)
                    time.sleep(2)
                elif job_status == 'skipped':
                    yield to_formatted_text('Job skipped.  Likely due to previous job failure.\n')
            yield to_formatted_text('\nPipeline Tail Complete\n', style='fg:ansiwhite bold')
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)

    p = Pager()
    p.add_source(GeneratorSource(tail()))
    p.run()


if __name__ == '__main__':
    main()