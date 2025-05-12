#!/bin/bash

# Script to Rebuild & Deploy JANUX Authentication Gateway on Docker Swarm
# Author: FOX Techniques <ali.nabbi@fox-techniques.com>

# Constants
STACK_NAME="janux-stack"
SERVICE_NAME="janux-auth-gateway"
NETWORK_NAME="janux-network"
IMAGE_NAME="janux-auth-gateway"
COMPOSE_FILE=${1:-"docker-compose.mongo.yml"}  # default, or pass as arg

# Retry config
MAX_RETRIES=10
RETRY_INTERVAL=3
MAX_HEALTH_RETRIES=5

# Check Docker
if ! command -v docker > /dev/null; then
  echo "❌ ERROR: Docker is not installed or not in PATH."
  exit 1
fi

# Check Docker daemon
if ! docker info > /dev/null 2>&1; then
  echo "❌ ERROR: Docker daemon is not running or permission denied."
  exit 1
fi

echo "🚀 Deploying ${STACK_NAME} using ${COMPOSE_FILE}..."

# Ensure Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
  echo "⚠️ Docker Swarm is not initialized. Initializing..."
  if docker swarm init > /dev/null 2>&1; then
    echo "✅ Docker Swarm initialized."
  else
    echo "❌ ERROR: Failed to initialize Docker Swarm."
    exit 1
  fi
fi

# Remove old stack
echo "🔄 Removing existing stack: ${STACK_NAME}"
docker stack rm "${STACK_NAME}" > /dev/null 2>&1
sleep 5

# Ensure overlay network
if ! docker network ls | grep -w "${NETWORK_NAME}" > /dev/null 2>&1; then
  echo "🔄 Creating overlay network: ${NETWORK_NAME}"
  if docker network create --driver overlay --attachable "${NETWORK_NAME}"; then
    echo "✔️ Network created: ${NETWORK_NAME}"
  else
    echo "❌ ERROR: Failed to create network '${NETWORK_NAME}'"
    exit 1
  fi
else
  echo "✅ Network '${NETWORK_NAME}' already exists."
fi

# Build image
echo "🔨 Building image: ${IMAGE_NAME}"
if docker build -t "${IMAGE_NAME}" .; then
  echo "✔️ Image '${IMAGE_NAME}' built successfully."
else
  echo "❌ ERROR: Failed to build Docker image '${IMAGE_NAME}'."
  exit 1
fi

# Deploy
echo "🚢 Deploying stack using ${COMPOSE_FILE}"
docker stack deploy -c "${COMPOSE_FILE}" "${STACK_NAME}"

# Wait for service to stabilize
echo "⏳ Waiting for '${STACK_NAME}_${SERVICE_NAME}' to become ready..."
TRIES=0
while ! docker service ls | grep -w "${STACK_NAME}_${SERVICE_NAME}" | grep -w "1/1" > /dev/null 2>&1; do
  TRIES=$((TRIES + 1))
  if [ "$TRIES" -ge "$MAX_RETRIES" ]; then
    echo "❌ ERROR: Service did not become ready after $((MAX_RETRIES * RETRY_INTERVAL)) seconds."
    exit 1
  fi
  echo "⏳ Retry ${TRIES}/${MAX_RETRIES}... waiting ${RETRY_INTERVAL}s"
  sleep "$RETRY_INTERVAL"
done

echo "✅ Service '${STACK_NAME}_${SERVICE_NAME}' is running."

# Health check
echo "🩺 Checking service health at http://localhost:8000/health..."
HEALTH_TRIES=0
while ! curl -s http://localhost:8000/health > /dev/null; do
  HEALTH_TRIES=$((HEALTH_TRIES + 1))
  if [ "$HEALTH_TRIES" -ge "$MAX_HEALTH_RETRIES" ]; then
    echo "❌ ERROR: API not reachable after $((MAX_HEALTH_RETRIES * RETRY_INTERVAL)) seconds."
    exit 1
  fi
  echo "🔄 Health retry ${HEALTH_TRIES}/${MAX_HEALTH_RETRIES}..."
  sleep "$RETRY_INTERVAL"
done

echo "✅ API is reachable!"
echo "📋 Active services:"
docker service ls

echo "🎉 Deployment of '${STACK_NAME}' complete!"
