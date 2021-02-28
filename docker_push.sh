#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push jaybee1971/todo_app:${TRAVIS_COMMIT} 