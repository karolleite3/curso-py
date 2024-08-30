from flask import Blueprint, Response, request
from models.models import db,  Disciplina
import json

app = Blueprint("disciplinas", __name__)

@app.route('/')
def index():
   query = db.text('SELECT * FROM disciplina')
   result = db.session.execute(query).fetchall()
   
   result_dict = [dict(zip(['id', 'nome'], row)) for row in result]
   return Response(response=json.dumps(result_dict), status=200, content_type="application/json")


@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    # Use parâmetros vinculados para a consulta SQL
    query = db.text('SELECT * FROM disciplina WHERE id = :id')
    result = db.session.execute(query, {'id': id}).fetchone()
    
    # Verifique se o resultado não é None
    if result:
        result_dict = dict(zip(['id', 'nome'], result))
        return Response(response=json.dumps(result_dict), status=200, content_type="application/json")
    else:
        return Response(response=json.dumps({'error': 'Estudante não encontrado'}), status=404, content_type="application/json")


@app.route('/add', methods=['POST'])
def add():
   disciplina = Disciplina(request.form['nome'])
   db.session.add(disciplina)
   db.session.commit()
   return Response(response=json.dumps({'status': 'sucess', 'data': disciplina.to_dict()}), status=200, content_type="application/json")


@app.route('/edit/<int:id>', methods=['PUT', 'POST'])
def edit(id):
   disciplina = Disciplina.query.get(id)
   disciplina.nome = request.form['nome']
   db.session.commit()
   return Response(response=json.dumps(disciplina.to_dict()), status=200, content_type="application/json")


@app.route('/delete/<int:id>', methods=['DELETE', 'POST'])
def delete(id):
   disciplina = Disciplina.query.get(id)
   db.session.delete(disciplina)
   db.session.commit()
   return Response(response=json.dumps(disciplina.to_dict()), status=200, content_type="application/json")
