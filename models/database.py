from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    alt = db.Column(db.String(150))
    
    def __init__(self, url, alt):
        self.url = url
        self.alt = alt