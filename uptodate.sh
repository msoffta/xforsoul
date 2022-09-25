#!/bin/bash
killall -9 python3
killall -9 python
killall -9 amain.py
git pull
python amain.py
screen -r 3419
bash run
screen -r 5268