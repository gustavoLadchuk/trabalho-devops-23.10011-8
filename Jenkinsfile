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
    stage('Wait for flask') {
        steps {
            script {
            def isReady = false
            for (int i = 0; i < 10; i++) { // Tentativas por 10 segundos
                try {
                    sh 'curl -X GET http://localhost:5000/alunos'
                    isReady = true
                    break
                } catch (Exception e) {
                    sleep(1) // Aguarda 1 segundo antes de tentar novamente
                }
            }
            if (!isReady) {
                error "Servidor Flask não iniciou a tempo!"
            }
          }
        }
    }
    stage('Test') {
    steps {
	 sh '''
		pytest --maxfail=1 --disable-warnings -q flask/tests/test_app.py				
	    '''
	    }
	}  
    }
}
