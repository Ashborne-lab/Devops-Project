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

        // ── 6. Security Scan ────────────────────────────────────────
        stage('Security Scan') {
            steps {
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

        // ── 7. Deploy ──────────────────────────────────────────────
        stage('Deploy with Compose') {
            steps {
                echo 'Deploying multi-container stack via Docker Compose...'
                sh '''
                    docker compose down --remove-orphans || true
                    docker compose up -d --build
                '''
            }
        }

        // ── 8. Verify ──────────────────────────────────────────────
        stage('Post-Deploy Health Check') {
            steps {
                echo 'Waiting for services to stabilise...'
                sh 'sleep 10'
                echo 'Running deployment health check...'
                sh '''
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)
                    if [ "$STATUS" != "200" ]; then
                        echo "Health check FAILED (HTTP $STATUS)"
                        exit 1
                    fi
                    echo "Health check PASSED (HTTP 200)"
                    curl -s http://localhost/health | python3 -m json.tool
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