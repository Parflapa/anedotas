from app.models.rep_anedotas import select_todas_anedotas, select_anedotas_por_categoria,select_anedota_por_id, select_anedotas_por_utilizador, insert_anedota, update_anedota, delete_anedota
from app.models.rep_categorias import select_categorias_e_quantas_anedotas
from app.utils.datas import formatar_data_pt
from app.utils.diversos import  preview
from pprint import pprint

def listar_anedotas():
    """
    Lista anedotas com preview

    Returns:
        List[Dictionary]
    """
    lista_anedotas  = select_todas_anedotas()
    resultado       = {}
    for anedota in lista_anedotas:
        preview = anedota['texto_a'][0:40] + "..."
        resultado['anedota'] = anedota['texto_a']
        resultado['preview'] = preview

    return resultado



def listar_anedotas_por_categoria(id_categoria,quantasAnedotas=None):
    lista_anedotas  = select_anedotas_por_categoria(id_categoria,quantasAnedotas)
    for anedota in lista_anedotas:
        anedota['preview'] = preview(anedota['anedota'])
        #pprint(anedota)

    #pprint(lista_anedotas)
    return lista_anedotas



def listar_anedotas_por_utilizador(id_utilizador,quantasAnedotas=None):
    lista_anedotas  = select_anedotas_por_utilizador(id_utilizador,quantasAnedotas)
    for anedota in lista_anedotas:
        anedota['preview'] = preview(anedota['anedota'])
        #pprint(anedota)

    #pprint(lista_anedotas)
    return lista_anedotas



def dash_board_categorias_anedotas():
    """
    Devolve uma estrutura agregada com categorias e as respetivas anedotas.

    Para cada categoria existente na base de dados, inclui:
    - identificação da categoria
    - nome da categoria
    - total de anedotas associadas
    - lista detalhada das anedotas pertencentes à categoria

    Returns:
        list[dict]: Lista de categorias enriquecida com as suas anedotas,
        no seguinte formato:
        {
            "id": int,                # ID da categoria
            "nome": str,              # nome da categoria
            "total_anedotas": int,    # número total de anedotas na categoria
            "anedotas": list[dict]    [{"id:int,"anedota":str,"preview":str,"categoria":str,"data":str,"nick":str}]
        }
    """
    # Escolher quantas anedotas por categoria na HomePage
    quantas_anedotas_por_categoria = 2
    categorias = select_categorias_e_quantas_anedotas()
    for c in categorias:
        anedotas_da_categoria = listar_anedotas_por_categoria(c['id'],quantas_anedotas_por_categoria)
        c['anedotas']  = anedotas_da_categoria
    return categorias



def detalhes_da_anedota(anedota_id):
    detalhes = select_anedota_por_id(anedota_id)
    detalhes['data'] = formatar_data_pt(detalhes['data'])       # type:ignore
    return detalhes



def adicionar_anedota(utilizador,texto,categoria):
    return insert_anedota(utilizador,texto,categoria)



def editar_anedota(id,texto,categoria):
    return update_anedota(id,texto,categoria)


def eliminar_anedota(id):
    return delete_anedota(id)


# para debug
if __name__ == "__main__":
    pprint(detalhes_da_anedota(7))