#!/usr/bin/bash

systemctl stop myportfolio
cd ~/portfolio-site
git fetch
git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl restart myportfolio
