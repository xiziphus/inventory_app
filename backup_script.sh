#!/bin/bash
# Script to back up the SQLite database

DB_PATH="site.db"
BACKUP_PATH="backups/site_$(date +%F).db"

# Create backups directory if it doesn't exist
mkdir -p backups

# Copy the database file
cp $DB_PATH $BACKUP_PATH

echo "Backup created at $BACKUP_PATH"
