#!/bin/sh
set -e

# Ensure log file exists
touch /var/log/cron.log

echo "🚀 Starting secure Excel export job..."

# Run the Python script
python3 /app/send_mail.py

echo "✅ Job finished."
