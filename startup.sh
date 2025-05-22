#!/bin/bash

# Navigate to the directory where the script is located
# This ensures that relative paths for FLASK_APP and requirements.txt work correctly
cd "$(dirname "$0")"

echo "Starting Meeting Summary Bot..."

# Install dependencies
echo "Installing dependencies from requirements.txt..."
if pip install --no-cache-dir -r requirements.txt; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies. Please check requirements.txt and pip configuration. Exiting."
    exit 1
fi

# Set Flask application environment variable
export FLASK_APP=app.py

# The FLASK_ENV variable can be 'development' or 'production'.
# 'production' is the default if not set. For development, 'flask run' enables the debugger.
# For this startup script, we aim for a production-like launch, so not setting FLASK_ENV or setting to production is fine.
# export FLASK_ENV=production 

echo "Starting Flask application..."

# Attempt to use Gunicorn if available (common for production Python web apps)
# Otherwise, fall back to Flask's built-in development server.
# The application must run on port 9000.
if command -v gunicorn &> /dev/null
then
    echo "Running with Gunicorn on port 9000."
    # Example: gunicorn --workers 4 --bind 0.0.0.0:9000 app:app
    # For simplicity, using 1 worker here. Adjust as needed.
    gunicorn --bind 0.0.0.0:9000 app:app
else
    echo "Gunicorn not found. Running with Flask development server on port 9000."
    # The `flask run` command respects FLASK_APP and uses its own mechanisms for host/port.
    # `debug=False` in app.py's app.run() is for `python app.py` execution.
    # `flask run` defaults to production mode (debug off) unless FLASK_DEBUG=1 or FLASK_ENV=development.
    python -m flask run --host=0.0.0.0 --port=9000
fi

# The script might exit if gunicorn/flask run is backgrounded. 
# For foreground execution (typical for startup scripts in containers/services), this is fine.
echo "Meeting Summary Bot should be accessible. If run in foreground, press Ctrl+C to stop."
