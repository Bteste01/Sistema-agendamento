import streamlit as st
from fpdf import FPDF
from datetime import datetime
from PIL import Image import io

#Estado inicial

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = [] if 'admin' not in st.session_state: st.session_state.admin = None if 'admin_email' not in st.session_state: st.session_state.admin_email = None if 'artistas_disponiveis' not in st.session_state: st.session_state.artistas_disponiveis = [ {"nome": "Bruno Cruz", "servicos": [{"nome": "Show musical", "preco": 2500.00}], "foto": None, "descricao": "Cantor e compositor com repertório variado.", "categoria": "Cantor"}, {"nome": "Skreps", "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal.", "categoria": "Palestrante"}, {"nome": "Lú Almeida", "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos.", "categoria": "Pregadora"} ] if 'admins' not in st.session_state: st.session_state.admins = {} if 'empresa' not in st.session_state: st.session_state.empresa = {"nome": "", "descricao": "", "logotipo": None}

SENHA_ADMIN_PRINCIPAL = "root123"

def login_admin(): st.sidebar.title("Login de Administrador") tipo_login = st.sidebar.radio("Tipo de administrador:", ("Administrador Principal", "Administrador Comum")) email = None senha = st.sidebar.text_input("Senha", type="password")

if tipo_login == "Administrador Principal":
    if st.sidebar.button("Entrar como Admin Principal"):
        if senha == SENHA_ADMIN_PRINCIPAL:
            st.session_state.admin = 'principal'
            st.session_state.admin_email = None
            st.sidebar.success("Logado como Administrador Principal")
        else:
            st.sidebar.error("Senha incorreta para Admin Principal")
else:
    email = st.sidebar.text_input("Email")
    if st.sidebar.button("Entrar como Admin Comum"):
        if email in st.session_state.admins and st.session_state.admins[email] == senha:
            st.session_state.admin = 'comum'
            st.session_state.admin_email = email
            st.sidebar.success(f"Logado como Admin Comum: {email}")
        else:
            st.sidebar.error("Credenciais inválidas")

def logout(): if st.sidebar.button("Logout"): st.session_state.admin = None st.session_state.admin_email = None st.experimental_rerun()

login_admin() logout()

menu_opcoes = ["Agendar", "Ver Agendamentos", "Exportar PDF", "Lista de Artistas"] if st.session_state.admin in ['principal', 'comum']: menu_opcoes.append("Cadastrar Artista") if st.session_state.admin == 'principal': menu_opcoes.append("Gerenciar Administradores") menu_opcoes.append("Empresa")

menu = st.sidebar.selectbox("Menu", menu_opcoes)

def mostrar_artista_info(artista): if artista.get("foto"): st.image(artista["foto"], width=150) if artista.get("descricao"): st.info(artista["descricao"]) if artista.get("categoria"): st.write(f"Categoria: {artista['categoria']}")

if menu == "Empresa" and st.session_state.admin == 'principal': st.title("Informações da Empresa") nome_empresa = st.text_input("Nome da Empresa", value=st.session_state.empresa["nome"]) descricao = st.text_area("Descrição", value=st.session_state.empresa["descricao"]) logotipo = st.file_uploader("Logotipo", type=["jpg", "jpeg", "png"])

if st.button("Salvar Empresa"):
    st.session_state.empresa["nome"] = nome_empresa
    st.session_state.empresa["descricao"] = descricao
    if logotipo:
        st.session_state.empresa["logotipo"] = logotipo.read()
    st.success("Informações da empresa salvas com sucesso!")

if menu == "Lista de Artistas": st.title("Artistas Disponíveis") if st.session_state.empresa["logotipo"]: st.image(st.session_state.empresa["logotipo"], width=150) if st.session_state.empresa["nome"]: st.subheader(st.session_state.empresa["nome"]) if st.session_state.empresa["descricao"]: st.write(st.session_state.empresa["descricao"])

for i, artista in enumerate(st.session_state.artistas_disponiveis):
    st.subheader(artista['nome'])
    mostrar_artista_info(artista)
    for servico in artista['servicos']:
        st.write(f"- {servico['nome']} (R$ {servico['preco']:.2f})")
    if st.session_state.admin == 'principal':
        if st.button(f"Excluir {artista['nome']}"):
            st.session_state.artistas_disponiveis.pop(i)
            st.success("Artista excluído com sucesso.")
            st.experimental_rerun()

elif menu == "Cadastrar Artista" and st.session_state.admin in ['principal', 'comum']: st.title("Cadastrar Novo Artista") nome = st.text_input("Nome do artista") categoria = st.text_input("Categoria do artista") descricao = st.text_area("Descrição do artista") foto = st.file_uploader("Foto do artista", type=["jpg", "jpeg", "png"]) servicos = [] num_servicos = st.number_input("Quantos serviços o artista oferece?", min_value=1, step=1)

for i in range(int(num_servicos)):
    st.markdown(f"### Serviço {i+1}")
    nome_servico = st.text_input(f"Nome do serviço {i+1}", key=f"servico_{i}")
    preco_servico = st.number_input(f"Preço do serviço {i+1}", min_value=0.0, step=100.0, key=f"preco_{i}")
    servicos.append({"nome": nome_servico, "preco": preco_servico})

if st.button("Cadastrar Artista"):
    if nome and all(s['nome'] for s in servicos):
        foto_bytes = foto.read() if foto else None
        st.session_state.artistas_disponiveis.append({
            "nome": nome,
            "descricao": descricao,
            "categoria": categoria,
            "servicos": servicos,
            "foto": foto_bytes
        })
        st.success("Artista cadastrado com sucesso!")
    else:
        st.warning("Preencha todos os campos dos serviços e o nome do artista.")

