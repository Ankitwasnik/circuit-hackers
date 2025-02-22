#!/bin/bash

SCRIPT_DIR=$(dirname "$0")

# Define the virtual environment directory
VIRTUALENV=".venv"

# Check if the virtual environment already exists
if [ ! -d "$VIRTUALENV" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv "$VIRTUALENV"
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source "$VIRTUALENV/bin/activate"

# Install the required packages
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate