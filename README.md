# summary-dockerized

## Table of Contents
- [Model Configuration](#model-configuration)
- [Using the Repo](#using-the-repo)
- [Creating a TAR File](#creating-a-tar-file)
- [Running Docker Image from a TAR File](#running-docker-image-from-a-tar-file)
- [Specs](#specs)
- [Test Results](#test-results)

## Model configuration
- `sshleifer/distilbart-cnn-12-6` finetuned on dialoguesum is used for summarization

## Using the repo
1. Install docker using following [link](https://docs.docker.com/engine/install/)
2. Clone the repo
```bash
git clone https://github.com/SkAndMl/summary-dockerized.git 
```
3. cd into the repo
```bash
cd summary-dockerized
```
4. Create the docker container and run the translation api using
```bash
docker-compose up --build
```
5. Verify and use the api at `https://localhost:8000/docs` , the summary api expects a list of dialogues

## Creating a TAR file
1. Build the image
```bash
docker-compose build
```
2. Tag the image
```bash
docker tag summary-dockerized-translate:latest your_dockerhub_username/summary-dockerized:latest
```
3. Save Docker to a TAR file
```bash
docker save -o summary-dockerized.tar your_dockerhub_username/summary-dockerized:latest
```
## Running docker image from a TAR file
1. Load the image
```bash
docker load -i summary-dockerized.tar
```
2. Run the image
```bash
docker-compose up
```

## Specs
- Expected image size - ~ 2.4GB (obtained from docker hub)
- Expect RAM usage - ~ 2.2GB (distilbart is 9.4GB)
- Device:
    *  CPU: Apple M2
    *  RAM: 16GB
    *  Storage: 256GB

## Test Results
Average ROUGE-1 Score: 0.3162
Average ROUGE-2 Score: 0.1113
Average ROUGE-L Score: 0.2498