#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P
daphne -b localhost -p 8001 hal.asgi:application
