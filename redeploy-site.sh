#!/bin/bash

# Kill all existing tmux sessions to stop any old Flask processes
tmux kill-server

# Go to your project directory
cd ~/portfolio-site || exit

# Pull latest changes from GitHub
git fetch && git reset origin/main --hard

# Activate virtual environment and install any new requirements
source venv/bin/activate
pip install -r requirements.txt

# Start new tmux session that runs Flask
tmux new-session -d -s flask "cd ~/portfolio-site && source venv/bin/activate && export FLASK_APP=app && flask run --host=0.0.0.0 --port=5000"


