#!/bin/bash

echo "Posting new timeline post..."
curl -X POST http://127.0.0.1:5000/api/timeline_post \
  -d "name=Test User" \
  -d "email=testuser@example.com" \
  -d "content=This is a test timeline post!" \
  --silent --show-error --fail

echo -e "\n\nGetting all timeline posts..."
curl http://127.0.0.1:5000/api/timeline_post \
  --silent --show-error --fail
