#!/bin/bash

# Script to Create or Update Docker Secrets for JANUX Authentication Gateway
# Author: FOX Techniques <ali.nabbi@fox-techniques.com>

# Exit if no argument is provided
if [ -z "$1" ]; then
  echo "❌ ERROR: Please specify the backend: 'mongo' or 'postgres'"
  echo "Usage: ./setup_docker_secret.sh mongo"
  exit 1
fi

BACKEND="$1"

# Validate backend argument
if [[ "$BACKEND" != "mongo" && "$BACKEND" != "postgres" ]]; then
  echo "❌ ERROR: Invalid backend. Choose 'mongo' or 'postgres'"
  exit 1
fi

# Define secrets directory
SECRETS_DIR="./secrets"

# Define shared secrets
declare -A SHARED_SECRETS=(
  ["janux_encryption_key"]="$SECRETS_DIR/janux_encryption_key"
  ["jwt_private_key"]="$SECRETS_DIR/jwt_private_key.pem"
  ["jwt_public_key"]="$SECRETS_DIR/jwt_public_key.pem"
)

# MongoDB-specific secrets
declare -A MONGO_SECRETS=(
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

# PostgreSQL-specific secrets
declare -A POSTGRES_SECRETS=(
  ["postgres_uri"]="$SECRETS_DIR/postgres_uri"
  ["postgres_admin_username"]="$SECRETS_DIR/postgres_admin_username"
  ["postgres_admin_password"]="$SECRETS_DIR/postgres_admin_password"
  ["postgres_admin_fullname"]="$SECRETS_DIR/postgres_admin_fullname"
  ["postgres_admin_role"]="$SECRETS_DIR/postgres_admin_role"
  ["postgres_user_username"]="$SECRETS_DIR/postgres_user_username"
  ["postgres_user_password"]="$SECRETS_DIR/postgres_user_password"
  ["postgres_user_fullname"]="$SECRETS_DIR/postgres_user_fullname"
  ["postgres_user_role"]="$SECRETS_DIR/postgres_user_role"
)

# Function to create or update a secret
create_or_update_secret() {
  local secret_name=$1
  local secret_file=$2

  if [ ! -f "$secret_file" ]; then
    echo "❌ ERROR: Secret file '$secret_file' does not exist. Skipping..."
    return 1
  fi

  if docker secret ls | grep -w "$secret_name" > /dev/null 2>&1; then
    echo "🔄 Updating secret: $secret_name"
    docker secret rm "$secret_name" > /dev/null 2>&1
    sleep 1
  else
    echo "✅ Creating secret: $secret_name"
  fi

  docker secret create "$secret_name" "$secret_file" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✔️ Secret '$secret_name' successfully stored."
  else
    echo "❌ ERROR: Failed to store secret '$secret_name'."
    return 1
  fi
}

# Ensure Docker Swarm is active
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

# Combine shared and backend-specific secrets
declare -A SELECTED_SECRETS
for k in "${!SHARED_SECRETS[@]}"; do
  SELECTED_SECRETS[$k]="${SHARED_SECRETS[$k]}"
done

if [[ "$BACKEND" == "mongo" ]]; then
  for k in "${!MONGO_SECRETS[@]}"; do
    SELECTED_SECRETS[$k]="${MONGO_SECRETS[$k]}"
  done
elif [[ "$BACKEND" == "postgres" ]]; then
  for k in "${!POSTGRES_SECRETS[@]}"; do
    SELECTED_SECRETS[$k]="${POSTGRES_SECRETS[$k]}"
  done
fi

# Process each secret
echo ""
echo "🚀 Configuring Docker secrets for backend: $BACKEND"
for secret_name in "${!SELECTED_SECRETS[@]}"; do
  create_or_update_secret "$secret_name" "${SELECTED_SECRETS[$secret_name]}"
done

# Summary
echo ""
echo "🔐 Configured secrets:"
for secret_name in "${!SELECTED_SECRETS[@]}"; do
  echo " - $secret_name"
done

echo ""
echo "📋 Docker secret list:"
docker secret ls

echo ""
echo "🎉 All secrets for backend '$BACKEND' have been securely configured!"
