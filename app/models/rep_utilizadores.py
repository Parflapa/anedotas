from app.db import conectar_pymysql
from pprint import pprint


def select_todos_utilizadores():
    """Lista todos os utilizadores

    Returns:
        _type_: _description_
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    query       = "SELECT * FROM utilizadores"
    
    try:
        cursor.execute(query)
        resultado   = cursor.fetchall()
    except Exception as e:
        print(e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()    

    return resultado


def select_utilizadores_e_quantas_anedotas():
    """
    Lista os utilizadores e quantas anedotas cada um deles tem

    Returns:
        list[dict]: Lista de utilizadores com o seguinte formato:
        {
            "id": str,              # id da utilizador
            "nome": str,            # nome da utilizador
            "nick": str,            # nick da utilizador
            "total_anedotas": int   # número de anedotas associadas
        }
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    sql         = """ 
                SELECT 
                    u.id_u AS id,
                    u.nome_u AS nome,
                    u.nick AS nick
                    COUNT(a.id_a) AS total_anedotas
                FROM utilizadores AS u
                LEFT JOIN anedotas AS a 
                    ON a.utilizador_a = u.id_u
                GROUP BY 
                    u.id_u, u.nome_u
                ORDER BY 
                    total_anedotas DESC; """
    
    try:
        cursor.execute(sql)
        resultado   = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    return resultado


def select_nick_do_utilizador(utilizador_id):
    """Devolve o nome e nick de um utilizador

    Returns:
        string: o nick do utilizador
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    query       = "SELECT nick_u FROM utilizadores WHERE id_u = %s"

    try:
        cursor.execute(query,(utilizador_id,))
        resultado = cursor.fetchone()
    except Exception as e:
        print(e)
        return "Utilizador não encontrado"
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
   
    return resultado['nick_u']     # type:ignore


def validar_dados_de_login(nick_ou_email):
    """
    Obtém os dados de um utilizador a partir do nick ou email.
    Returns:
        dict:{"id_u": int, "nome_u": str, "nick_u": str, "email_u": str, "password_u": str}
        ou {"mensagem": str}
    """

    conexao = conectar_pymysql()
    cursor = conexao.cursor()

    query = """
        SELECT id_u, nome_u, nick_u, email_u, password_u
        FROM utilizadores
        WHERE nick_u = %s OR email_u = %s
    """

    try:
        cursor.execute(query, (nick_ou_email, nick_ou_email))
        resultado = cursor.fetchone()

        if not resultado:
            return {"mensagem": "O utilizador não foi encontrado"}

        return {
            "id_u": resultado["id_u"],
            "nome_u": resultado["nome_u"],
            "nick_u": resultado["nick_u"],
            "email_u": resultado["email_u"],
            "password_u": resultado["password_u"]
        }
    except Exception as e:
        return {
            "mensagem": "Erro na base de dados.",
            "erro": str(e)
        }
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()



def insert_utilizador(nome, email, nick, pais, password):
    conexao = conectar_pymysql()
    cursor  = conexao.cursor()

    try:
        query = "INSERT INTO utilizadores (nome_u, email_u, nick_u, pais_u, password_u) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(nome, email, nick, pais, password))
        conexao.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    



if __name__ == "__main__":
    pprint(select_todos_utilizadores())