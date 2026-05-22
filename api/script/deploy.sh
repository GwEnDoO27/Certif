#!/usr/bin/env bash
# scripts/deploy.sh
set -euo pipefail

# Configuration
IMAGE_NAME="api-achat-facture-mb"
TAG="${1:-latest}"
NAMESPACE="${2:-default}"

# Se placer à la racine du projet (le Dockerfile est ici)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

echo "Building Docker image ${IMAGE_NAME}:${TAG} from ${ROOT_DIR} ..."

# Build Docker image
docker build -t "${IMAGE_NAME}:${TAG}" .

# Tag for k3s registry (local registry)
docker tag "${IMAGE_NAME}:${TAG}" "localhost:5000/${IMAGE_NAME}:${TAG}"

# Push to registry
docker push "localhost:5000/${IMAGE_NAME}:${TAG}"

# Restart deployment
sudo kubectl rollout restart "deployment/${IMAGE_NAME}" -n "${NAMESPACE}"

echo "Deployment completed!"
