from dotenv import load_dotenv
import os
import pymysql           # type:ignore
# import mysql.connector


local = r"C:\xampp\credenciais\crd_anedotas.env"
prod = "/var/www/vhosts/websis.pt/credenciais/crd_anedotas.env"
if os.path.exists(local):
    load_dotenv(local)
else:
    load_dotenv(prod)



def conectar_pymysql():
    conexao = pymysql.connect(
        host        = str(os.getenv("DB_HOST")),
        user        = str(os.getenv("DB_USER")),
        password    = str(os.getenv("DB_PASSWORD")),
        database    = str(os.getenv("DB_NAME")),
        autocommit  = False,
        cursorclass = pymysql.cursors.DictCursor
    )
    return conexao



""" def conectar_connector():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rentacar",
        autocommit=False,  # importante mas desnecessário pq é o valor default em caso de não referência
    )
 """

