from app.db import conectar_pymysql
from pprint import pprint

def select_todas_categorias():
    """Lista todas as categorias

    Returns:
        _type_: _description_
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    query       = "SELECT * FROM categorias"
    
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


def select_categorias_e_quantas_anedotas():
    """
    Lista os nomes das categorias e quantas anedotas cada uma delas tem

    Returns:
        list[dict]: Lista de categorias com o seguinte formato:
        {
            "id": str,              # id da categoria
            "nome": str,            # nome da categoria
            "total_anedotas": int   # número de anedotas associadas
        }
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    sql         = """ 
                SELECT 
                    c.id_c AS id,
                    c.nome_c AS nome,
                    COUNT(a.id_a) AS total_anedotas
                FROM categorias AS c
                LEFT JOIN anedotas AS a 
                    ON a.categoria_a = c.id_c
                GROUP BY 
                    c.id_c, c.nome_c
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


def select_nome_da_categoria(categoria_id):
    """Devolve o nome de uma categoria

    Returns:
        string: nome da categoria
    """    
    conexao     = conectar_pymysql()
    cursor      = conexao.cursor()
    query       = "SELECT nome_c FROM categorias WHERE id_c = %s"

    try:
        cursor.execute(query,(categoria_id,))
        resultado = cursor.fetchone()
    except Exception as e:
        print(e)
        return "Categoria não encontrada"
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
   
    return resultado['nome_c']     # type:ignore


if __name__ == "__main__":
    pprint(select_nome_da_categoria(1))