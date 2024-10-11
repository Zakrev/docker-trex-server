#!/bin/bash

python3 -m trex-starter ./server-runner.sh || exit 1
chmod +x ./server-runner.sh || exit 1
./server-runner.sh || exit 1
