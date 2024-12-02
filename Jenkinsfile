def buildAndPushTag(Map args) {
    def defaults = [
        registryUrl: "https://registry.hub.docker.com",  
        dockerfileDir: "./",
        dockerfileName: "Dockerfile",
        buildArgs: "",
        pushLatest: true
    ]
    args = defaults + args
    
    //def dockerImage = docker.build "${DOCKER_REGISTRY}" + ":${buildTag}"

    echo 'Loggin in registry'
    docker.withRegistry(args.registryUrl, registryCredential) {
        echo 'buildin image'
        def image = docker.build(args.image, "${args.buildArgs} ${args.dockerfileDir} -f ${args.dockerfileName}")
        echo 'Pushing image'
        image.push(args.buildTag)
        if(args.pushLatest) {
            image.push("latest")
            sh "docker rmi --force ${args.image}:latest"
        }
        sh "docker rmi --force ${args.image}:${args.buildTag}"
 
        return "${args.image}:${args.buildTag}"
    }
}

pipeline {
    agent any

    environment {
        IMAGE_NAME = "fomazione_sou_k8s" 
        DOCKER_USER = "corradot93"  
        registryCredential = 'dockerhub_id'

    }

    stages {
        stage('Determine Tag') {
            steps {
                script {
                    // Determine the tag based on the Git branch or tag
                    def branch = env.GIT_BRANCH
                    echo 'Pulling...' + env.BRANCH_NAME
                    def gitTag = env.GIT_TAG
                    echo 'tag...' + env.GIT_BRANCH
                    def commitSha = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()

                    if (gitTag) {
                        // If it's a tag, use the tag name
                        env.DOCKER_TAG = gitTag
                    } else if (branch == 'main') {
                        // If it's the master branch, use the "latest" tag
                        env.DOCKER_TAG = 'latest'
                    } else if (branch == 'develop') {
                        // If it's the develop branch, use "develop-<commitSha>"
                        env.DOCKER_TAG = "develop-${commitSha}"
                    } else {
                        // Fallback to branch name if it's not master or develop
                        env.DOCKER_TAG = branch
                    }

                    echo "Docker image tag: ${env.DOCKER_TAG}"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'calling Pushing image'
                    buildAndPushTag(
                        image: "${env.DOCKER_USER}/${env.IMAGE_NAME}",
                        buildTag: "${env.DOCKER_TAG}",
                        buildArgs: "",  // You can add any build arguments if needed
                        pushLatest: (env.DOCKER_TAG == 'latest') // Only push "latest" if the tag is "latest"
                    )
                }
            }
        }

        stage('Using helm to install on kubernates cluster') {
            steps {
                script {
                    echo 'Set kubeconfig'
                    sh "export KUBECONFIG=/root/.kube/config"
                    echo 'Run helm install'
                    sh "helm upgrade --install --kubeconfig=/var/jenkins_home/.kube/kubeconfig flask-app ./flask-app-chart --kube-insecure-skip-tls-verify --set tag=${env.DOCKER_TAG} --debug"  
                }
            }
        }        
    }

    post {
        always {
            // Clean up Docker images (optional)
            sh "docker system prune -f"
        }
    }
}
