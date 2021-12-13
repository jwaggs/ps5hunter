# What and Why

My son wants a PlayStation 5 for Christmas. So do I.

They sell out within seconds of coming back into stock at any store.
This is a quick and dirty bot to gain an edge in the hunt for a ps5.

This is not professional work.

## Quickstart

This bot relies on selenium to load webpages, and twilio to send sms notifications.

If you already have a selenium grid running and create a trial twilio account, 
you can quickly get this bot running locally in a container via:
```
docker build -t hunter .
docker run --env SELENIUM_URL --env TWILIO_ACCOUNT_SID --env TWILIO_AUTH_TOKEN --env TWILIO_PHONE_NUM --env SMS_NOTIFY_NUM hunter
```

## Deployed Bot - Kubernetes on Google Cloud (GKE)

You can use GCP free credits to run this bot for a while. At time of writing, you can get $300 in free credits on GCP.

Once a GCP project is created, download and authenticate gcloud cli.

Run the deploy script `deploy.zsh` (swapping the project id and cluster id for your own).

Use GCP Scheduler to invoke the deployed hunter as often as you want.

Voilà
