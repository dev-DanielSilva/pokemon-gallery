from flask import Flask
from models.database import db
import os

app = Flask(__name__, template_folder='views')

# Permite ler o diretório absoluto de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Secret para as flash messages
app.config['SECRET_KEY'] = 'pokemongallerysecretkey'
# Define o tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
# Define pasta que receberá arquivos de upload (caminho absoluto)
app.config['UPLOAD_FOLDER'] = os.path.join(dir, 'static', 'uploads')
# Define o tamanho máximo de um arquivo de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

# Import e inicialização das rotas DEPOIS da configuração do app
# ESCOLHA APENAS UMA DAS OPÇÕES ABAIXO:

# OPÇÃO 1: Se routes.py está na pasta controllers
from controllers.routes import init_app

# OPÇÃO 2: Se routes.py está na raiz (comente a linha acima e use esta)
# from routes import init_app

init_app(app)

def create_upload_folder():
    """Cria a pasta de uploads se não existir"""
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Pasta de uploads criada: {upload_folder}")

if __name__ == '__main__':
    with app.app_context():
        # Cria a pasta de uploads
        create_upload_folder()
        
        # Cria todas as tabelas do banco de dados
        db.create_all()
        print("Banco de dados inicializado!")
    
    app.run(host='localhost', port=5000, debug=True)