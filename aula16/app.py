# Aula 16 - REST API parte 2
from flask import Flask
from models.models import db
from controllers.estudante import app as estudante_controller
from controllers.disciplina import app as disciplina_controller


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite3'

app.register_blueprint(estudante_controller, url_prefix="/estudante/")
app.register_blueprint(disciplina_controller, url_prefix="/disciplina/")

db.init_app(app=app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco de dados e tabelas criados com sucesso!")
    app.run(debug=True)