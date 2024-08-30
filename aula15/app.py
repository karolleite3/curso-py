# Aula 15 - Rest API parte 1
from flask import Flask, render_template, request, url_for, redirect, Response
from models import db, Estudante
import json
from sqlalchemy import text

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite3'


db.init_app(app=app)


@app.route('/')
def index():
  # estudantes = Estudante.query.all()
   #result = [e.to_dict() for e in estudantes]
   query = text('SELECT * FROM estudante')
   result = db.session.execute(query).fetchall()
   
   result_dict = [dict(zip(['id', 'nome', 'idade'], row)) for row in result]
   return Response(response=json.dumps(result_dict), status=200, content_type="application/json")


@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    # Use parâmetros vinculados para a consulta SQL
    query = text('SELECT * FROM estudante WHERE id = :id')
    result = db.session.execute(query, {'id': id}).fetchone()
    
    # Verifique se o resultado não é None
    if result:
        result_dict = dict(zip(['id', 'nome', 'idade'], result))
        return Response(response=json.dumps(result_dict), status=200, content_type="application/json")
    else:
        return Response(response=json.dumps({'error': 'Estudante não encontrado'}), status=404, content_type="application/json")


@app.route('/add', methods=['POST'])
def add():
   estudante = Estudante(request.form['nome'], request.form['idade'])
   db.session.add(estudante)
   db.session.commit()
   return app.response_class(response=json.dumps({'status': 'sucess', 'data': estudante.to_dict()}), status=200, content_type="application/json")


@app.route('/edit/<int:id>', methods=['PUT', 'POST'])
def edit(id):
   estudante = Estudante.query.get(id)
   estudante.nome = request.form['nome']
   estudante.idade = request.form['idade']
   db.session.commit()
   return Response(response=json.dumps(estudante.to_dict()), status=200, content_type="application/json")


@app.route('/delete/<int:id>', methods=['DELETE', 'POST'])
def delete(id):
   estudante = Estudante.query.get(id)
   db.session.delete(estudante)
   db.session.commit()
   return Response(response=json.dumps(estudante.to_dict()), status=200, content_type="application/json")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco de dados e tabelas criados com sucesso!")
    app.run(debug=True)