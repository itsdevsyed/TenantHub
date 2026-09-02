pipeline {
    agent any

    stages {
        stage('Check Python') {
            steps {
                sh 'python3 --version || true'
                sh 'pip3 --version || true'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --user -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }
    }
}
