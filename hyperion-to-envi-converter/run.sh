#!/bin/bash
APP_DIR=$(dirname "$(realpath "$0")")

# Load env vars
LOCAL_ENV_PATH="$APP_DIR/env"
REQUIREMENTS_SPEC_PATH="$APP_DIR/requirements.in"
REQUIREMENTS_PATH="$APP_DIR/requirements.txt"
ACTIVATE_PATH="$LOCAL_ENV_PATH/bin/activate"

NEEDS_INSTALL=0
NEEDS_RECOMPILE=0
if [[ "$1" == "--upgrade" ]]; then
    NEEDS_INSTALL=1
    shift
elif [[ "$1" == "--recompile" ]]; then
    NEEDS_INSTALL=1
    NEEDS_RECOMPILE=1
    shift
elif [[ ! -f "$ACTIVATE_PATH" ]]; then
    NEEDS_INSTALL=1
fi


# Initialize virtual environment
if (( NEEDS_INSTALL )); then
    echo "Installing..."
    rm -rf "$LOCAL_ENV_PATH"
    echo "Creating a virtual environment 'env' in $APP_DIR..."
    python3.10 -m venv "$LOCAL_ENV_PATH"
fi

# Activate the virtual environment
source "$LOCAL_ENV_PATH/bin/activate"

# Update packages
if (( NEEDS_INSTALL )); then
    echo "Initialized $APP_DIR"
    if (( NEEDS_RECOMPILE )); then
        pip3.10 install pip-tools
        pip-compile "$REQUIREMENTS_SPEC_PATH" -o "$REQUIREMENTS_PATH"
    fi
    pip3.10 install -r "$APP_DIR/requirements.txt" --quiet
fi

# Run the python script
python3.10 "$APP_DIR/main.py" "$@"