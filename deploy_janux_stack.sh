#!/bin/bash

# Script to Rebuild & Deploy JANUX Authentication Gateway on Docker Swarm
# Author: FOX Techniques <ali.nabbi@fox-techniques.com>

# Wait for services to start (retry up to 10 times)
MAX_RETRIES=10
RETRY_INTERVAL=3
TRIES=0

# Define constants
STACK_NAME="janux-stack"
SERVICE_NAME="janux-auth-gateway"
NETWORK_NAME="janux-network"
IMAGE_NAME="janux-auth-gateway"

echo "🚀 Deploying ${STACK_NAME} on Docker Swarm..."

# Ensure Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
    echo "⚠️ Docker Swarm is not initialized. Initializing now..."
    docker swarm init > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Docker Swarm initialized successfully."
    else
        echo "❌ ERROR: Failed to initialize Docker Swarm."
        exit 1
    fi
fi

# Remove old stack if exists
echo "🔄 Removing old stack: ${STACK_NAME}"
docker stack rm "${STACK_NAME}" > /dev/null 2>&1
sleep 5  # Give Docker time to remove old services

# Ensure the overlay network exists
if ! docker network ls | grep -w "${NETWORK_NAME}" > /dev/null 2>&1; then
    echo "🔄 Creating overlay network: ${NETWORK_NAME}"
    docker network create --driver overlay --attachable "${NETWORK_NAME}"
    if [ $? -eq 0 ]; then
        echo "✔️ Network '${NETWORK_NAME}' created successfully."
    else
        echo "❌ ERROR: Failed to create network '${NETWORK_NAME}'."
        exit 1
    fi
else
    echo "✅ Network '${NETWORK_NAME}' already exists."
fi

# Build the latest Docker image
echo "🔨 Building latest image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .
if [ $? -eq 0 ]; then
    echo "✔️ Image '${IMAGE_NAME}' built successfully."
else
    echo "❌ ERROR: Failed to build Docker image '${IMAGE_NAME}'."
    exit 1
fi

# Deploy the updated stack
echo "🚢 Deploying stack: ${STACK_NAME}"
docker stack deploy -c docker-compose.yml "${STACK_NAME}"

# Wait for services to start (retry up to 10 times)
MAX_RETRIES=10
RETRY_INTERVAL=3
TRIES=0

echo "⏳ Waiting for '${STACK_NAME}_${SERVICE_NAME}' to become ready..."
while ! docker service ls | grep -w "${STACK_NAME}_${SERVICE_NAME}" | grep -w "1/1" > /dev/null 2>&1; do
    TRIES=$((TRIES + 1))
    if [ "$TRIES" -ge "$MAX_RETRIES" ]; then
        echo "❌ ERROR: Service '${STACK_NAME}_${SERVICE_NAME}' failed to start after $((MAX_RETRIES * RETRY_INTERVAL)) seconds. Check logs."
        exit 1
    fi
    echo "⏳ Service not ready yet... retrying in ${RETRY_INTERVAL}s (${TRIES}/${MAX_RETRIES})"
    sleep "$RETRY_INTERVAL"
done

echo "✅ Service '${STACK_NAME}_${SERVICE_NAME}' is running."

# Display running services
echo "📋 Running services:"
docker service ls

# Test the health endpoint (retry up to 5 times)
MAX_HEALTH_RETRIES=5
HEALTH_TRIES=0

echo "🩺 Checking service health..."
while ! curl -s http://localhost:8000/health > /dev/null; do
    HEALTH_TRIES=$((HEALTH_TRIES + 1))
    if [ "$HEALTH_TRIES" -ge "$MAX_HEALTH_RETRIES" ]; then
        echo "❌ ERROR: API is NOT reachable after $((MAX_HEALTH_RETRIES * RETRY_INTERVAL)) seconds."
        exit 1
    fi
    echo "🔄 API not ready yet... retrying in ${RETRY_INTERVAL}s (${HEALTH_TRIES}/${MAX_HEALTH_RETRIES})"
    sleep "$RETRY_INTERVAL"
done

echo "✅ API is reachable!"
echo "🎉 Deployment complete!"
