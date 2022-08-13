#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P
{ .venv/bin/daphne --b localhost -p 8001 hal.asgi:application; } >> hal.log 2>&1
