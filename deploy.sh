#!/bin/bash

set -eo pipefail

SERVER_USER="root"
SERVER_HOST="calyps.io"
# The live stack. (/lemio on the server is an older copy with different
# settings: don't deploy from it.)
REMOTE_PATH="/root/lemio"
COMPOSE_FILE="docker-compose.prod.yml"
IMAGES="calyps-server client calyps-nginx-proxy"

remote() {
  ssh ${SERVER_USER}@${SERVER_HOST} "$@"
}

# Images are always built here and sent over. Building on the server can run it
# out of memory: the client build alone peaks at over 1GB.
echo "🔨 Building Docker images locally..."
docker compose -f $COMPOSE_FILE build

echo "📁 Creating remote folder..."
remote "mkdir -p ${REMOTE_PATH}/backups"

echo "🚀 Copying compose file to ${SERVER_HOST}..."
scp $COMPOSE_FILE ${SERVER_USER}@${SERVER_HOST}:${REMOTE_PATH}/

# Before loading, because the new images need the space.
echo "🧹 Freeing disk space on ${SERVER_HOST}..."
remote "rm -f ${REMOTE_PATH}/stack.tar && docker image prune -f && df -h /"

echo "📦 Sending Docker images to ${SERVER_HOST}..."
docker save $IMAGES | gzip | remote "gunzip | docker load"

# The new server image runs migrations on start, so keep a copy to roll back to.
# Credentials come from the db container's own environment.
echo "💾 Backing up the database..."
BACKUP="${REMOTE_PATH}/backups/db-$(date +%Y%m%d-%H%M%S).sql.gz"
# (Start the db first if it isn't running, e.g. after a reboot.)
remote "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE up -d --no-build --wait db"
remote "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE exec -T db sh -c 'pg_dump -U \"\$POSTGRES_USER\" \"\$POSTGRES_DB\"' | gzip > ${BACKUP} && ls -lh ${BACKUP}"

echo "🧹 Cleaning up old containers..."
remote "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE down"

# --no-build: if an image is somehow missing, fail rather than build it there.
echo "🚀 Starting up new stack..."
remote "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE up -d --no-build"

# Re-link the existing certificates and reload nginx. Unlike force_renew, this
# doesn't issue new ones, which Let's Encrypt limits to 5 per week per domain.
echo "🔒 Checking certificates..."
remote "sleep 30 && cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE exec -T acme-companion signal_le_service" \
  || echo "⚠️  Could not trigger the certificate check. The companion retries hourly."

echo "🧹 Removing the images this deploy replaced..."
remote "docker image prune -f"

echo "✅ Deployment complete!"
