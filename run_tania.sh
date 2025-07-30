#!/bin/bash

# Tania AI Assistant - Launch Script for Linux/macOS

echo "============================================================"
echo "                    Tania AI Assistant"
echo "============================================================"
echo ""
echo "Starting Tania..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

# Check if the main file exists
if [ ! -f "tania_ai_assistant.py" ]; then
    echo "ERROR: tania_ai_assistant.py not found"
    echo "Please make sure you're in the correct directory"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

# Run Tania
python3 tania_ai_assistant.py

# Check if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred while running Tania."
    echo "Check the error message above for details."
    read -p "Press Enter to continue..."
fi