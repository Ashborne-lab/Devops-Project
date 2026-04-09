pipeline {
    agent any

    environment {
        APP_IMAGE   = 'devops-python-app'
        NGINX_IMAGE = 'devops-nginx'
        APP_VERSION = "${env.BUILD_NUMBER ?: 'latest'}"
        NETWORK     = 'devops-net'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {

        // ── 1. Source ────────────────────────────────────────────────
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Building version: ${APP_VERSION}"
            }
        }

        // ── 2. Dependencies ──────────────────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // ── 3. Code Quality ─────────────────────────────────────────
        stage('Lint & Code Quality') {
            steps {
                echo 'Running flake8 linting...'
                sh '''
                    . venv/bin/activate
                    flake8 app.py test_app.py --statistics --count
                '''
            }
        }

        // ── 4. Tests ────────────────────────────────────────────────
        stage('Unit & Integration Tests') {
            steps {
                echo 'Running pytest with JUnit XML output...'
                sh '''
                    . venv/bin/activate
                    pytest test_app.py -v --tb=short --junitxml=reports/test-results.xml
                '''
            }
        }

        // ── 5. Build ───────────────────────────────────────────────
        stage('Build Production Images') {
            steps {
                echo 'Building Docker images...'
                sh """
                    docker build -t ${APP_IMAGE}:${APP_VERSION} -t ${APP_IMAGE}:latest -f Dockerfile .
                    docker build -t ${NGINX_IMAGE}:${APP_VERSION} -t ${NGINX_IMAGE}:latest -f Dockerfile.nginx .
                """
            }
        }

        // ── 6. Security Scan (non-blocking) ─────────────────────────
        stage('Security Scan') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    echo 'Installing Trivy (if not present) and scanning images...'
                    sh '''
                        if ! command -v trivy &> /dev/null; then
                            echo "Trivy not found — installing..."
                            curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                        fi
                    '''
                    sh """
                        trivy image --severity HIGH,CRITICAL --exit-code 0 --no-progress ${APP_IMAGE}:${APP_VERSION}
                        trivy image --severity HIGH,CRITICAL --exit-code 0 --no-progress ${NGINX_IMAGE}:${APP_VERSION}
                    """
                }
            }
        }

        // ── 7. Deploy ──────────────────────────────────────────────
        stage('Deploy Containers') {
            steps {
                echo 'Deploying multi-container stack...'
                sh """
                    # Create network if it doesn't exist
                    docker network create devops-net || true

                    # Stop and remove old containers
                    docker rm -f live-python-app live-nginx || true

                    # Run Flask app container
                    docker run -d \
                        --name live-python-app \
                        --network devops-net \
                        --restart unless-stopped \
                        --memory 256m \
                        --cpus 1.0 \
                        -e FLASK_ENV=production \
                        ${APP_IMAGE}:${APP_VERSION}

                    # Wait for app to be healthy
                    echo 'Waiting for Flask app to start...'
                    sleep 5

                    # Run Nginx container
                    docker run -d \
                        --name live-nginx \
                        --network devops-net \
                        --restart unless-stopped \
                        -p 80:80 \
                        ${NGINX_IMAGE}:${APP_VERSION}
                """
            }
        }

        // ── 8. Verify ──────────────────────────────────────────────
       stage('Post-Deploy Health Check') {
            steps {
                echo 'Waiting for services to stabilise...'
                sh 'sleep 10'
                
                echo 'Running deployment health check...'
                sh '''
                # 1. Use host.docker.internal to escape the Jenkins container
                # 2. Check the /metrics endpoint which actually exists in our app
                STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal/metrics)
                
                if [ "$STATUS" != "200" ]; then
                    echo "Health check failed! Nginx returned status: $STATUS"
                    exit 1
                fi
                echo "Health check passed! Telemetry API is live."
                '''
            }
        }
    }

    post {
        success {
            echo """
            ╔══════════════════════════════════════════════╗
            ║   ✅  DEPLOYMENT SUCCESSFUL — v${APP_VERSION}        ║
            ║   Dashboard: http://localhost                ║
            ╚══════════════════════════════════════════════╝
            """
        }
        failure {
            echo """
            ╔══════════════════════════════════════════════╗
            ║   ❌  PIPELINE FAILED — check logs above     ║
            ╚══════════════════════════════════════════════╝
            """
        }
        always {
            echo 'Cleaning up dangling Docker images...'
            sh 'docker image prune -f || true'
        }
    }
}