#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P
hypercorn --bind localhost:8001 hal.asgi:application
