from flask import Flask, request, jsonify, Blueprint
from conexao import criar_conexao, fechar_conexao
from hashlib import sha256

funcionarios_bp = Blueprint('funcionarios', __name__)

# criar um usuario novo
@funcionarios_bp.route('/novofuncionario', methods=['POST'])
def criar_funcionario():
    data = request.json
    NOME = data['NOME'] 
    LOGIN = data['LOGIN']
    SENHA = data['SENHA']
    CARGO = data['CARGO']
    
    #criptografa a senha
    senhaCripto = sha256(SENHA.encode('utf-8')).hexdigest()

    #conectar com o banco
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO funcionario (NOME, LOGIN, SENHA, CARGO)"
                   "VALUES (%s, %s, %s, %s)",
                  (NOME, LOGIN, senhaCripto, CARGO))
    conn.commit()
    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem":"Funcionário criado com sucesso" }), 200

#logar
@funcionarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.json
    LOGIN = data['LOGIN']
    SENHA = data['SENHA']

    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT SENHA, NOME, CARGO, ID_FUNCIONARIO FROM funcionario WHERE LOGIN = %s",
                  (LOGIN,))      

    senhaBanco = cursor.fetchone()    

    if checar_senha(senhaBanco['SENHA'], SENHA):
        cursor.close()
        fechar_conexao(conn)

        return jsonify({'ID_FUNCIONARIO': senhaBanco['ID_FUNCIONARIO'], 'Nome': senhaBanco['NOME'], 'Cargo': senhaBanco['CARGO']})
    
    else :
        cursor.close()
        fechar_conexao(conn)

        return jsonify({"mensagem": "Login Incorreto"})
    
    #verificar a senha
def checar_senha(senhaBanco, senha):
        senha_convertida = sha256(senha.encode('utf-8')).hexdigest()
        return senhaBanco == senha_convertida

#lista todos as EPIs do banco
@funcionarios_bp.route('/listar', methods=['GET'])
def listar_funcionario():
    #conectar com o banco de dados
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM funcionario")
    funcionario = cursor.fetchall()

    #fechar conexão com banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify(funcionario)