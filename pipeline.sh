#!/bin/sh

echo "Starting pipeline..."

echo "Running Azure forward translation..."
python3 azure/forward_translate.py

echo "Running Google forward translation..."
python3 googlecloud/forward_translate.py 

echo "Running forward evaluation..."
python3 evaluation/forward_evaluation.py
