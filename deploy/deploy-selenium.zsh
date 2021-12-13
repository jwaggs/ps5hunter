# bail on any error
set -e

# create selenium hub deployment
kubectl create --filename=selenium/selenium-hub-deployment.yaml

# create selenium hub service
kubectl create --filename=selenium/selenium-hub-svc.yaml

# create selenium chrome workers
kubectl create --filename=selenium/selenium-node-chrome-deployment.yaml

# FIREFOX disabled for now
# create selenium firefox workers
# kubectl create --filename=selenium/selenium-node-firefox-deployment.yaml
