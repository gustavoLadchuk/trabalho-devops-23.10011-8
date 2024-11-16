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
		docker-compose logs -f mariadb
		docker-compose logs -f flask_app			
	    '''
	    }
	}  
    }
}
