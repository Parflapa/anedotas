from app.db import conectar_pymysql
from app.utils.datas import formatar_data_pt
from pprint import pprint


def select_todas_anedotas():
    """
    Seleciona todos os campos da tabela

    Returns:
        _type_: Dictionary
    """
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()

    try:
        query       = "SELECT * FROM anedotas ORDER BY data DESC"
        cursor.execute(query)
        resultado   = cursor.fetchall()
    except Exception as e:
        print(e)
        resultado = []
    finally:
        conexao.close()

    return resultado


def select_anedotas_por_categoria(categoria_id, limite=None):
    """
    Devolve as anedotas de uma categoria, incluindo dados do autor e categoria.

    Args:
        categoria_id (int): ID da categoria.
        limit (int, optional): Limite de resultados.

    Returns:
        list[dict]: "id","anedota","data","categoria", "nick" e "id_utilizador"
    """

    conexao = conectar_pymysql()
    cursor = conexao.cursor()

    sql = """
        SELECT 
            id_a AS id,
            texto_a AS anedota,
            data_a AS data,
            nome_c AS categoria,
            nick_u AS nick,
            id_u AS id_utilizador
        FROM anedotas
        LEFT JOIN categorias ON categoria_a = id_c
        LEFT JOIN utilizadores ON autor_a = id_u
        WHERE categoria_a = %s
        ORDER BY data DESC
    """

    params = [categoria_id]

    if limite is not None:
        sql += " LIMIT %s"
        params.append(limite)

    try:
        cursor.execute(sql, tuple(params))
        resultado = cursor.fetchall()
        for anedota in resultado:
            anedota['data'] = formatar_data_pt(anedota['data']) 
        return resultado

    except Exception as e:
        print(e)
        return []

    finally:
        cursor.close()
        conexao.close()


def select_anedotas_por_utilizador(utilizador_id, limite=None):
    """
    Devolve as anedotas de um utilizador, incluindo dados do autor e categoria.

    Args:
        categoria_id (int): ID da categoria.
        limit (int, optional): Limite de resultados.

    Returns:
        list[dict]: "id","anedota","data","categoria", "id_categoria" e "nick"
    """

    conexao = conectar_pymysql()
    cursor = conexao.cursor()

    sql = """
        SELECT 
            id_a AS id,
            texto_a AS anedota,
            data_a AS data,
            nome_c AS categoria,
            id_c AS id_categoria,
            nick_u AS nick
        FROM anedotas
        LEFT JOIN categorias ON categoria_a = id_c
        LEFT JOIN utilizadores ON autor_a = id_u
        WHERE autor_a = %s
        ORDER BY data DESC
    """

    params = [utilizador_id]

    if limite is not None:
        sql += " LIMIT %s"
        params.append(limite)

    try:
        cursor.execute(sql, tuple(params))
        resultado = cursor.fetchall()
        for anedota in resultado:
            anedota['data'] = formatar_data_pt(anedota['data']) 
        return resultado

    except Exception as e:
        print(e)
        return []

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def select_anedota_por_id(anedota_id):
    """ Pesquisa uma anedota pelo id e devolve todos os dados

    Args:
        anedota_id (int): _description_

    Returns:
        Dictionary: _description_
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()

    try:
        query   = """
        SELECT texto_a AS anedota, data_a AS data, nick_u AS nick, nome_c AS categoria 
        FROM anedotas 
        LEFT JOIN categorias ON categoria_a=id_c
        LEFT JOIN utilizadores ON autor_a=id_u
        WHERE id_a = %s"""
        cursor.execute(query,(anedota_id,))
        resultado   = cursor.fetchone()
    except Exception as e:
        print(e)
        resultado = []
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


    return resultado


def insert_anedota(autor, texto, categoria):
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()

    try:
        query   = """
        INSERT INTO anedotas (texto_a, data_a, autor_a, categoria_a)
        VALUES (%s,CURDATE(),%s,%s)
        """
        cursor.execute(query,(texto, autor, categoria))
        conexao.commit()
        return True
    except Exception as e:
        print(e)
        conexao.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


if __name__ == "__main__":
    pprint(select_anedota_por_id(1))