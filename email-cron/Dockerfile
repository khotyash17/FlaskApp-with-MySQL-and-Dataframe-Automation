FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    mariadb-client \
    bash \
    cron \
    libreoffice \
    qpdf \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install yagmail mysql-connector-python python-dotenv

WORKDIR /app

# Copy scripts
COPY run_cron.sh /app/run_cron.sh
COPY send_mail.py /app/send_mail.py

# Give execution rights
RUN chmod +x /app/run_cron.sh

# Setup cron job (runs every 3 mins)
RUN echo "*/3 * * * * /app/run_cron.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/cron \
    && chmod 0644 /etc/cron.d/cron \
    && crontab /etc/cron.d/cron

CMD ["cron", "-f"]
