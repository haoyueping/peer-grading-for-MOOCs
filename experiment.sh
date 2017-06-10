#!/bin/bash

# not done yet!!!!!!!!!!!!
for k in `seq 6 4 24`;
do
  python3 experiments/displacement.py em_borda 1000 $k 10
done
