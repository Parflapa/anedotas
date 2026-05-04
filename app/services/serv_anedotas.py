from app.models.rep_anedotas import select_todas_anedotas, select_anedotas_por_categoria,select_anedota_por_id, select_anedotas_por_utilizador, insert_anedota, update_anedota, delete_anedota, update_anedota_add_voto, update_anedota_add_visualizacao, select_anedota_aleatoria
from app.models.rep_categorias import select_categorias_e_quantas_anedotas
from app.utils.datas import formatar_data_pt
from app.utils.diversos import  preview
from pprint import pprint

def listar_anedotas(tipo="atual"):
    """
    Lista anedotas com preview 
    Argument: top (lista anedotas mais recentes ou lista de anedotas mais votadas - TOP)

    Returns:
        List[Dictionary]
    """
    lista_anedotas  = select_todas_anedotas(tipo)
    lista_final     = [] 
    for anedota in lista_anedotas:
        resultado                   = {}
        resultado['anedota_id']     = anedota['id_a']
        resultado['anedota']        = anedota['texto_a']
        resultado['preview']        = anedota['texto_a'][0:40] + "..."
        resultado['utilizador']     = anedota['nick_u']
        resultado['utilizador_id']  = anedota['utilizador_a']
        resultado['categoria']      = anedota['nome_c']
        resultado['categoria_id']   = anedota['categoria_a'] 
        resultado['visualizacoes']  = anedota['visualizacoes_a'] 
        resultado['votos']          = anedota['votos_a']      
        resultado['data']           = formatar_data_pt(anedota['data_a'])
        lista_final.append(resultado)

    return lista_final



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


def votar_nesta_anedota(id):
    return update_anedota_add_voto(id)


def mais_uma_visualizacao_nesta_anedota(id):
    #return update_anedota_add_visualizacao(id)
    update_anedota_add_visualizacao(id)


def anedota_aleatoria():
    id_aleatorio = select_anedota_aleatoria()
    detalhes = detalhes_da_anedota(id_aleatorio)
    return detalhes



# para debug
if __name__ == "__main__":
    pprint(anedota_aleatoria())