import requests
import json


FRESHDESK_DOMAIN = 'int6tech.freshdesk.com'


STATUSES_PERMITIDOS = [2, 3]
TIPO_ESPERADO = "Suporte / Manutenção a CPEs já homologados"

MENSAGEM_AUTOMATICA_HTML = """
<p>Olá!</p>
<p>Para prosseguirmos com o chamado de manutenção, precisamos de algumas informações!</p>
<br>
<p><strong>Qual seria exatamente o erro? (Se houver)</strong><br>
<ul>
    <li>Teria Print dos casos com problema?</li>
    <li>Qual seria o comportamento esperado?</li>
    <li>Teria um contrato de exemplo onde ocorreu o problema?</li>
<ul>   
<p><strong>Em caso de melhoria:</strong></p>
<ul>
    <li>Teria print de como está sendo feito atualmente e o que deveria mudar?</li>
    <li>Poderia descrever exatamente o que precisa ser feito?</li>
</ul>
<p>Aguardamos essas informações para dar andamento.<br>
Atenciosamente.</p>
"""



def executar_manutencao(ticket_id: str, api_key: str):
    """
    Verifica um ticket no Freshdesk e, se os critérios forem atendidos, envia uma resposta automática.
    """
    print(f"--- INICIANDO SCRIPT DE MANUTENÇÃO PARA O TICKET {ticket_id} ---")

    try:
        url_get_ticket = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}"
        print(f"Buscando informações em: {url_get_ticket}")


        response = requests.get(url_get_ticket, auth=(api_key, 'X'))
        response.raise_for_status()

        ticket_data = response.json()
        ticket_status_code = ticket_data.get('status')
        ticket_type = ticket_data.get('type')

        print(f"-> Status recebido: {ticket_status_code} | Tipo recebido: '{ticket_type}'")

        if ticket_status_code in STATUSES_PERMITIDOS and ticket_type == TIPO_ESPERADO:
            print("[✓] Critérios atendidos. Preparando para enviar resposta...")

            url_reply = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}/reply"
            headers = {'Content-Type': 'application/json'}
            payload = {'body': MENSAGEM_AUTOMATICA_HTML}


            reply_response = requests.post(url_reply, auth=(api_key, 'X'), headers=headers, data=json.dumps(payload))
            reply_response.raise_for_status()

            mensagem_sucesso = f"SUCESSO! Resposta automática enviada para o ticket #{ticket_id}."
            print(mensagem_sucesso)
            return (True, mensagem_sucesso)

        else:
            mensagem_aviso = f"O ticket #{ticket_id} não atende aos critérios para resposta. Nenhuma ação foi tomada."
            print(f"[X] {mensagem_aviso}")
            return (False, mensagem_aviso)

    except requests.exceptions.HTTPError as http_err:
        mensagem_erro = f"ERRO DE HTTP: {http_err}. Verifique o ID do ticket ou a chave de API."
        print(mensagem_erro)
        return (False, mensagem_erro)

    except Exception as e:
        mensagem_erro = f"ERRO INESPERADO: {e}"
        print(mensagem_erro)
        return (False, mensagem_erro)