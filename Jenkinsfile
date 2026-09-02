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
                    python -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/python -m pytest'
            }
        }
    }
}
