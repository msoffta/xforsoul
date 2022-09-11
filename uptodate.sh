#!/bin/bash
screen -r 36071
kill -9 amain.py
git pull
python /home/sun/workspace/c/src/server.py &