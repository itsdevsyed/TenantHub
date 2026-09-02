pipeline {
    agent {
        docker {
            image 'python:3.11-slim-bookworm'
        }
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version

                    python -m venv .venv

                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    .venv/bin/python -m pytest
                    TEST_EXIT_CODE=$?

                    if [ $TEST_EXIT_CODE -eq 5 ]; then
                        echo "No tests found. Skipping test failure for now."
                        exit 0
                    fi

                    exit $TEST_EXIT_CODE
                '''
            }
        }
    }

    post {
        success {
            echo 'TenantHub CI pipeline completed successfully!'
        }

        failure {
            echo 'TenantHub CI pipeline failed!'
        }
    }
}
