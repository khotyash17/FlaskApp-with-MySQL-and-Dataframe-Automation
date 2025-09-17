#!/bin/sh
set -e

EXPORT_DIR="/app/exports"
mkdir -p "$EXPORT_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
CSV_FILE="$EXPORT_DIR/students_$TIMESTAMP.csv"
PDF_FILE="$EXPORT_DIR/students_$TIMESTAMP.pdf"
SECURE_PDF="$EXPORT_DIR/students_$TIMESTAMP-secure.pdf"

# Step 1: Export MySQL → CSV
mysql -h db -u root -ppassword --ssl=0 studentsdb -e "SELECT * FROM students;" \
  | sed 's/\t/,/g' > "$CSV_FILE"

echo "✅ CSV created: $CSV_FILE"

# Step 2: Convert CSV → PDF
libreoffice --headless --convert-to pdf "$CSV_FILE" --outdir "$EXPORT_DIR"

echo "✅ PDF created: $PDF_FILE"

# Step 3: Protect PDF with password
qpdf --encrypt "$ZIP_PASS" "$ZIP_PASS" 256 -- "$PDF_FILE" "$SECURE_PDF"

echo "✅ Secure PDF created: $SECURE_PDF"

# Step 4: Send via Gmail
python3 /app/send_mail.py "$SECURE_PDF"
