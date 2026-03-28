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
                echo 'Setting up Python environment and running tests...'
                sh '''
                # Create a virtual environment and activate it
                python3 -m venv venv
                . venv/bin/activate
                
                # Install Flask and run our test script
                pip install flask
                python3 test_app.py
                '''
            }
        }
    }
}