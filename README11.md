# Python_Git_Jenkins_Docker_K8S_Project

**Release date: 15/06/2023**

## Project Description
This project combines two processes for testing a Flask server. The first process involves running a container built from an image using the Docker engine. The second process involves running a container using Kubernetes (minikube). The Helm package is used to manage the running and creation of services. The project utilizes an image from Docker Hub to facilitate testing of the Flask server outside the container. The testing scripts included are `docker_backend_testing.py` and `K8S_backend_testing.py`.

## Technologies Used
- Python for the main project
- Groovy for pipeline scripts
- YAML for various configuration files (`docker-compose.yml`, Helm package files)

## Prerequisites
Before running this project, ensure the following prerequisites are installed:
- Python 3
- Java
- Jenkins
- Docker
- Git
- Kubernetes (minikube)
- Helm package

Additionally, the following steps should be performed:
1. Ensure Docker daemon is running (Docker Desktop).
2. Start Minikube.
3. Have an existing repository on Docker Hub.
4. Set up Jenkins credentials for Docker Hub connection.
5. Run `minikube tunnel` in the command prompt or Git Bash. Refer to the documentation about `minikube tunnel` to set up the LoadBalancer ([minikube.sigs.k8s.io/docs/handbook/accessing](https://minikube.sigs.k8s.io/docs/handbook/accessing/)).

## Project Files
The project includes the following files:

- `db_connector.py`: This file connects to a remote MySQL server and implements methods for INSERT, SELECT, UPDATE, and DELETE operations.
- `rest_app.py`: This file defines routes with a REST API for creating, reading, updating, and deleting users from/to the remote MySQL server. It starts a Flask server (localhost) that runs inside a container created from a Docker image.
- `backend_testing.py`: This script tests the Flask server (`rest_app.py`) locally.
- `clean_environment.py`: This file stops the Flask servers (localhost) from `rest_app.py`. It is protected with error handling in case the servers are unresponsive.
- `templates` folder: This folder contains HTML files for rendering templates in `rest_app.py`.
- `Dockerfile`: This file defines the steps to build an image.
- `docker-compose.yml`: This file runs the container based on the definitions in the `docker-compose.yml` file.
- `docker_backend_testing.py`: This script tests the Flask server (`rest_app.py`) inside the container created by the Docker image. The test runs outside the container and attempts to send/get/put/delete requests to the Flask server.
- `requirements.txt`: This file lists the requirements to be installed before executing the Python files.
- `K8S_backend_testing.py`: This script tests the Flask server (`rest_app.py`) inside the container created by Kubernetes (minikube). The test runs outside the container and attempts to send/get/put/delete requests to the Flask server.
- `flaskchart` folder: This folder contains the Helm package, including `Chart.yaml`, `values.yaml`, `flask-deploy.yaml`, and `flask_service.yaml` files. These files deploy the image repository and run the container on Kubernetes, exposing the URL for testing the Flask server using `K8S_backend_testing.py`.
- `jenkinsfile`: This is a Jenkins pipeline script (in Groovy) that connects to the Git repository and executes the following steps:
   1. Checkout Git repository holding this project.
   2. Run `rest_app.py` to start a Flask server locally.
   3. Run `backend_testing.py` to test the Flask server locally.
   4. Run `clean_environment.py` to shut down the Flask server locally.
   5. Build the Docker image locally.
   6. Push the Docker image to Docker Hub.
   7. Set the compose image version by updating the version inside the `.env` file for `docker-compose` (based on the pipeline build number).
   8. Run `docker-compose` in detached mode to run the container based on the definitions in `docker-compose.yml`.
   9. Test the dockerized app using `docker_backend_testing.py`.
   10. Clean the container by calling `docker-compose down` and deleting the local image.
   11. Deploy the Helm Chart, which deploys the service and runs the container based on the definitions in the Helm package files.
   12. Write the service URL into a file (`k8s_url.txt`) using the `minikube service flaskchart --url` command. This stage is disabled as the URL is exposed and run by the `minikube tunnel` command (refer to prerequisites installations).
   13. The `K8S_backend_testing.py` script tests the Flask server based on the URL (`http://127.0.0.1:5000/users/1`) obtained in the previous stage.
   14. Clean the Helm environment by calling `helm delete`.

## Authors
- Yosi Zion
- Oren Elraz
- Email: yzion10@gmail.com
- LinkedIn: [Yosi Zion](https://www.linkedin.com/in/yosi-zion-bb90a2181/)
