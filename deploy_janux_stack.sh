#!/bin/bash

# 🚀 Script to Rebuild & Deploy JANUX Authentication Gateway on Docker Swarm
# Author: FOX Techniques

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

# Wait for services to start
sleep 5

# Check if the service is running
if docker service ls | grep -w "${STACK_NAME}_${SERVICE_NAME}" > /dev/null 2>&1; then
    echo "✅ Service '${STACK_NAME}_${SERVICE_NAME}' is running."
else
    echo "❌ ERROR: Service '${STACK_NAME}_${SERVICE_NAME}' failed to start. Check logs."
    exit 1
fi

# Display running services
echo "📋 Running services:"
docker service ls

# Test the health endpoint
echo "🩺 Checking service health..."
curl -s http://localhost:8000/health && echo "✅ API is reachable!" || echo "❌ ERROR: API is NOT reachable!"

echo "🎉 Deployment complete!"
