# bail on any error
set -e

# build, tag and push our ps5hunter python script
docker build -t us.gcr.io/ps5hunter/hunter:latest .
docker push us.gcr.io/ps5hunter/hunter:latest

# apply deployment
kubectl apply -f deploy/hunter/hunter-deployment.yaml

# trigger fresh pods if the apply didn't
kubectl rollout restart deployment hunter
