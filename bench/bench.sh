#!/bin/bash

set -e # exit with error if any of this fails

cd "$(dirname "$0")"

python3 -O bench.py
