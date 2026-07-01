#!/bin/bash
tmux kill-server && cd /MLH_Portfolio_website_WK2 && git fetch && git reset origin/HEAD --hard && python -m venv python3-virtualenv && source python3-virtualenv/bin/activate && tmux new-session -d -s flask 'flask run; bash'







