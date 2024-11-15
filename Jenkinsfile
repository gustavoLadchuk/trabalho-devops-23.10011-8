pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Test') {
            steps {
                
            }
        }
	stage('Build') {
	    steps {
	    sh '''
		docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
		docker compose up -d --build
		docker compose ps
	    '''
	}
    }
    }
}
