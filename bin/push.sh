#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/googleoauth2:1.0
docker push spaceone/googleoauth2:1.0
