#pip install mysql-connector-python
import mysql.connector

#configuração do banco de dados
def criar_conexao():
    return mysql.connector.connect(
        host = "sql10.freesqldatabase.com",
        user = "sql10710319",
        password = "P3vDcbBSDn",
        database = "sql10710319"
    )

def fechar_conexao(conexao):
    if conexao:
            conexao.close()