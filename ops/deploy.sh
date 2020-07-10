#!/bin/bash

# shellcheck disable=SC2164
cd "$(dirname "$0")"

SERVER_IP=${1}

if [ "$SERVER_IP" = "" ]; then
  echo "Please pass in the server IP address"
else
  DEPLOY_PATH="ec2-user@$SERVER_IP:/home/ec2-user"
  scp -r -i greenery.pem ../src "$DEPLOY_PATH"
fi