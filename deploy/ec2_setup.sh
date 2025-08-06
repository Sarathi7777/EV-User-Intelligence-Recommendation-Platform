#!/bin/bash
sudo apt update
sudo apt install -y python3-pip docker.io
sudo systemctl start docker
sudo systemctl enable docker
cd /home/ubuntu/UV-Cursor
docker build -t ev-backend -f deploy/Dockerfile .
docker run -d -p 8000:8000 --env-file backend/.env ev-backend