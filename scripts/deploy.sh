#!/usr/bin/env bash

set -e  # Exit the script if any of the following commands throws an error

# This assumes that the configuration already exists
gcloud config configurations activate <any-name-of-your-choice>

PROJECT_ID="<YOUR-PROJECT-ID>"
FUNCTION_NAME="<YOUR-FUNCTION-NAME>"

# Build the container
gcloud builds submit --tag gcr.io/$PROJECT_ID/$FUNCTION_NAME

# Deploy the container to Cloud Run
gcloud run deploy $FUNCTION_NAME \
    --image gcr.io/$PROJECT_ID/$FUNCTION_NAME \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
