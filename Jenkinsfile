pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Automated Tests') {
            steps {
                echo 'Running Python Integration Tests...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install flask
                python3 test_app.py
                '''
            }
        }
        
       stage('Build Production Images') {
            steps {
                echo 'Tests passed! Building the Docker images...'
                // Build the Python App
                sh 'docker build -t devops-python-app:latest -f Dockerfile .'
                // Build the custom Nginx Proxy
                sh 'docker build -t devops-nginx:latest -f Dockerfile.nginx .'
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying the multi-container architecture...'
                
                sh '''
                # 1. Create a private network for the containers
                docker network create devops-net || true
                
                # 2. Delete any old containers
                docker rm -f live-python-app || true
                docker rm -f live-nginx || true
                
                # 3. Launch the Python App (Hidden on the private network)
                docker run -d --network devops-net --name live-python-app devops-python-app:latest
                
                # 4. Launch Nginx (Public facing on port 80, using our new custom baked image)
                docker run -d -p 80:80 --network devops-net --name live-nginx devops-nginx:latest
                '''
            }
        }
    }
}