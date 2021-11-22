# What and Why

My son wants a PlayStation 5 for Christmas, and frankly so do I.
They sell out within an hour of coming back into stock at any store.
This is a quick and dirty bot to hunt down a ps5 - not professional work.

# Commands to get going

`docker build -t us.gcr.io/ps5hunter/hunter:latest .`

`docker run --env TWILIO_ACCOUNT_SID --env TWILIO_AUTH_TOKEN --env TWILIO_PHONE_NUM --env SMS_NOTIFY_NUM us.gcr.io/ps5hunter/hunter:latest`


### Option 1 Google Cloud Run

```
### Selenium Browser Deployment

# pull, tag, then push a selenium-chrome container to GCP container registry
docker pull selenium/standalone-chrome
docker image tag selenium/standalone-chrome us.gcr.io/ps5hunter/headless-chrome
docker push us.gcr.io/ps5hunter/headless-chrome

# deploy our chrome service
gcloud run deploy chrome \
    --image us.gcr.io/ps5hunter/headless-chrome \
    --port 4444 \
    --memory 2G

# created service url:
# https://chrome-34ex3ebfba-uc.a.run.app


### Create & Bind Service Account

# create service account
gcloud iam service-accounts create browser-invoker \
    --description "Service account used to call our browser service" \
    --display-name "Browser Invoker"

# bind iam permissions to service account
gcloud run services add-iam-policy-binding chrome  \
    --member serviceAccount:browser-invoker@ps5hunter.iam.gserviceaccount.com \
    --role roles/run.invoker

### Script Deployment

# build, tag and push our ps5hunter python script
docker build -t us.gcr.io/ps5hunter/hunter:latest .
docker push us.gcr.io/ps5hunter/hunter:latest

# deploy our hunter script
gcloud run deploy hunter \
    --image us.gcr.io/ps5hunter/hunter \
    --service-account browser-invoker \
    --allow-unauthenticated \
    --min-instances=0 \
    --max-instances=4 \
    --memory 1G \
    --set-env-vars SELENIUM_URL=$SELENIUM_URL \
    --set-env-vars TWILIO_ACCOUNT_SID=$TWILIO_ACCOUNT_SID \
    --set-env-vars TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN \
    --set-env-vars TWILIO_PHONE_NUM=$TWILIO_PHONE_NUM \
    --set-env-vars SMS_NOTIFY_NUM=$SMS_NOTIFY_NUM

# update image after pushing new one tagged with :latest
gcloud run services update hunter \
    --image us.gcr.io/ps5hunter/hunter


```

### Option 2 Kubernetes

[scalable selenium on k8s](https://github.com/kubernetes/examples/tree/master/staging/selenium)



