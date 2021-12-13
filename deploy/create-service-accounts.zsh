# adapted from `https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity`

# bail on any error
set -e

# env config
PROJECT_ID=ps5hunter
K8S_SA=hunter-k8s-sa
GCP_SA=hunter-iam-sa
# IAM_ROLE=browser-invoker@ps5hunter.iam.gserviceaccount.com

# create k8s service account
kubectl create serviceaccount "$K8S_SA"

# create gcp service account
gcloud iam service-accounts create "$GCP_SA"

# bind gcp iam service account to iam role
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member "serviceAccount:$GCP_SA@$PROJECT_ID.iam.gserviceaccount.com" \
    --role roles/storage.objectCreator \
    --role roles/storage.objectViewer

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member "serviceAccount:$GCP_SA@$PROJECT_ID.iam.gserviceaccount.com" \
    --role roles/iam.serviceAccountTokenCreator

# bind gcp iam service account to k8s service account
gcloud iam service-accounts add-iam-policy-binding "$GCP_SA@$PROJECT_ID.iam.gserviceaccount.com" \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$PROJECT_ID.svc.id.goog[$K8S_SA]"

# annotate k8s service account with iam account
kubectl annotate serviceaccount "$K8S_SA" \
    "iam.gke.io/gcp-service-account=$GCP_SA@$PROJECT_ID.iam.gserviceaccount.com"
