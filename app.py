import streamlit as st
from reply_maintance import executar_manutencao
from reply_new import executar_nova_instalacao


st.set_page_config(page_title="Assistente de CPEs", layout="centered")


st.title("🤖 Assistente de Automação de CPEs")
st.markdown("Selecione a operação, informe os dados e clique em executar.")


api_key = st.text_input(
    "Sua Chave de API do Freshdesk",
    type="password",
    help="Sua chave será usada apenas para esta operação e não será armazenada."
)


opcoes = ('Selecione uma opção', 'Manutenção de CPE', 'CPE Nova')


opcao_selecionada = st.selectbox("Qual operação você deseja realizar?", opcoes)
ticket_id = st.text_input("Digite o ID do Ticket do Freshdesk")
botao_executar = st.button("Executar Automação")


if botao_executar:

    if not api_key.strip():
        st.warning("Por favor, insira sua Chave de API do Freshdesk.")
    elif opcao_selecionada == 'Selecione uma opção':
        st.warning("Por favor, selecione uma operação no menu.")
    elif not ticket_id.strip():
        st.warning("Por favor, digite o ID do Ticket.")
    else:

        st.divider()

        if opcao_selecionada == 'Manutenção de CPE':
            with st.spinner(f"Executando manutenção para o ticket {ticket_id}..."):

                sucesso, mensagem = executar_manutencao(ticket_id, api_key)

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)

        elif opcao_selecionada == 'CPE Nova':
            with st.spinner(f"Configurando nova CPE para o ticket {ticket_id}..."):

                sucesso, mensagem = executar_nova_instalacao(ticket_id, api_key)

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)