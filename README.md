# Sistema Escolar Monitorado
Uma aplicação criada com o framework Flask com funções de cadastro e gerenciamento de alunos. A aplicação é monitorada a partir do Prometheus e Grafana, e pode ser inicializada com testes automatizados a partir do Jenkins.

## Requisitos de sistema
Para que tudo funcione corretamente, é necessário instalar as dependências
- [Docker](https://docs.docker.com/engine/install/) 
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Jenkins](https://www.jenkins.io/doc/book/installing/)

## Baixar o repositório
Acesse o diretório desejado e clone o repositório em sua máquina
```bash
  git clone https://github.com/gustavoLadchuk/trabalho-devops-23.10011-8
```

## Iniciar o Jenkins
Digite o comando abaixo para que o Jenkins inicie em seu sistema
```bash
  sudo systemctl start jenkins
```
Obs: Tenha certeza de que nada esteja sendo hospedado na porta 8080

### Monitorar o status do Jenkins
Digite o seguinte comando para verificar se o Jenkins está funcionando corretamente
```bash
  sudo systemctl start jenkins
```

## Acessar o jenkins
Para acessar o Jenkins, acesse o localhost na porta 8080
- http://localhost:8080

## Alternativa: rodar a aplicação sem usar o Jenkins
```bash
  sudo docker compose up -d --build
```

***

## Parar a aplicação
```bash
  sudo docker compose down
```

## Remover todos os containers caso não tenham sido removidos
```bash
  docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
```

## Parar o Jenkins
```bash
  sudo systemctl stop jenkins
```
