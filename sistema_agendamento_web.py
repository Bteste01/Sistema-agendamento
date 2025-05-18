import streamlit as st
from datetime import datetime
from PIL import Image
import json
import io
import os

# ... [bloco inicial de funções já incluído anteriormente]

# --- Continuação da interface administrativa ---

if st.session_state.admin_logado:
    st.title("Painel Administrativo")

    aba = st.sidebar.selectbox("Menu", ["Artistas", "Agendamentos", "Empresa", "WhatsApp", "Administradores"])

    if aba == "Artistas":
        st.subheader("Cadastro e Edição de Artistas")
        with st.form("novo_artista"):
            nome = st.text_input("Nome do Artista")
            descricao = st.text_area("Descrição")
            categoria = st.text_input("Categoria")
            foto = st.file_uploader("Foto (opcional)", type=["png", "jpg", "jpeg"])
            servicos = st.text_area("Serviços (nome:preco por linha)")
            submitted = st.form_submit_button("Salvar Artista")
            if submitted:
                lista_servicos = []
                for linha in servicos.splitlines():
                    if ":" in linha:
                        nome_serv, preco = linha.split(":")
                        lista_servicos.append({"nome": nome_serv.strip(), "preco": float(preco.strip())})
                imagem = Image.open(foto) if foto else None
                st.session_state.artistas_disponiveis.append({
                    "nome": nome,
                    "descricao": descricao,
                    "categoria": categoria,
                    "foto": imagem,
                    "servicos": lista_servicos
                })
                salvar_artistas()
                st.success("Artista salvo com sucesso!")

        st.subheader("Excluir Artista")
        nomes = [a['nome'] for a in st.session_state.artistas_disponiveis]
        artista_excluir = st.selectbox("Escolha um artista para excluir", nomes)
        if st.button("Excluir Artista"):
            st.session_state.artistas_disponiveis = [a for a in st.session_state.artistas_disponiveis if a['nome'] != artista_excluir]
            salvar_artistas()
            st.success("Artista excluído.")

    elif aba == "Agendamentos":
        st.subheader("Lista de Agendamentos")
        for ag in st.session_state.agendamentos:
            st.markdown(f"**{ag['artista']} - {ag['servico']}**")
            st.write(f"{ag['cliente']} - {ag['email']} - {ag['telefone']} - {ag['cidade']}")
            st.write(f"{ag['inicio']} até {ag['fim']}")
            st.markdown("---")

    elif aba == "Empresa":
        st.subheader("Dados da Empresa")
        with st.form("form_empresa"):
            nome_emp = st.text_input("Nome da Empresa", value=st.session_state.empresa['nome'])
            descricao_emp = st.text_area("Descrição", value=st.session_state.empresa['descricao'])
            logotipo = st.file_uploader("Logotipo (opcional)", type=["png", "jpg", "jpeg"])
            submitted = st.form_submit_button("Salvar")
            if submitted:
                imagem = Image.open(logotipo) if logotipo else st.session_state.empresa['logotipo']
                st.session_state.empresa = {"nome": nome_emp, "descricao": descricao_emp, "logotipo": imagem}
                salvar_empresa()
                st.success("Dados da empresa atualizados!")

    elif aba == "WhatsApp":
        st.subheader("Contato WhatsApp")
        whatsapp_input = st.text_input("Número com DDI (ex: +55 11 91234-5678)", value=st.session_state.whatsapp)
        if st.button("Salvar WhatsApp"):
            st.session_state.whatsapp = whatsapp_input
            salvar_whatsapp()
            st.success("WhatsApp atualizado com sucesso!")

    elif aba == "Administradores":
        if st.session_state.admin_logado == "Administrador Principal":
            st.subheader("Cadastro de Novos Administradores")
            email_novo = st.text_input("Email")
            senha_nova = st.text_input("Senha", type="password")
            if st.button("Cadastrar Novo Admin"):
                st.session_state.admins.append({"email": email_novo, "senha": senha_nova})
                salvar_admins()
                st.success("Administrador cadastrado com sucesso!")
        else:
            st.info("Apenas o Administrador Principal pode cadastrar novos administradores.")
                
