# Aula 11 - Cookies

from flask import Flask, render_template, request, make_response

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/setcookie', methods=['GET','POST'])
def setcookie():
   resp = make_response(render_template('setcookie.html'))
   if request.method == 'POST':
      dados = request.form['c']
      resp.set_cookie('testeCookie', dados)
   
   return resp

@app.route('/getcookie')
def getcookie():
   cookie_name = request.cookies.get('testeCookie')
   return '<h1>Valor do cookie é: {} </h1>'.format(cookie_name)
      
      
if __name__ == '__main__':
    app.run(debug=True)
