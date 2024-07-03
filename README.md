# Ollama Bar

This is a simple macOS status bar that allows you to start/stop/view [ollama](https://ollama.com/) from the menu bar.

**NOTICE**: This project is not directly affiliated with Ollama and is provided as-is as a convenience for managing the ollama server process from the menu bar.

## Prerequisites

First and foremost, you need to have ollama installed on your machine. You can download it from [ollama.com](https://ollama.com/) of use [homebrew](https://brew.sh/) to install it:

```sh
brew install ollama
```

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
