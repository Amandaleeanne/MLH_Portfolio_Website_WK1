#!/bin/bash
cd /MLH_Portfolio_website_WK2 && git fetch && git reset origin/HEAD --hard && python -m venv python3-virtualenv && source python3-virtualenv/bin/activate && systemctl daemon-reload && systemctl restart myportfolio












