FROM python:3.11-slim

# Install dependencies (LibreOffice for XLS password)
RUN apt-get update && apt-get install -y \
    apt-utils \
    gnupg \
    mariadb-client \
    bash \
    cron \
    libreoffice-core \
    libreoffice-common \
    && rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip install --no-cache-dir yagmail mysql-connector-python pandas openpyxl msoffcrypto-tool

WORKDIR /app

COPY run_cron.sh send_mail.py /app/
RUN chmod +x /app/run_cron.sh


# Exports folder
RUN mkdir -p /app/exports
VOLUME /app/exports
RUN touch /var/log/cron.log
RUN chmod 0666 /var/log/cron.log


# Cron job
RUN echo "*/3 * * * * root /app/run_cron.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron \
    && chmod 0644 /etc/cron.d/my-cron \
    && crontab /etc/cron.d/my-cron

# Keep container alive & show logs
CMD cron && tail -f /var/log/cron.log
