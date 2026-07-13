#!/bin/bash
cd ~/MLH_Portfolio_Website_WK2 && git fetch && git reset origin/HEAD --hard && source python3-virtualenv/bin/activate && pip install -r requirements.txt && systemctl daemon-reload && systemctl restart myportfolio












