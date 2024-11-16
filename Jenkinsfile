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
		docker compose build
		docker compose up -d
		docker compose ps
	    '''
	}
    }
	 stage('Test') {
	    steps {
	    sh '''
		docker logs mariadb_container
		docker logs flask_app_container			
	    '''
	    }
	}  
    }
}
