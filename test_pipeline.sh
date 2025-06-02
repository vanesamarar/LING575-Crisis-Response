#!/bin/bash

set -e
start_time=$(date +%s)

echo "Starting pipeline..."

echo "Running Azure forward translation..."
python3 azure/test_azure_translation.py

echo "Running Google forward translation..."
python3 googlecloud/test_google_translation.py 

echo "Running forward evaluation..."
python3 evaluation/test_forward_evaluation.py

echo "Running Azure backward translation..."
python3 azure/test_azure_backtranslation.py

echo "Running Google backward translation..."
python3 googlecloud/test_google_backtranslation.py

echo "Running backward evaluation..."
python3 evaluation/test_back_evaluation.py

end_time=$(date +%s)
elapsed=$(( end_time - start_time ))

echo "Pipeline ran successfully in $elapsed seconds."
