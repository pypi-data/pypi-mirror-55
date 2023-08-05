# Tailpipe

A simple, command-line tool for reading Gitlab pipeline job output in the
console.  Just run `tailpipe` when your working directory is within a Git
repository and the tool will determine your remote repository details, the
current commit, and what pipeline jobs are currently running in Gitlab for
that commit.

## Setup

You will need to create a `~/.python-gitlab.cfg` file with a format like this:

```
[global]
default = main
ssl_verify = true
timeout = 5

[main]
url = <GITLAB_URL>
private_token = <PRIVATE_TOKEN>
api_version = 4
```

Replace `<GITLAB_URL>` with your Gitlab URL.  Replace `<PRIVATE_TOKEN>` with a Gitlab private token created with API access.
Follow the instructions [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token)