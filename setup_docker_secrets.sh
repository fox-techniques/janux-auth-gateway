#!/bin/bash

# Script to Create or Update Docker Secrets for JANUX Authentication Gateway
# Author: FOX Techniques <ali.nabbi@fox-techniques.com>

# Define secrets directory
SECRETS_DIR="./secrets"

# Define secrets list (Docker Secret Name -> Local File)
declare -A SECRETS=(
    ["janux_encryption_key"]="$SECRETS_DIR/janux_encryption_key"
    ["jwt_private_key"]="$SECRETS_DIR/jwt_private_key.pem"
    ["jwt_public_key"]="$SECRETS_DIR/jwt_public_key.pem"
    ["mongo_uri"]="$SECRETS_DIR/mongo_uri"
    ["mongo_admin_email"]="$SECRETS_DIR/mongo_admin_email"
    ["mongo_admin_password"]="$SECRETS_DIR/mongo_admin_password"
    ["mongo_admin_fullname"]="$SECRETS_DIR/mongo_admin_fullname"
    ["mongo_admin_role"]="$SECRETS_DIR/mongo_admin_role"
    ["mongo_user_email"]="$SECRETS_DIR/mongo_user_email"
    ["mongo_user_password"]="$SECRETS_DIR/mongo_user_password"
    ["mongo_user_fullname"]="$SECRETS_DIR/mongo_user_fullname"
    ["mongo_user_role"]="$SECRETS_DIR/mongo_user_role"
)

# Function to create or update a secret
create_or_update_secret() {
    local secret_name=$1
    local secret_file=$2

    if [ ! -f "$secret_file" ]; then
        echo "❌ ERROR: Secret file '$secret_file' does not exist. Skipping..."
        return 1
    fi

    # Check if the secret already exists
    if docker secret ls | grep -w "$secret_name" > /dev/null 2>&1; then
        echo "🔄 Updating secret: $secret_name"
        docker secret rm "$secret_name" > /dev/null 2>&1
        sleep 1  # Short delay to prevent race condition
    else
        echo "✅ Creating secret: $secret_name"
    fi

    # Create the new secret
    docker secret create "$secret_name" "$secret_file" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✔️ Secret '$secret_name' successfully stored in Docker Swarm."
    else
        echo "❌ ERROR: Failed to store secret '$secret_name'. Check Docker logs for details."
        return 1
    fi
}

# Check if Docker Swarm is initialized
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

# Process each secret
echo "🚀 Configuring Docker Secrets..."
for secret_name in "${!SECRETS[@]}"; do
    create_or_update_secret "$secret_name" "${SECRETS[$secret_name]}"
done

# Verify secrets after creation
echo "📋 Verifying stored secrets..."
docker secret ls

echo "🎉 All secrets have been securely configured!"
