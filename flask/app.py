import time
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import logging

app = Flask(__name__)

# Initialize PrometheusMetrics for automatic metric collection
metrics = PrometheusMetrics(app)

# Define a custom HTTP request counter
http_request_counter = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint']
)

# Configuration for secret key and database
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model definition for "Aluno"
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    disciplinas = db.Column(db.String(200), nullable=False)

# Retry connecting to MariaDB until it is ready
attempts = 5
for i in range(attempts):
    try:
        with app.app_context():
            db.create_all()  # Initialize the database
            # Create a default admin user
            if not appbuilder.sm.find_user(username='admin'):
                appbuilder.sm.add_user(
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    email='admin@admin.com',
                    role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                    password='admin'
                )
        logger.info("Database initialized successfully.")
        break
    except OperationalError:
        if i < attempts - 1:
            logger.warning("Database connection failed. Retrying in 5 seconds...")
            time.sleep(5)  # Wait 5 seconds before retrying
        else:
            logger.error("Could not connect to the database after multiple attempts.")
            raise

# View for the "Aluno" model in the admin panel
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'sobrenome', 'turma', 'disciplinas']

# Add the model view to AppBuilder
appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos",
)

@app.route('/metrics')
def metrics_endpoint():
    # Custom MariaDB metrics
    result = db.session.execute('SHOW STATUS LIKE "Threads_connected";').fetchone()
    threads_connected = result[1] if result else 0
    custom_metric = f"# TYPE mariadb_threads_connected gauge\nmariadb_threads_connected {threads_connected}\n"
    result = db.session.execute('SHOW STATUS LIKE "Queries";').fetchone()
    queries = result[1] if result else 0
    custom_metric += f"# TYPE mariadb_queries gauge\nmariadb_queries {queries}\n"

    # Combine default metrics and custom metrics
    default_metrics = generate_latest()  # Collect all default metrics, including Flask metrics
    combined_metrics = default_metrics + custom_metric.encode('utf-8')

    return Response(combined_metrics, mimetype=CONTENT_TYPE_LATEST)

# Increment the HTTP request counter on each request
@app.before_request
def increment_request_counter():
    http_request_counter.labels(method=request.method, endpoint=request.path).inc()

# Route to list all "Aluno" records - GET method
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'sobrenome': aluno.sobrenome, 'turma': aluno.turma, 'disciplinas': aluno.disciplinas} for aluno in alunos]
    return jsonify(output)

# Route to add a new "Aluno" record - POST method
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], turma=data['turma'], disciplinas=data['disciplinas'])
    db.session.add(novo_aluno)
    db.session.commit()
    logger.info(f"Aluno {data['nome']} {data['sobrenome']} added successfully!")
    return jsonify({'message': 'Aluno added successfully!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
