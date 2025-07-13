#!/bin/bash

# Go to your project directory
cd ~/portfolio-site || exit

# Pull latest changes from GitHub
git fetch && git reset origin/main --hard

# Activate virtual environment and install any new requirements
source venv/bin/activate
pip install -r requirements.txt

# Restart the systemd service
sudo systemctl restart myportfolio
