#!/bin/bash

set -e

SERVER_USER="root"
SERVER_HOST="calyps.io"
REMOTE_PATH="/lemio"
COMPOSE_FILE="docker-compose.prod.yml"

echo "🔨 Building Docker images locally..."
docker compose -f $COMPOSE_FILE build

echo "📦 Saving Docker images..."
docker save calyps-server client calyps-nginx-proxy -o stack.tar

echo "📁 Creating remote folder..."
ssh ${SERVER_USER}@${SERVER_HOST} "mkdir -p ${REMOTE_PATH}"

echo "🚀 Copying files to ${SERVER_HOST}..."
scp $COMPOSE_FILE stack.tar ${SERVER_USER}@${SERVER_HOST}:${REMOTE_PATH}/
scp -r ./nginx ./server ./client ${SERVER_USER}@${SERVER_HOST}:${REMOTE_PATH}/

echo "📦 Loading Docker images on server..."
ssh ${SERVER_USER}@${SERVER_HOST} "cd ${REMOTE_PATH} && docker load -i stack.tar"

echo "🧹 Cleaning up old containers..."
ssh ${SERVER_USER}@${SERVER_HOST} "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE down"

echo "🚀 Starting up new stack..."
ssh ${SERVER_USER}@${SERVER_HOST} "cd ${REMOTE_PATH} && docker compose -f $COMPOSE_FILE up -d"

echo "✅ Deployment complete!"
