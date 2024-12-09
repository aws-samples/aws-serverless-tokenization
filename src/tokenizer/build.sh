#!/bin/bash

# Define the Docker image name
IMAGE_NAME="lambda-python-layer"

# Create and switch to a new builder instance
echo "Creating and switching to a new builder instance..."
docker buildx create --name mybuilder --use

# Inspect the builder instance to ensure it's configured
echo "Inspecting the builder instance to ensure it's configured..."
docker buildx inspect --bootstrap

# Build the Docker image and load it locally
echo "Building the Docker image for the specified platform (linux/arm64) and loading it locally..."
docker buildx build --platform linux/arm64 -t ${IMAGE_NAME} --load .

# Remove the builder instance after the build
echo "Removing the builder instance after the build..."
docker buildx rm mybuilder
