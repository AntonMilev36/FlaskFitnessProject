// Some comment, that have a change
pipeline {
    agent any

    environment {
        VENV = ".venv"
        DB_USER = credentials('postgres')
        DB_PASSWORD = credentials('yourpassword')
        DB_PORT = credentials('5432')
        DB_NAME = credentials('fitness_system')
        TEST_DB_NAME = credentials('fitness_system_testing')
        SECRET_KEY = credentials('your_secret_key')
        AWS_ACCESS_KEY = credentials('aws_secret_key')
        AWS_SECRET = credentials('aws_secret')
        AWS_BUCKET = credentials('yuor_aws_bucket')
        AWS_REGION = credentials('aws_region')
        CLIENT_ID = credentials('paypal_client_id')
        PAYPAL_SECRET = credentials('paypal_secret_key')
        CLIENT_URL = credentials("http://127.0.0.1:5000")
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
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }
}
