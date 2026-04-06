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
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying the multi-container architecture...'
                
                sh '''
                # 1. Create a private network for the containers to talk to each other
                docker network create devops-net || true
                
                # 2. Delete any old containers
                docker rm -f live-python-app || true
                docker rm -f live-nginx || true
                
                # 3. Launch the Python App (Hidden from the outside world, no -p flag!)
                docker run -d --network devops-net --name live-python-app devops-python-app:latest
                
                # 4. Launch Nginx (Public facing on port 80, mounted with our config file)
                docker run -d -p 80:80 --network devops-net --name live-nginx -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf nginx:alpine
                '''
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying the live website...'
                // If an old version is running, delete it first
                sh 'docker rm -f live-python-app || true'
                // Launch the new updated website
                sh 'docker run -d -p 5000:5000 --name live-python-app devops-python-app:latest'
            }
        }
    }
}