# Releasify

[![Build Status](https://travis-ci.org/steven-mercatante/releasify.svg?branch=master)](https://travis-ci.org/steven-mercatante/releasify)
[![codecov](https://codecov.io/gh/steven-mercatante/releasify/branch/master/graph/badge.svg)](https://codecov.io/gh/steven-mercatante/releasify)

## What is this?
A tool that lets you quickly and easily create [semver](https://semver.org/) releases for GitHub repositories. It automatically builds the release body for you by combining all of the merge commit messages since the previous release.

This project includes a command line interface and a web API. Use either on its own, or combine it with an existing [CI](https://en.wikipedia.org/wiki/Continuous_integration) pipeline. You can wire this up to a Slackbot to publish releases from chat rooms, or wire it up to Zapier to send clients a changelog email automatically.

## How do I use it?

### CLI:
TODO: flesh out
```bash
$ python releasify/cli.py owner_name repo_name minor
```

### API:
...

## Are there tests?
Yep. Run `make test`
