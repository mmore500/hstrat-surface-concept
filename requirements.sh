#!/usr/bin/env bash

cd "$(dirname "$0")"

python3 -m uv pip compile requirements.in --python 3.10 > requirements.txt
