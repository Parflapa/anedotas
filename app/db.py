# import mysql.connector
import pymysql              # type:ignore

""" def conectar_connector():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rentacar",
        autocommit=False,  # importante mas desnecessário pq é o valor default em caso de não referência
    )
 """

def conectar_pymysql():
    conexao =  pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="anedotas",
        autocommit=False,  # importante
        cursorclass=pymysql.cursors.DictCursor  # dicionário
    )
    return conexao