#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running test suite..."
pytest test_dash_app.py -v

if [ $? -eq 0 ]; then
    echo "✓ All tests passed successfully!"
    exit 0
else
    echo "✗ Tests failed!"
    exit 1
fi
