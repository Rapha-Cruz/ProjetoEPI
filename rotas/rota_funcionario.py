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

#atualizar um livro pelo ID
@funcionarios_bp.route('/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    data = request.get_json()
    NOME = data['NOME']
    CARGO = data['CARGO']
    LOGIN = data['LOGIN']
    SENHA = data['SENHA']
    
    #criptografa a senha
    senhaCripto = sha256(SENHA.encode('utf-8')).hexdigest()

    conn = criar_conexao()
    cursor = conn.cursor()

    sql = "UPDATE funcionario SET NOME = %s, CARGO = %s, LOGIN = %s, SENHA = %s WHERE id_FUNCIONARIO = %s"
    valores = (NOME, CARGO, LOGIN, senhaCripto, id)

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "Funcionário atualizado com sucesso"}), 200

#deletar epi
@funcionarios_bp.route('/<int:id_epi>', methods=['DELETE'])
def deletar_epi(id_funcionario):
    conn = criar_conexao()
    cursor = conn.cursor()

    sql = "DELETE FROM funcionario WHERE id_funcionario = %s"
    valores = (id_funcionario, )

    try :
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"mensagem":"Funcionário deletado"}), 200
    
    except Exception as err:
        conn.rollback()
        return jsonify({"erro": f"Erro ao deletar o Funcionário: {err}"}), 500

    finally: 
        cursor.close()
        fechar_conexao(conn)