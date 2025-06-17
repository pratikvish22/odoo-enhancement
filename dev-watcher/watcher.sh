#!/bin/sh
# Source environment variables from env file if it exists
set -e

WATCH_PATH="/mnt/extra-addons"
ODOO_SERVICE="${ODOO_SERVICE:-odoo_15}"

# Wait for docker socket
while [ ! -S /var/run/docker.sock ]; do
  echo "Waiting for Docker socket..."
  sleep 1
done

echo "Watching $WATCH_PATH for changes..."

find "$WATCH_PATH" -type f | \
  entr -n -r sh -c "echo 'Change detected, restarting Odoo '; docker restart $ODOO_SERVICE"
