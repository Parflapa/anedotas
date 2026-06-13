from app.models.rep_utilizadores import select_utilizadores_e_quantas_anedotas, select_nick_do_utilizador, validar_dados_de_login, insert_utilizador, update_confirmar_registo, select_user_por_email
from app.models.rep_anedotas import select_anedotas_por_utilizador
from app.utils.diversos import preview
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

from flask import url_for, current_app
from flask_mail import Message
from app.utils.extensoes import mail
from itsdangerous import URLSafeTimedSerializer
import logging


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
                "email": dados["email_u"],
                "nivel": dados["nivel_u"]
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
    try:
        password_encriptada = generate_password_hash(password)
        insercao = insert_utilizador(nome, email, nick, pais, password_encriptada, 1)
        
        if insercao:
            # logging.info(f"Utilizador registado com sucesso: {email}")
            enviar_email_confirmacao(email)
            # logging.info(f"Email de confirmação enviado: {email}")
            return True
        else:
            logging.warning(f"Falha ao registar utilizador (insert_utilizador=False): {email}")
            return False

    except Exception as e:
        logging.error(
            f"Erro inesperado ao registar utilizador: {email} - {str(e)}",
            exc_info=True
        )
        return False
    


def confirmar_registo(email):
    return update_confirmar_registo(email)



def enviar_email_confirmacao(user_email):
    # criar um objeto serializer da biblioteca itsdangerous (criar tokens assinados, validar tokens, definir tempo de expiração)
    # usa internamente a chave secreta Flask que assina criptograficamente o token e impede alguém de fabricar tokens falsos 
    # sem a SECRET_KEY correta o token não pode ser validado.
    # O que é URLSafeTimedSerializer: URLSafe (token é seguro para usar num URL: sem espaços, sem caracteres problemáticos, próprio para links de email)
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    dados_para_token = {
        'email' : user_email
    }
    token = s.dumps(dados_para_token, salt='confirmar-email')
    url = url_for('utilizadores.confirmacao', token=token, _external=True)

    with open('app/templates/email_confirmacao.html') as f:
        html = f.read().replace('{{ url_confirmacao | safe }}', url)

    msg = Message(
        'Confirma a tua conta',
        recipients=[user_email])
    msg.html = html
    mail.send(msg)



def verificar_se_email_ja_esta_registado(email):
    return select_user_por_email(email)




if __name__ == "__main__":
    pprint(registar_utilizador("Pedro", "lapa.pedro@gmail.com", "Adremek", "Portugal", "ABCDADOSFICTICIOS"))