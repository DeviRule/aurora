#!/bin/bash

set -eu
IMAGE_NAME="aurora:latest"
SOURCE_PATH="/home/sefcom/hulin/shared"

cmd="sudo docker run -v ${SOURCE_PATH}:/shared -it ${IMAGE_NAME} /usr/bin/bash"

echo "$cmd"
$cmd