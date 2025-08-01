#!/bin/bash

echo "Starting the report generator in the background..."
python run_reporter.py &

echo "Starting the web server..."
exec python run_web.py
