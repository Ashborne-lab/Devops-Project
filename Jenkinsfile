pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                // This tells Jenkins to securely download your code from GitHub
                checkout scm
            }
        }
        
        stage('Verify Files') {
            steps {
                echo 'Successfully pulled code from GitHub!'
                // This lists the files to prove they are there
                sh 'ls -la' 
            }
        }
    }
}