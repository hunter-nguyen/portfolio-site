#!/usr/bin/bash

systemctl stop myportfolio
cd ~/portfolio-site
git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
dockercompose -f docker-compose.prod.yml up -d --build