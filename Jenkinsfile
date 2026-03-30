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
        
        stage('Build Production Image') {
            steps {
                echo 'Tests passed! Building the Docker image...'
                sh 'docker build -t devops-python-app:latest .'
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