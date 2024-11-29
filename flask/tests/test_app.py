import pytest
from flask import Flask
from app import app, db, Aluno  # Importando a aplicação e o banco de dados do seu arquivo app.py

@pytest.fixture
def client():
    # Configuração para usar o banco em memória SQLite durante os testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # Criar as tabelas no banco de dados em memória
    with app.app_context():
        db.create_all()

    # Criar o cliente para fazer as requisições
    with app.test_client() as client:
        yield client

    # Limpar o banco de dados após os testes
    with app.app_context():
        db.drop_all()

def test_listar_alunos(client):
    response = client.get('/alunos')
    assert response.status_code == 200
    assert response.json == []

def test_adicionar_aluno(client):
    novo_aluno = {
        'nome': 'João',
        'sobrenome': 'Silva',
        'turma': '1A',
        'disciplinas': 'Matemática, Física'
    }

    response = client.post('/alunos', json=novo_aluno)
    assert response.status_code == 201
    assert response.json == {'message': 'Aluno adicionado com sucesso!'}
    
    response = client.get('/alunos')
    assert response.status_code == 200
    alunos = response.json
    assert len(alunos) == 1
    assert alunos[0]['nome'] == 'João'
    assert alunos[0]['sobrenome'] == 'Silva'
    assert alunos[0]['turma'] == '1A'
    assert alunos[0]['disciplinas'] == 'Matemática, Física'
