# bail on any error
set -e

# use gcloud cli to ensure config is set to right project etc etc.
gcloud config set project ps5hunter
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1b

# get cluster credentials from gcloud
gcloud container clusters get-credentials ps5hunter --region us-central1 --project ps5hunter

source deploy/create-config.zsh
source deploy/create-secrets.zsh
source deploy/create-service-accounts.zsh
source deploy/deploy-selenium.zsh
source deploy/deploy-hunter.zsh
