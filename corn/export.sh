#!/bin/sh

# Directory for local CSV storage (matches Docker volume)
EXPORT_DIR="/app/exports"
mkdir -p "$EXPORT_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
CSV_FILE="$EXPORT_DIR/students_$TIMESTAMP.csv"


mysql -h db -u root -ppassword --ssl=0 studentsdb -e "SELECT * FROM students;" \
  | sed 's/\t/,/g' > "$CSV_FILE"


if [ $? -eq 0 ]; then
  echo "[$(date)] ✅ Exported data to $CSV_FILE"
else
  echo "[$(date)] ❌ Failed to export data"
  exit 1
fi


# Upload to S3
aws s3 cp "$CSV_FILE" s3://students-reg-csv/ --region us-east-1

if [ $? -eq 0 ]; then
  echo "[$(date)] Successfully uploaded $CSV_FILE to S3"
else
  echo "[$(date)] Failed to upload $CSV_FILE to S3"
fi
