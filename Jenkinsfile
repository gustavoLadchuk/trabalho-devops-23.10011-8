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
		echo "Testando método GET
		curl -X GET http://localhost:5000/alunos

		echo "Testando método POST
		curl -X POST http://localhost:5000/alunos \
	    -H "Content-Type: application/json" \
     -d '{
           "nome": "Teste",
           "sobrenome": "Teste",
           "turma": "Teste",
           "disciplinas": "Teste1, Teste2"
         }'
					
	    '''
	    }
	}  
    }
}
