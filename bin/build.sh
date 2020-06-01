#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/googleoauth2 .
docker tag pyengine/googleoauth2 pyengine/googleoauth2:1.0
docker tag pyengine/googleoauth2 spaceone/googleoauth2:1.0
