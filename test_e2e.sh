#!/bin/bash

IMAGE_NAME="neuralink-image-service-prompt"
CONTAINER_NAME="neuralink-image-service-container"
HOST="localhost"
PORT="50051"

function log() {
	echo "[$(date)] $1"
}

log "Building Docker image $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

log "Generate gRPC files..."
docker run \
	-v "$(pwd):/root" \
	--name $CONTAINER_NAME \
	$IMAGE_NAME \
	./build
docker container rm $CONTAINER_NAME

log "Starting NLImageService server at $HOST:$PORT in Docker container $CONTAINER_NAME..."
docker run \
	-d \
	-v "$(pwd):/root" \
	--name $CONTAINER_NAME \
	$IMAGE_NAME \
	./server --host $HOST --port $PORT

log "Sleeping..."
sleep 10

rm -f mean_filter*.png

log "Running mean filter..."
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output mean_filter.png \
	--mean_filter && \

rm -f rotate*.png && \

log "Running no rotation..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output rotate_none.png \
	--rotate none && \

log "Running ninety deg rotation..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output rotate_ninety_deg.png \
	--rotate NINETY_DEG && \

log "Running one eighty deg rotation..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output rotate_one_eighty_deg.png \
	--rotate ONE_EIGHTY_DEG && \

log "Running two deventy deg rotation..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output rotate_two_seventy_deg.png \
	--rotate TWO_SEVENTY_DEG && \

log "Running mean filter and rotation simultaneously..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output mean_filter_and_rotate.png \
	--mean_filter \
	--rotate NINETY_DEG && \

log "Testing outputting to jpeg..." && \
docker container exec $CONTAINER_NAME ./client \
	--host $HOST \
	--port $PORT \
	--input signing_dec_of_ind.jpg \
	--output rotate_jpeg.jpg \
	--rotate NINETY_DEG && \

log "Stopping Docker container $CONTAINER_NAME..." && \
docker container stop $CONTAINER_NAME && \
log "Deleting Docker container $CONTAINER_NAME..." && \
docker container rm $CONTAINER_NAME && \
log "Deleting Docker image $IMAGE_NAME..." && \
docker image rm $IMAGE_NAME
