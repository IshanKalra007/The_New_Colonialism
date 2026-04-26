#!/bin/bash
# Force recalc via LibreOffice convert-to-xlsx
# Usage: ./recalc_force.sh <xlsx_path>

set -e
FILE="$1"
TMPDIR="/tmp/recalc_$$"
rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"

# Convert (which forces full recalc and re-save with cached values)
timeout 240 soffice --headless --calc --convert-to xlsx "$FILE" --outdir "$TMPDIR" > /dev/null 2>&1

# Replace original
FNAME=$(basename "$FILE")
cp -f "$TMPDIR/$FNAME" "$FILE"

# Cleanup
rm -rf "$TMPDIR"

echo "Recalculated: $FILE"
