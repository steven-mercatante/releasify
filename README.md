# Releasify

[![Build Status](https://travis-ci.org/steven-mercatante/releasify.svg?branch=master)](https://travis-ci.org/steven-mercatante/releasify)
[![codecov](https://codecov.io/gh/steven-mercatante/releasify/branch/master/graph/badge.svg)](https://codecov.io/gh/steven-mercatante/releasify)

## What is this?
A tool that lets you quickly and easily create [semver](https://semver.org/) releases to GitHub repositories. It automatically builds the release body by combining all merge commit messages since the last release. Works great on its own, or as part of a continuous integration pipeline.

## How do I use it?
You can invoke this script via CLI or API.

### CLI:
TODO: flesh out instructions
```bash
$ python releasify/cli.py owner_name repo_name minor
```

### API:
...

## Are there tests?
Yep. Run `make test`
