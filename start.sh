#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P >> hal.log
hypercorn --bind localhost:8001 hal.asgi:application >> hal.log
