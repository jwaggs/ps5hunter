# bail on any error.
set -e

# twilio keys and nums used to send sms notifications.
kubectl create secret generic twilio \
  --from-literal=TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID" \
  --from-literal=TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN" \
  --from-literal=TWILIO_FROM_NUM="$TWILIO_FROM_NUM" \
  --from-literal=SMS_NOTIFY_NUM="$SMS_NOTIFY_NUM"
