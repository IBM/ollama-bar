# Ollama Bar

This is a simple macOS status bar that allows you to start/stop/view ollama from the menu bar.

## Prerequisites

This project is based on [rumps](https://github.com/jaredks/rumps) and uses python to build and run the app. It is highly recommended that you use a python version manager like [pyenv](https://github.com/pyenv/pyenv) or [conda](https://github.com/conda-forge/miniforge) to manage your python versions.

In a clean python environment, you can do an editable install of the project and dependencies with pip:

```sh
pip install -e ".[dev]"
```

## Installation

The app can be installed with a single `make install-app` command. This will create a new application bundle in `/Applications/ollama-bar.app`.

## Running the tests

To run all tests, use:

```
make test
```

You can also run [scripts/run_tests.sh](scripts/run_tests.sh) directly with additional `pytest` args to control which tests are run.
