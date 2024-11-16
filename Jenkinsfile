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
		docker exec -it mariadb_container mysql -u root -p
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
