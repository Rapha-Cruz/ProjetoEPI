from flask import Flask, request, jsonify, Blueprint
from conexao import criar_conexao, fechar_conexao

epi_bp = Blueprint('epi', __name__)

#lista todos as EPIs do banco
@epi_bp.route('/listar', methods=['GET'])
def listar_epi():
    #conectar com o banco de dados
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM epi ORDER BY DATA_VENCIMENTO DESC")
    epi = cursor.fetchall()

    #fechar conexão com banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify(epi)

#criar um epi novo
@epi_bp.route('/novoepi', methods=['POST'])
def criar_epi():
    data = request.json
    NOME_EPI = data['NOME_EPI']
    INSTRUCAO_EPI = data['INSTRUCAO_EPI']
    DATA_ENTREGA = data['DATA_ENTREGA']
    DATA_VENCIMENTO = data['DATA_VENCIMENTO']
    ID_FUNCIONARIO = data['ID_FUNCIONARIO']

    #conectar com o banco
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO epi (NOME_EPI, INSTRUCAO_EPI, DATA_ENTREGA, DATA_VENCIMENTO, ID_FUNCIONARIO)"
                   "VALUES (%s, %s, %s, %s, %s)",
                   (NOME_EPI, INSTRUCAO_EPI, DATA_ENTREGA, DATA_VENCIMENTO, ID_FUNCIONARIO))
    conn.commit()

    #fechar a conexao com o banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "EPI criado com sucesso"})

#atualizar um livro pelo ID
@epi_bp.route('/<int:id>', methods=['PUT'])
def atualizar_epi(id):
    data = request.get_json()
    NOME_EPI = data['NOME_EPI']
    INSTRUCAO_EPI = data['INSTRUCAO_EPI']
    DATA_ENTREGA = data['DATA_ENTREGA']
    DATA_VENCIMENTO = data['DATA_VENCIMENTO']
    ID_FUNCIONARIO = data['ID_FUNCIONARIO']

    conn = criar_conexao()
    cursor = conn.cursor()

    sql = "UPDATE epi SET NOME_EPI = %s, INSTRUCAO_EPI = %s, DATA_ENTREGA = %s, DATA_VENCIMENTO = %s, ID_FUNCIONARIO = %s WHERE id_epi = %s"
    valores = (NOME_EPI, INSTRUCAO_EPI, DATA_ENTREGA, DATA_VENCIMENTO, ID_FUNCIONARIO, id)

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "EPI atualizado com sucesso"}), 200

#deletar epi
@epi_bp.route('/<int:id_epi>', methods=['DELETE'])
def deletar_epi(id_epi):
    conn = criar_conexao()
    cursor = conn.cursor()

    sql = "DELETE FROM epi WHERE id_epi = %s"
    valores = (id_epi, )

    try :
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"mensagem":"EPI deletado"}), 200
    
    except Exception as err:
        conn.rollback()
        return jsonify({"erro": f"Erro ao deletar o EPI: {err}"}), 500

    finally: 
        cursor.close()
        fechar_conexao(conn)