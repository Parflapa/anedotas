from app.models.rep_categorias import select_categorias_e_quantas_anedotas, select_nome_da_categoria, insert_categoria, update_categoria, delete_categoria, select_categoria_por_id
from app.models.rep_anedotas import select_anedotas_por_categoria
from app.utils.diversos import  preview
from pprint import pprint

def listar_categorias():
    """Lista as categorias existentes e informa o número de anedotas da mesma

    Returns:
        _type_: _description_
    """    
    lista_categorias  = select_categorias_e_quantas_anedotas()
    return lista_categorias 


def dados_da_categoria(id):
    return select_categoria_por_id(id)


def listar_todas_anedotas_desta_categoria(categoria_id):
    """Devolve uma lista com elementos:
            o nome, e o id da categoria,
            as anedotas da categoria,
            em caso de erro: uma mensagem ou None

    Args:
        categoria_id (int): id da categoria

    Returns:
        [string: nome da categoria,[Dict: "id","anedota","data","nick",""categoria]]: _description_
    """
    anedotas = select_anedotas_por_categoria(categoria_id)
    categoria_nome = select_nome_da_categoria(categoria_id)
    if anedotas:
        for anedota in anedotas:
            anedota['preview'] = preview(anedota['anedota'])
    
    resultado = {
        "categoria"     : categoria_nome,
        "categoria_id"  : categoria_id,
        "mensagem"      : None if anedotas else f"Não há anedotas da categoria {categoria_nome}",
        "anedotas"      : anedotas,
    }
    return resultado


def adicionar_categoria(nome):
    return insert_categoria(nome)



def editar_categoria(id,nome):
    return update_categoria(id,nome)


def eliminar_categoria(id):
    return delete_categoria(id)





if __name__ == "__main__":
    pprint(dados_da_categoria(1))