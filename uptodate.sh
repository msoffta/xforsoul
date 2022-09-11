#!/bin/bash
killall -9 python3
killall -9 python
killall -9 amain.py
git pull
python amain.py