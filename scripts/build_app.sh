#!/usr/bin/env bash

################################################################################
# This script is used to create an executable version of Ollama Bar app for
# Mac OS. It uses the "py2app" module to bundle all dependencies into a single
# executable app.
#
# https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file
################################################################################

# Clean existing build artifacts
rm -rf build/ dist/ ollama_bar.egg-info/

# Perform a clean build of the application
python setup.py py2app -A
