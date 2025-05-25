#!/bin/bash
cd /home/pi/mcp-assistant
source .venv/bin/activate
python garmin_daily_sync.py >> logs/sync.log 2>&1
