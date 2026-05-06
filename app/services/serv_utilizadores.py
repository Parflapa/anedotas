from app.models.rep_utilizadores import select_utilizadores_e_quantas_anedotas, select_nick_do_utilizador, validar_dados_de_login, insert_utilizador
from app.models.rep_anedotas import select_anedotas_por_utilizador
from app.utils.diversos import preview
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash


def listar_utilizadores():
    """Lista os utilizadores existentes e informa o número de anedotas dos mesmos

    Returns:
        _type_: _description_
    """    
    lista_utilizadores  = select_utilizadores_e_quantas_anedotas()
    return lista_utilizadores 



def listar_todas_anedotas_deste_utilizador(utilizador_id):
    """Devolve uma lista com 2 elementos:
            o nick do utilizador,
            as anedotas do utilizador

    Args:
        utilizador_id (int): id do utilizador

    Returns:
        [string: nick do utilizador,[Dict: "id","anedota","data","nick",""categoria]]: _description_
    """
    anedotas = select_anedotas_por_utilizador(utilizador_id)
    nick = select_nick_do_utilizador(utilizador_id)
    if anedotas:
        for anedota in anedotas:
            anedota['preview'] = preview(anedota['anedota'])
    
    resultado = {
        "utilizador"    : nick,
        "anedotas"      : anedotas,
        "mensagem"      : None if anedotas else f"Não há anedotas do utilizador {nick}",
    }
    return resultado





def validar_login(nick_ou_email, password):
    """
    Valida credenciais de login sem efeitos colaterais (stateless).

    Args:
        nick_ou_email (str): Nick ou email do utilizador.
        password (str): Password em texto simples.

    Returns:
        dict:
            {
                "sucesso": bool,
                "mensagem": str (opcional),
                "utilizador": dict (opcional)
            }
    """

    dados = validar_dados_de_login(nick_ou_email)

    if "mensagem" in dados:
        return {
            "sucesso": False,
            "mensagem": dados["mensagem"]
        }

    if check_password_hash(dados["password_u"], password):
        return {
            "sucesso": True,
            "utilizador": {
                "id": dados["id_u"],
                "nome": dados["nome_u"],
                "nick": dados["nick_u"],
                "email": dados["email_u"]
            }
        }

    return {
        "sucesso": False,
        "mensagem": "Password incorreta"
    }
        


def listar_passes():
    pCocas      = generate_password_hash("Cocas")
    pDevilOne   = generate_password_hash("DevilOne")
    pTia_Anica   = generate_password_hash("Tia_Anica")
    print(pCocas)
    print(pDevilOne)
    print(pTia_Anica)



def registar_utilizador(nome, email, nick, pais, password):
    password_encriptada = generate_password_hash(password)
    return insert_utilizador(nome, email, nick, pais, password_encriptada)




if __name__ == "__main__":
    pprint(registar_utilizador("Pedro", "lapa.pedro@gmail.com", "Adremek", "Portugal", "ABCDADOSFICTICIOS"))