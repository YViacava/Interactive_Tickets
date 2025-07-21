import requests
import json


FRESHDESK_DOMAIN = 'int6tech.freshdesk.com'


STATUSES_PERMITIDOS = [2, 3]
TIPO_ESPERADO = "Suporte para novo fabricante/modelo de ONU/firmware"

MENSAGEM_AUTOMATICA_HTML = """
<p>Olá!</p>
<p>Para prosseguirmos com o chamado de homologação, precisamos de algumas informações!</p>
<br>
<p><strong>Sobre a bancada:</strong><br>
    <li><strong>IP:</strong></li>
    <li><strong>Usuário:</strong></li>
    <li><strong>Senha:</strong></li>
    <li><strong>Tipo de acesso (ex: SSH, Telnet, Web):</strong></li>
    <li><strong>Porta no MikroTik (Ether):</strong></li>
<p><strong>Sobre o CPE:</strong></p>
<ul>
    <li><strong>Modelo e Fabricante:</strong></li>
    <li><strong>Tipo (Router/Bridge):</strong></li>

    <li><strong>Login/Senha Inicial:</strong></li>
    <li><strong>Login/Senha Provisionado:</strong></li>
    <li><strong>Possui algum preset de fábrica?</strong></li>
</ul>
<p><strong>Sobre o modelo em bancada:</strong></p>
<ul>
    <li><strong>Número de Série:</strong></li>
    <li><strong>Em qual OLT ele está provisionado?</strong></li>
</ul>
<p><strong>Para os testes:</strong><br>
Precisamos de um contrato de testes ativo no portal. Qual seria o seu usuário e senha PPPoE?</p>
<br>
<p><i>Uma foto da etiqueta do equipamento seria muito útil!</i></p>
<br>
<p>Se tiver algum detalhe adicional de configuração (VLANs, etc.), por favor, adicione também!</p>
<br>
<p>Aguardamos essas informações para dar andamento.<br>
Atenciosamente.</p>
"""



def executar_nova_instalacao(ticket_id: str, api_key: str):
    """
    Verifica um ticket no Freshdesk e, se for de homologação, envia uma resposta automática.
    """
    print(f"--- INICIANDO SCRIPT DE NOVA CPE PARA O TICKET {ticket_id} ---")

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

            mensagem_sucesso = f"SUCESSO! Pedido de informações de homologação enviado para o ticket #{ticket_id}."
            print(mensagem_sucesso)
            return (True, mensagem_sucesso)

        else:
            mensagem_aviso = f"O ticket #{ticket_id} não atende aos critérios para resposta de homologação. Nenhuma ação foi tomada."
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