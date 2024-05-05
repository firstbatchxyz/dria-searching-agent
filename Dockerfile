# Use browserless base image
FROM ghcr.io/browserless/base:latest

# Additional Dockerfile commands here
docker run -p 3000:3000 -e "TOKEN=6R0W53R135510" ghcr.io/browserless/chromium