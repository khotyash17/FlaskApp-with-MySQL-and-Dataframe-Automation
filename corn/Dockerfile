FROM alpine:latest

# Install MySQL client, bash, cron, and pip
RUN apk add --no-cache mariadb-client bash busybox-suid py3-pip && \
    pip install --no-cache-dir awscli --break-system-packages

WORKDIR /app

COPY export.sh /app/export.sh
RUN chmod +x /app/export.sh

# Create exports folder
RUN mkdir -p /app/exports


# Shared folder for CSVs
VOLUME /app/exports

# Run every 5 minutes (change as needed)
RUN echo "*/3 * * * * /app/export.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root

CMD ["crond", "-f", "-L", "/dev/stdout"]
