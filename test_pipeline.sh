#!/bin/bash

set -e
echo "Starting pipeline..."

echo "Running Azure forward translation..."
python3 azure/test_forward_translate.py

echo "Running Google forward translation..."
python3 googlecloud/test_forward_translate.py 

echo "Running forward evaluation..."
python3 evaluation/test_forward_evaluation.py

echo "Running Azure backward translation..."
python3 azure/test_backward_translate.py

echo "Running Google backward translation..."
python3 googlecloud/test_backward_translate.py

echo "Running backward evaluation..."
python3 evaluation/test_backward_evaluation.py

echo "Pipeline ran successfully."
