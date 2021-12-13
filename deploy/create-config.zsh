# bail on any error
set -e

# create config map for env vars
kubectl create configmap hunter-config \
    --from-literal=SELENIUM_URL="$SELENIUM_URL"
