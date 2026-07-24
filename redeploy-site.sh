#!/bin/bash
cd ~/MLH_Portfolio_Website_WK2 && git fetch && git reset origin/HEAD --hard && docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.yml up -d --build

