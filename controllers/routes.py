from flask import render_template, request, url_for, redirect, flash
from models.database import db, Images  # Corrigido o import
import urllib
import json
import os
import uuid

def init_app(app):
    
    # Definindo tipos de arquivos permitidos para upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    # Rota Home
    @app.route('/', methods=['GET', 'POST'])
    def home():
        # Seleciona todas as imagens no banco
        images = Images.query.all()
        
        if request.method == 'POST':
            # Verifica se o arquivo foi enviado
            if 'file' not in request.files:
                flash('Nenhum arquivo selecionado.', 'danger')
                return redirect(url_for('home'))
            
            file = request.files['file']
            
            # Verifica se o arquivo tem nome
            if file.filename == '':
                flash('Nenhum arquivo selecionado.', 'danger')
                return redirect(url_for('home'))
            
            # Verifica se o tipo de arquivo é permitido
            if not allowed_file(file.filename):
                flash('Tipo de arquivo não permitido.', 'danger')
                return redirect(url_for('home'))
            
            # Obtém a extensão do arquivo
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            
            # Gerar nome único preservando a extensão
            filename = f"{str(uuid.uuid4())}.{file_ext}"
            
            # Gravando a imagem no banco (corrigido)
            img = Images(url=filename, alt=filename)  # Você pode ajustar o 'alt'
            db.session.add(img)
            db.session.commit()
            
            # Gravando o arquivo na pasta uploads (sintaxe corrigida)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Imagem enviada com sucesso!', 'success')
            return redirect(url_for('home'))
            
        return render_template('index.html', images=images)