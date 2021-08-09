[![run](https://github.com/Artalus/hg-longpath-test/actions/workflows/run.yml/badge.svg)](https://github.com/Artalus/hg-longpath-test/actions/workflows/run.yml)

## The Point
You usually run Mercurial on windows by simply typing `hg` in your shell/cmd/whatever - which in turn calls the
`hg.exe` binary, compiled by `pip install` or whatever means you used to get Mercurial from Python code.
However this binary is broken (as of Mercurial 5.8.1 and Python 3.9) and will not handle ["Windows Long Paths"](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=cmd).
Even if you enabled them via registry or policy hacks. Even if Python 3 itself supports it!

HOWEVER, if instead of `<hg.exe>` file you invoke `<hg>` file - which is just a Python script used on Linux via `chmod +x ./hg` -
Mercurial WILL ACTUALLY handle long paths in repo correctly. Thus, the invokation turns into something like
`C:/dev/python3/Scripts/python.exe C:/dev/python3/Scripts/hg clone` instead of simple `hg clone`. Which is nonsence, but handy.

...except for `hg update`. For some reason, this bugger might or might not work correctly depending on the environment.

## The Tests

This repo contains Github Actions CI used to run a number of Mercurial commands like `hg add`, `hg update` in a repo
containing files with long paths. The commands are wrapped into PyTest, and tests written in such way that they should
be green no matter how you invoke Mercurial; in case of executable they check that the commands fail miserably,
and in case of script - that they do what they should.

### the ci

GHA runs tests nightly, and I hope one day they become a stable red - this might mean that Mercurial dudes
have changed something, and maybe `hg.exe` now can handle long paths as correctly as the script one.

### the local

See [`.github/workflows/run.yml`](/.github/workflows/run.yml). But basically this:
1. On Linux:
    - `virtualenv venv && . venv/bin/activate`
    - `pip install -e .`
    - `python -m hgl.init --repo repo`
2. Then on Windows or any other test OS:
    - `virtualenv venv ; venv/Scripts/activate.ps1`
    - `pip install -e .[test]`
    - acquire `repo.tar` created by `hgl.init` previously
    - `pytest -n logical` - this will run all tests in parallel (and may still take some time if you are on virtual machine)
