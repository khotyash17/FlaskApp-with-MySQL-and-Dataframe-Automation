#!/bin/sh
set -e

echo "🚀 Starting secure Excel export job..."

# Load environment variables
if [ -f /app/.env ]; then
    export $(grep -v '^#' /app/.env | xargs)
else
    echo "⚠️ .env file not found!"
fi


touch /var/log/cron.log

/usr/local/bin/python3 /app/send_mail.py

echo "✅ Job finished."
