## Setting up the project
- Install dependencies
  - [Python](https://www.python.org/)
  - [gcloud CLI](https://cloud.google.com/sdk/docs/install)
  - [Docker](https://www.docker.com/products/docker-desktop/) (Docker Desktop should run in background)
- Fork the project then clone
```
git clone git@github.com:<your-username>/pdf-to-image-gcp.git
cd pdf-to-image-gcp
```
- Install project requirements
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Configure `gcloud` for the first time 
```
gcloud auth login
gcloud auth application-default login
gcloud auth configure-docker

# Need this configuration for the release script to work
gcloud config configurations create <any-name-of-your-choice>
gcloud config set project <YOUR-PROJECT>
gcloud config set account <YOUR-EMAIL>
```

## Deploy cloud function
Run the deployment script. It assumes that there's already a cloud function with that name setup
on Google Cloud Run Functions.
```
./scripts/deploy.sh
```
If the file is not executable, you need to run this only once `chmod +x ./scripts/deploy.sh`.

⚠️ CAUTION! Do not use Cloud Run Function's inline editor UI to make changes to the cloud function!
