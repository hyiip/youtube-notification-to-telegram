export $(grep -v '^#' .env | xargs)

gcloud  --project $project beta functions deploy channel_noti \
--runtime python37 \
--trigger-http \
--allow-unauthenticated \
--region=us-central1 \
--security-level=secure-always
