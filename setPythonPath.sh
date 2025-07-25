#!/bin/bash

#echo "Actual Path: $PWD"
unset DISPLAY
export PYTHONPATH="$PWD"
echo "PYTHONPATH updated"
# nohup python -u src/gridSearch.py > FitFalse.out 2> FitFalse.err &
# nohup python -u src/gridSearch.py > FitTrueConstantArea1Stim.out 2>&1 &