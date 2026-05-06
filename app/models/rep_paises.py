from app.db import conectar_pymysql

def select_paises():
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    query       = "SELECT id_p AS id, nome_p AS nome FROM paises"

    try:
        cursor.execute(query)
        resultado   = cursor.fetchall()
        return resultado
    except Exception as e:
        print(e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()  