from flask import Flask
from flask_cors import CORS
from rotas.rota_epi import epi_bp
from rotas.rota_funcionario import funcionarios_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(epi_bp, url_prefix='/epi')
app.register_blueprint(funcionarios_bp, url_prefix='/funcionario')

#executar a API
if __name__ == "__main__":
    #app.run(port=5000, host='localhost', debug=True)
    app.run()