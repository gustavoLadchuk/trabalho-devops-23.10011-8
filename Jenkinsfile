pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
	stage('Build') {
	    steps {
	    sh '''
		docker compose down
		docker rm -v -f $(docker ps -qa)
		docker compose build
		docker compose up -d
		docker compose ps
	    '''
	}
    }
	 stage('Test') {
	    steps {
	    sh '''
	
	    '''
	    }
	}  
    }
}
