import streamlit as st
from fpdf import FPDF
from datetime import datetime, time
from PIL import Image
import io

# Estado inicial
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin' not in st.session_state:
    st.session_state.admin = None
if 'admin_email' not in st.session_state:
    st.session_state.admin_email = None
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = [
        {
            "nome": "Bruno Cruz",
            "servicos": [{"nome": "Show musical", "preco": 2500.00}],
            "foto": None,
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor"
        },
        {
            "nome": "Skreps",
            "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
            "foto": None,
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante"
        },
        {
            "nome": "Lú Almeida",
            "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
            "foto": None,
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora"
        }
    ]
if 'admins' not in st.session_state:
    st.session_state.admins = {}
if 'empresa' not in st.session_state:
    st.session_state.empresa = {"nome": "", "descricao": "", "logo": None}

# Função de login
st.title("Sistema de Agendamento de Artistas")
if not st.session_state.admin:
    st.subheader("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email == "admin@empresa.com" and senha == "admin123":
            st.session_state.admin = True
            st.session_state.admin_email = email
        elif email in st.session_state.admins and st.session_state.admins[email] == senha:
            st.session_state.admin = True
            st.session_state.admin_email = email
        else:
            st.error("Credenciais inválidas")
    st.stop()

# Menu principal
menu = st.sidebar.selectbox("Menu", ["Agendamento", "Lista de Artistas", "Cadastrar Artista", "Dados da Empresa", "Gerenciar Administradores"])

# Agendamento
if menu == "Agendamento":
    st.subheader("Agendamento de Serviço")

    if st.session_state.empresa["logo"]:
        st.image(st.session_state.empresa["logo"], width=100)
    st.markdown(f"**{st.session_state.empresa['nome']}**")
    st.markdown(st.session_state.empresa['descricao'])

    artista_nome = st.selectbox("Escolha o artista", [artista["nome"] for artista in st.session_state.artistas_disponiveis])
    artista = next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista_nome)
    servico = st.selectbox("Escolha o serviço", [s["nome"] for s in artista["servicos"]])
    data = st.date_input("Data do evento")
    hora_inicio = st.time_input("Horário de Início")
    hora_fim = st.time_input("Horário de Término")

    email_cont = st.text_input("Email do Contratante")
    telefone = st.text_input("Telefone do Contratante")
    cidade = st.text_input("Cidade do Evento")

    conflito = any(a["data"] == data and a["hora_inicio"] <= hora_inicio < a["hora_fim"] and a["artista"] == artista_nome for a in st.session_state.agendamentos)

    if conflito:
        st.warning("Este artista já está agendado neste horário.")
    elif st.button("Confirmar Agendamento"):
        st.session_state.agendamentos.append({
            "artista": artista_nome,
            "servico": servico,
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "email": email_cont,
            "telefone": telefone,
            "cidade": cidade
        })
        st.success("Agendamento realizado com sucesso!")

# Lista de Artistas
elif menu == "Lista de Artistas":
    st.subheader("Artistas Cadastrados")
    for i, artista in enumerate(st.session_state.artistas_disponiveis):
        st.markdown(f"### {artista['nome']}")
        if artista['foto']:
            st.image(artista['foto'], width=150)
        st.markdown(f"**Categoria:** {artista['categoria']}")
        st.markdown(f"**Descrição:** {artista['descricao']}")
        for serv in artista['servicos']:
            st.markdown(f"- {serv['nome']} - R$ {serv['preco']:.2f}")
        if st.button(f"Excluir {artista['nome']}"):
            st.session_state.artistas_disponiveis.pop(i)
            st.success("Artista excluído.")
            st.experimental_rerun()

# Cadastro de Artista
elif menu == "Cadastrar Artista" and st.session_state.admin_email == "admin@empresa.com":
    st.subheader("Cadastrar Novo Artista")
    nome = st.text_input("Nome do Artista")
    categoria = st.text_input("Categoria")
    descricao = st.text_area("Descrição")
    servicos = []

    with st.form("servico_form"):
        nome_servico = st.text_input("Nome do Serviço")
        preco_servico = st.number_input("Preço do Serviço", min_value=0.0)
        adicionar = st.form_submit_button("Adicionar Serviço")
        if adicionar and nome_servico:
            servicos.append({"nome": nome_servico, "preco": preco_servico})

    if "servicos_temp" not in st.session_state:
        st.session_state.servicos_temp = []
    if adicionar and nome_servico:
        st.session_state.servicos_temp.append({"nome": nome_servico, "preco": preco_servico})

    st.markdown("### Serviços Cadastrados")
    for serv in st.session_state.servicos_temp:
        st.markdown(f"- {serv['nome']} - R$ {serv['preco']:.2f}")

    foto = st.file_uploader("Foto do Artista", type=["jpg", "png"])

    if st.button("Salvar Artista"):
        imagem = Image.open(foto) if foto else None
        st.session_state.artistas_disponiveis.append({
            "nome": nome,
            "servicos": st.session_state.servicos_temp,
            "foto": imagem,
            "descricao": descricao,
            "categoria": categoria
        })
        st.session_state.servicos_temp = []
        st.success("Artista cadastrado com sucesso!")

# Dados da Empresa
elif menu == "Dados da Empresa" and st.session_state.admin:
    st.subheader("Informações da Empresa")
    nome = st.text_input("Nome da Empresa", value=st.session_state.empresa["nome"])
    descricao = st.text_area("Descrição da Empresa", value=st.session_state.empresa["descricao"])
    logo = st.file_uploader("Logotipo", type=["png", "jpg"])

    if st.button("Salvar Dados"):
        st.session_state.empresa["nome"] = nome
        st.session_state.empresa["descricao"] = descricao
        if logo:
            st.session_state.empresa["logo"] = Image.open(logo)
        st.success("Dados da empresa atualizados.")

# Gerenciar administradores
elif menu == "Gerenciar Administradores" and st.session_state.admin_email == "admin@empresa.com":
    st.subheader("Gerenciar Administradores")
    email_novo = st.text_input("Email do novo administrador")
    senha_novo = st.text_input("Senha", type="password")
    if st.button("Cadastrar Administrador"):
        if email_novo in st.session_state.admins:
            st.warning("Administrador já cadastrado.")
        else:
            st.session_state.admins[email_novo] = senha_novo
            st.success("Administrador cadastrado com sucesso.")
    
