gRPC Image Rotation Service: SOLUTION
=====================================

See `prompt.md` for context.

Requirements
------------

A clean install of Ubuntu 18.04.

Installation
------------

The script `setup`, in the top level directory, installs any dependencies and sets up the system. Runnable via `./setup`.

Build
-----

The script `build` carries out required build steps. It's in the top level directory and runnable via `./build`.

If you'd like to run the solution inside a Docker container, then you can build the image using the provided `Dockerfile`,

```
docker build -t $IMAGE_NAME .
```

Then run `./build` using a throwaway Docker container,

```
docker run \
   -d \
   -v "$(pwd):/root" \
   --name $CONTAINER_NAME \
   $IMAGE_NAME \
   ./build
docker container rm $CONTAINER_NAME
```

Usage
-----

The `gRPC` server that implements the `NLImageService` interface, is runnable via, `./server --port <...> --host <...>`, in the top level directory, e.g.

```
./server --host localhost --port 50051
```

The server runs in blocking mode and will wait until terminated.

The client provides `--port`, `--host`, `--input`, `--output`, `--rotate`, and `--mean` arguments and can be run from the top level directory via `./client --port <...> --host <...> --input <...> --output <...> --rotate <...> --mean`, e.g.

```
./client \
   --host localhost \
   --port 50051 \
   --input /path/to/input_image.jpg \
   --output /path/to/output_image.png \
   --rotate NINETY_DEG
```

To run the server and client in a Docker environment, start a container with a running instance of the server, e.g.

```
docker run \
   -d \
   -v "$(pwd):/root" \
   --name $CONTAINER_NAME \
   $IMAGE_NAME \
   ./server --host $HOST --port $PORT
```

Then run client requests against the server within the container, e.g.

```
docker container exec $CONTAINER_NAME ./client \
   --host $HOST \
   --port $PORT \
   --input /path/to/input_image.jpg \
   --output /path/to/output_image.png \
   --rotate NINETY_DEG
``` 

Test
-----

Unit tests can be checked by running,

```
python test_lib.py

```

Or through the Docker container,

```
docker container exec $CONTAINER_NAME python test_lib.py
``` 

Discussion
----------

Discussion of limitations or known issues with my solution and how I'd change it for production given more time and resources:

* Proper error handling: It's certain that some error cases are not accounted for, through neither the server nor client, and for those that do trigger a failure, the returned error information is indirect and obtuse in many cases.  
* Proper logging: There are some logging statements sprinkled in the source code but there are definitely gaps where added logging can be highly informative. For instance, while applying an image transformation on the server, logging information such as time elapsed.
* Negative test cases: `test_lib.py` contains a number of positive unit tests and `test_e2e.sh` contains a number of positive e2e tests, but there's an obvious lack of test cases for erroneous inputs. 
* Containerization: Although I've created a Docker image for testing the server and client during development, we can further containerize the server, e.g. exposing Docker container ports so the server can interact with container-external entities.
* Source code documentation: There's a marked lack of source code documentation and comments that renders the code unfit for multi-contributor software development. (Also, there are definitely code style errors.)
* Client and server libraries: There's a common library file, `lib.py` containing functions used by both the client and server. In order to keep the client binary light and avoid leaking server details, it's best to omit any server-side-only code from code shared with the client.
* Security: Client-server communication is not encrypted and should be in most production scenarios.
* Timeout: To prevent the client from hanging indefinitely, there should be support for setting a timeout for a request. (Similarly, there should be support to cancel requests.)
* Caching: If it's known that certain requests are going to be repeated, adding a server-side cache can significantly improve response times.
* Asynchronous requests: The client blocks while waiting for the server to respond to a request but users of the client would most likely want asynchronous request handling. (Although, it's arguable whether such functionality is an appropriate concern for the client or code calling the client.)  
