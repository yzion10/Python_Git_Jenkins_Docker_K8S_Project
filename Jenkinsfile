def JOB1_SUCCESS = false
def HELM_CHART_DEPLOYED_OK = false
def URL_WRITTEN_INTO_FILE = false
def imageTag = env.BUILD_NUMBER
def rest_app = 'rest_app.py'
def backend_testing = 'backend_testing.py'
def clean_environment = 'clean_environment.py'

pipeline
{
    options
    {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }

    agent any

    stages
    {
        stage('checkout Git Repo')
        {
            steps
            {
                script
                {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                }

                git 'https://github.com/yzion10/Python_Git_Jenkins_Docker_K8S_Project.git'
            }
        }
        stage('Run rest_app.py')
        {
            steps
            {
                script
                {
                    def isSuccess = false

                    try
                    {
                        bat "start /min python $rest_app"
                        isSuccess = true
                    }
                    catch (Exception e)
                    {
                        isSuccess = false
                        echo "$rest_app Error: ${e.getMessage()}"
                    }
                    finally
                    {
                        JOB1_SUCCESS = isSuccess
                    }
                }
            }
        }
        stage('Run backend_testing.py')
        {
            when
            {
                expression
                {
                    JOB1_SUCCESS
                }
            }
            steps
            {
                script
                {
                    try
                    {
                        bat "python $backend_testing"
                    }
                    catch (Exception e)
                    {
                        echo "$backend_testing Error: ${e.getMessage()}"
                    }
                }
            }
        }
        stage('Run clean_environment.py')
        {
            when
            {
                expression
                {
                    JOB1_SUCCESS
                }
            }
            steps
            {
                script
                {
                    try
                    {
                        bat "python $clean_environment"
                    }
                    catch (Exception e)
                    {
                        echo "$clean_environment Error: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('build_Image_locally')
        {
            steps
            {
                script
                {
                    bat "docker build -t yzion10/dockerapp:${imageTag} ."
                }
            }
        }

        stage('push_Image_ToDockerHub')
        {
            steps
            {
                script
                {
                    // Not working
                    //docker.withRegistry('', 'docker_hub')
                    //{
                    //    def image = docker.image("yzion10/dockerapp:${imageTag}")
                    //    image.push()
                    //}

                    bat "docker push yzion10/dockerapp:${imageTag}"
                }
            }
        }

        stage('set_compose_version')
        {
            steps
            {
                script
                {
                    bat "echo IMAGE_TAG=${imageTag} > .env"
                }
            }
        }

        stage('Run docker_compose')
        {
            steps
            {
                script
                {
                    // Run the container using the .env file to get from him the IMAGE_TAG
                    bat 'docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Test_dockerized_app')
        {
            steps
            {
                script
                {
                    bat 'pip install -r requirements.txt'
                    bat 'python docker_backend_testing.py'
                }
            }
        }

        stage('Clean_container')
        {
            steps
            {
                script
                {
                    bat 'docker-compose down'
                    bat "docker image rmi yzion10/dockerapp:${imageTag}"
                }
            }
        }

        stage('Deploy Helm Chart')
        {
            steps
            {
                script
                {
                    def isSuccess = false

                    try
                    {
                        bat 'helm install flaskchart flaskchart'
                        bat 'helm upgrade --install flaskchart flaskchart --set image.version="${imageTag}"'
                        bat "sed -i 's/version: "[0-9]*"/version: "${imageTag}"/' flaskchart/values.yaml"
                        bat 'helm upgrade --install flaskchart flaskchart -f flaskchart/values.yaml'

                        isSuccess = true
                    }
                    catch (Exception e)
                    {
                        isSuccess = false
                        echo "Deploy Helm Chart Error: ${e.getMessage()}"
                    }
                    finally
                    {
                        HELM_CHART_DEPLOYED_OK = isSuccess
                    }
                }
            }
        }
        stage('Write Service URL Into File')
        {
            when
            {
                expression
                {
                    HELM_CHART_DEPLOYED_OK
                }
            }
            steps
            {
                script
                {
                    def isSuccess = false

                    try
                    {
                        bat 'minikube service flaskchart --url >k8s_url.txt'

                        isSuccess = true
                    }
                    catch (Exception e)
                    {
                        isSuccess = false
                        echo "Write Service URL Into File Error: ${e.getMessage()}"
                    }
                    finally
                    {
                        URL_WRITTEN_INTO_FILE = isSuccess
                    }
                }
            }
        }
        stage('Test deployed app')
        {
            when
            {
                expression
                {
                    HELM_CHART_DEPLOYED_OK && URL_WRITTEN_INTO_FILE
                }
            }
            steps
            {
                script
                {
                    bat 'pip install -r requirements.txt'
                    bat 'python K8S_backend_testing.py'
                }
            }
        }
        stage('Clean HELM environment')
        {
            when
            {
                expression
                {
                    HELM_CHART_DEPLOYED_OK
                }
            }
            steps
            {
                script
                {
                    bat 'helm delete flaskchart'
                }
            }
        }
    }
    post
    {
        failure
        {
            emailext subject: 'Pipeline Failed',
                     body: 'The Jenkins pipeline failed (Python_Git_Jenkins_Docker_K8S_Project)',
                     to: 'yzion10@gmail.com',
                     from: 'yzion10@gmail.com'
        }
    }
}
