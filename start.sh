#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P
{ venv/bin/hypercorn --bind localhost:8001 hal.asgi:application; } >> hal.log 2>&1
