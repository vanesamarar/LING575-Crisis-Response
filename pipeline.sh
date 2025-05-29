#!/bin/bash

set -e
echo "Starting pipeline..."

echo "Running Azure forward translation..."
python3 azure/forward_translate.py

echo "Running Google forward translation..."
python3 googlecloud/forward_translate.py 

echo "Running forward evaluation..."
python3 evaluation/forward_evaluation.py

echo "Running Azure backward translation..."
python3 azure/backward_translate.py

echo "Running Google backward translation..."
python3 googlecloud/backward_translate.py

echo "Running backward evaluation..."
python3 evaluation/backward_evaluation.py

echo "Pipeline ran successfully."
