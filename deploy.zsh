# bail on any error
set -e

# use gcloud cli to ensure config is set to right project etc etc.
gcloud config set project ps5hunter
gcloud config set compute/region us-central1

# get cluster credentials from gcloud
gcloud container clusters get-credentials ps5hunter --region us-central1 --project ps5hunter

# build local repo then push it as hunter image to gcr
docker build -t us.gcr.io/ps5hunter/hunter:latest .
docker push us.gcr.io/ps5hunter/hunter:latest

# TODO: remove secrets from config map
# create config map for env vars
kubectl create configmap hunter-config \
    --from-literal=TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID" \
    --from-literal=TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN" \
    --from-literal=TWILIO_FROM_NUM="$TWILIO_FROM_NUM" \
    --from-literal=SMS_NOTIFY_NUM="$SMS_NOTIFY_NUM" \
    --from-literal=SELENIUM_URL="$SELENIUM_URL"

# create hunter deployment
kubectl apply -f deploy/hunter/hunter-deployment.yaml

# expose hunter deployment externally with a load-balancer
kubectl expose deployment hunter --name=hunter-external --labels="app=hunter,external=true" --type=LoadBalancer

# create internal service
# kubectl apply -f deploy/hunter/hunter-svc.yaml
