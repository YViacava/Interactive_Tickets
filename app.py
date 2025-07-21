# /assistente_cpe/app.py

import streamlit as st
from reply_maintance import executar_manutencao
from reply_new import executar_nova_instalacao

# --- Configuração da Página ---
st.set_page_config(page_title="Assistente de CPEs", layout="centered")

# --- Interface do Usuário (Frontend) ---
st.title("🤖 Assistente de Automação de CPEs")
st.markdown("Selecione a operação, informe os dados e clique em executar.")

# Adicionando o campo para a chave de API
api_key = st.text_input(
    "Sua Chave de API do Freshdesk",
    type="password",
    help="Sua chave será usada apenas para esta operação e não será armazenada."
)

# Opções para o menu dropdown
opcoes = ('Selecione uma opção', 'Manutenção de CPE', 'CPE Nova')

# Criando os widgets da interface
opcao_selecionada = st.selectbox("Qual operação você deseja realizar?", opcoes)
ticket_id = st.text_input("Digite o ID do Ticket do Freshdesk")
botao_executar = st.button("Executar Automação")

# --- Lógica do Backend ---
if botao_executar:
    # 1. Validação dos inputs (adicionamos a verificação da API Key)
    if not api_key.strip():
        st.warning("Por favor, insira sua Chave de API do Freshdesk.")
    elif opcao_selecionada == 'Selecione uma opção':
        st.warning("Por favor, selecione uma operação no menu.")
    elif not ticket_id.strip():
        st.warning("Por favor, digite o ID do Ticket.")
    else:
        # 2. Execução baseada na seleção
        st.divider()

        if opcao_selecionada == 'Manutenção de CPE':
            with st.spinner(f"Executando manutenção para o ticket {ticket_id}..."):
                # Passamos a chave de API como um novo argumento
                sucesso, mensagem = executar_manutencao(ticket_id, api_key)

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)

        elif opcao_selecionada == 'CPE Nova':
            with st.spinner(f"Configurando nova CPE para o ticket {ticket_id}..."):
                # Passamos a chave de API como um novo argumento
                sucesso, mensagem = executar_nova_instalacao(ticket_id, api_key)

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)