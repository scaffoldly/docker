#!/bin/bash

NAME=$1
IMAGE=$2
ARCH=$3

# Create a temporary directory
mkdir -p /tmp/layer

docker pull $IMAGE
docker create --platform $ARCH --name extract $IMAGE
docker cp extract:/opt /tmp/layer
docker rm -f extract

# Create a zip file
cd /tmp/layer
zip -r /tmp/layer.zip .

# Convert ARCH to x86_64 or arm64
if [ $ARCH == "linux/arm64" ]; then
    LAYER_ARCH="arm64"
else
    LAYER_ARCH="x86_64"
fi

# Publish the Lambda Layer
aws lambda publish-layer-version \
    --layer-name $NAME \
    --zip-file fileb:///tmp/layer.zip \
    --compatible-runtimes provided.al2 provided.al2023 \
    --compatible-architectures $LAYER_ARCH
