#!/bin/bash
export PYTHONPATH=$PYTHONPATH:${PWD}

VIRTUALENV=".venv"
source "$VIRTUALENV/bin/activate"
python src/main.py

