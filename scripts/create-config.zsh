# bail on any error
set -e

# TODO: remove secrets from config map
# create config map for env vars
kubectl create configmap hunter-config \
    --from-literal=TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID" \
    --from-literal=TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN" \
    --from-literal=TWILIO_FROM_NUM="$TWILIO_FROM_NUM" \
    --from-literal=SMS_NOTIFY_NUM="$SMS_NOTIFY_NUM" \
    --from-literal=SELENIUM_URL="$SELENIUM_URL"