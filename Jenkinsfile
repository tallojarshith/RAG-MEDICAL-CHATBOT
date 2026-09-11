pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = 'myrepo'
        IMAGE_TAG = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repository...'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/tallojarshith/RAG-MEDICAL-CHATBOT.git'
                    ]]
                )
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Scan Docker Image with Trivy') {
            steps {
                script {
                    sh """
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --format json \
                    -o trivy-report.json \
                    ${ECR_REPO}:${IMAGE_TAG}
                    """
                }

                archiveArtifacts artifacts: 'trivy-report.json',
                                 allowEmptyArchive: true
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-token']
                ]) {
                    script {

                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        def ecrRegistry =
                            "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                        def imageFullTag =
                            "${ecrRegistry}/${ECR_REPO}:${IMAGE_TAG}"

                        sh """
                        aws ecr get-login-password \
                        --region ${AWS_REGION} \
                        | docker login \
                        --username AWS \
                        --password-stdin ${ecrRegistry}

                        docker tag \
                        ${ECR_REPO}:${IMAGE_TAG} \
                        ${imageFullTag}

                        docker push ${imageFullTag}
                        """
                    }
                }
            }
        }
    }
}