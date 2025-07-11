#!/bin/bash

curl -X POST http://localhost:5000/api/timeline_post \
    -d "name=John Doe" \
    -d "email=john@example.com" \
    -d "content=Hello, world!" \
    -H "Content-Type: application/x-www-form-urlencoded"

curl -X GET http://localhost:5000/api/timeline_post

curl -X DELETE http://localhost:5000/api/timeline_post \
    -d "id=1"