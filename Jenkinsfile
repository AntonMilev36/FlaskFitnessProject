// Some comment, that have a change
pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    pytest --maxfail=1 --disable-warnings -q --junitxml=test-results/results.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'test-results/results.xml'
        }
    }
}
