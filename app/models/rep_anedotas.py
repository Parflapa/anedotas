from app.db import conectar_pymysql
from app.utils.datas import formatar_data_pt
from pprint import pprint
import random


def select_todas_anedotas(tipo="atual"):
    """
    Seleciona todos os campos da tabela

    Returns:
        _type_: Dictionary
    """
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    if tipo == "atual":
        order_by = "data_a DESC"
    elif tipo == "top":
        order_by = "votos_a DESC"
    elif tipo == "visualizacoes":
        order_by = "visualizacoes_a DESC"
    else:
        order_by = "data_a DESC"

    query       = f"""
                    SELECT * FROM anedotas
                    LEFT JOIN utilizadores ON utilizador_a=id_u
                    LEFT JOIN categorias ON categoria_a=id_c
                    ORDER BY {order_by}
                """

    try:
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
        LEFT JOIN utilizadores ON utilizador_a = id_u
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
        LEFT JOIN utilizadores ON utilizador_a = id_u
        WHERE utilizador_a = %s
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
        SELECT id_a AS anedota_id, texto_a AS anedota, data_a AS data, nick_u AS nick, id_u AS utilizador_id, nome_c AS categoria, id_c AS categoria_id, visualizacoes_a AS visualizacoes, votos_a AS votos 
        FROM anedotas 
        LEFT JOIN categorias ON categoria_a=id_c
        LEFT JOIN utilizadores ON utilizador_a=id_u
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
        INSERT INTO anedotas (texto_a, data_a, utilizador_a, categoria_a)
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


def update_anedota(id, texto, categoria):
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    try:
        query   = """
        UPDATE anedotas 
        SET texto_a=%s, data_a=CURDATE(), categoria_a=%s 
        WHERE id_a=%s
        """
        cursor.execute(query,(texto, categoria, id))
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



def delete_anedota(id):
    conexao = conectar_pymysql()
    cursor = conexao.cursor()
    try:
        query = """
        DELETE FROM anedotas 
        WHERE id_a = %s
        """
        cursor.execute(query, (id,))
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


def update_anedota_add_visualizacao(id):
    conexao = conectar_pymysql()
    cursor = conexao.cursor()
    try:
        query = """
        UPDATE anedotas
        SET visualizacoes_a = visualizacoes_a + 1
        WHERE id_a = %s;
        """
        cursor.execute(query, (id,))
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


def update_anedota_add_voto(id):
    conexao = conectar_pymysql()
    cursor = conexao.cursor()
    try:
        query = """
        UPDATE anedotas
        SET votos_a = votos_a + 1
        WHERE id_a = %s;
        """
        cursor.execute(query, (id,))
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


def select_anedota_aleatoria():
    conexao = conectar_pymysql()
    cursor = conexao.cursor()
    # 1. total
    query = "SELECT COUNT(*) AS contagem FROM anedotas;"
    cursor.execute(query)
    resultado = cursor.fetchone()
    contagem = resultado['contagem'] if resultado else 0

    # 2. offset aleatório (em Python)
    offset = random.randint(0, contagem-1)

    # 3. query
    query = """SELECT id_a FROM anedotas
    LIMIT 1 OFFSET %s;
    """
    cursor.execute(query,(offset,))

    anedota_aleatoria = cursor.fetchone()

    id_aleatorio = anedota_aleatoria['id_a']          # type: ignore

    return id_aleatorio



if __name__ == "__main__":
    pprint(select_anedota_por_id(1))