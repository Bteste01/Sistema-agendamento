import streamlit as st
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Estado inicial
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin' not in st.session_state:
    st.session_state.admin = None  # None, 'principal' ou 'comum'
if 'admin_email' not in st.session_state:
    st.session_state.admin_email = None
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = [
        {"nome": "Bruno Cruz", "servicos": [{"nome": "Show musical", "preco": 2500.00}], "foto": None, "descricao": "Cantor e compositor com repertório variado."},
        {"nome": "Skreps", "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal."},
        {"nome": "Lú Almeida", "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos."}
    ]
if 'admins' not in st.session_state:
    st.session_state.admins = {}

SENHA_ADMIN_PRINCIPAL = "root123"

def login_admin():
    st.sidebar.title("Login de Administrador")

    tipo_login = st.sidebar.radio("Tipo de administrador:", ("Administrador Principal", "Administrador Comum"))

    email = None
    senha = st.sidebar.text_input("Senha", type="password")

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

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.admin = None
        st.session_state.admin_email = None
        st.experimental_rerun()

login_admin()
logout()

menu_opcoes = ["Agendar", "Ver Agendamentos", "Exportar PDF", "Lista de Artistas"]
if st.session_state.admin in ['principal', 'comum']:
    menu_opcoes.append("Cadastrar Artista")
if st.session_state.admin == 'principal':
    menu_opcoes.append("Gerenciar Administradores")

menu = st.sidebar.selectbox("Menu", menu_opcoes)

def mostrar_artista_info(artista):
    if artista.get("foto"):
        st.image(artista["foto"], width=150)
    if artista.get("descricao"):
        st.info(artista["descricao"])

if menu == "Agendar":
    st.title("Agendamento")

    artista_nomes = [a["nome"] for a in st.session_state.artistas_disponiveis]
    artista_escolhido = st.selectbox("Escolha o artista", artista_nomes)
    artista_info = next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista_escolhido)

    mostrar_artista_info(artista_info)

    servicos = [s["nome"] for s in artista_info["servicos"]]
    servico_escolhido = st.selectbox("Escolha o serviço", servicos)
    preco = next(s['preco'] for s in artista_info['servicos'] if s['nome'] == servico_escolhido)

    st.write(f"**Preço:** R$ {preco:.2f}")

    data = st.date_input("Data do agendamento")
    hora = st.time_input("Horário")

    conflito = any(
        ag['artista'] == artista_escolhido and ag['data'] == data and ag['hora'] == hora
        for ag in st.session_state.agendamentos
    )

    st.subheader("Dados do contratante")
    contratante = st.text_input("Nome do contratante")
    email = st.text_input("Email do contratante")
    telefone = st.text_input("Telefone do contratante")
    cidade = st.text_input("Cidade do contratante")

    if st.button("Agendar"):
        if conflito:
            st.error("Este artista já está agendado para essa data e horário.")
        elif not (contratante and email):
            st.error("Por favor, preencha nome e email do contratante.")
        else:
            st.session_state.agendamentos.append({
                "artista": artista_escolhido,
                "servico": servico_escolhido,
                "preco": preco,
                "data": data,
                "hora": hora,
                "contratante": contratante,
                "email": email,
                "telefone": telefone,
                "cidade": cidade
            })
            st.success("Agendamento realizado com sucesso!")

elif menu == "Ver Agendamentos":
    st.title("Agendamentos Realizados")
    if not st.session_state.agendamentos:
        st.info("Nenhum agendamento realizado.")
    else:
        for i, ag in enumerate(st.session_state.agendamentos):
            st.write(f"**{i+1}. Artista:** {ag['artista']} | **Serviço:** {ag['servico']} | **Preço:** R$ {ag['preco']:.2f}")
            st.write(f"   **Data:** {ag['data']} | **Hora:** {ag['hora']}")
            st.write(f"   **Contratante:** {ag['contratante']} | **Email:** {ag['email']} | **Telefone:** {ag['telefone']} | **Cidade:** {ag['cidade']}")
            if st.session_state.admin in ['principal', 'comum']:
                if st.button(f"Cancelar agendamento {i+1}"):
                    st.session_state.agendamentos.pop(i)
                    st.success("Agendamento cancelado.")
                    st.experimental_rerun()

elif menu == "Exportar PDF":
    st.title("Exportar Agendamentos")

    if not st.session_state.agendamentos:
        st.info("Nenhum agendamento para exportar.")
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Agendamentos", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)

        for ag in st.session_state.agendamentos:
            pdf.cell(0, 10, f"Artista: {ag['artista']} - Serviço: {ag['servico']} - Preço: R$ {ag['preco']:.2f}", ln=True)
            pdf.cell(0, 10, f"Data: {ag['data']} - Hora: {ag['hora']}", ln=True)
            pdf.cell(0, 10, f"Contratante: {ag['contratante']} - Email: {ag['email']} - Tel: {ag['telefone']} - Cidade: {ag['cidade']}", ln=True)
            pdf.ln(5)

        pdf_output = "agendamentos.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            st.download_button("Baixar PDF", f, file_name="agendamentos.pdf")

elif menu == "Lista de Artistas":
    st.title("Artistas Disponíveis")
    for artista in st.session_state.artistas_disponiveis:
        st.subheader(artista['nome'])
        mostrar_artista_info(artista)
        for servico in artista['servicos']:
            st.write(f"- {servico['nome']} (R$ {servico['preco']:.2f})")

elif menu == "Cadastrar Artista" and st.session_state.admin in ['principal', 'comum']:
    st.title("Cadastrar Novo Artista")

    nome = st.text_input("Nome do artista")
    descricao = st.text_area("Descrição do artista")
    foto = st.file_uploader("Foto do artista", type=["jpg", "jpeg", "png"])
    servicos = []

    num_servicos = st.number_input("Quantos serviços o artista oferece?", min_value=1, step=1)

    for i in range(int(num_servicos)):
        st.markdown(f"### Serviço {i+1}")
        nome_servico = st.text_input(f"Nome do serviço {i+1}", key=f"servico_{i}")
        preco_servico = st.number_input(f"Preço do serviço {i+1}", min_value=0.0, step=100.0, key=f"preco_{i}")
        servicos.append({"nome": nome_servico, "preco": preco_servico})

    if st.button("Cadastrar Artista"):
        if nome and all(s['nome'] for s in servicos):
            foto_bytes = foto.read() if foto else None
            st.session_state.artistas_disponiveis.append({"nome": nome, "descricao": descricao, "servicos": servicos, "foto": foto_bytes})
            st.success("Artista cadastrado com sucesso!")
        else:
            st.warning("Preencha todos os campos dos serviços.")

elif menu == "Gerenciar Administradores" and st.session_state.admin == 'principal':
    st.title("Gerenciar Administradores")

    st.subheader("Cadastrar novo administrador comum")
    email_novo = st.text_input("Email do novo administrador")
    senha_novo = st.text_input("Senha do novo administrador", type="password")

    if st.button("Cadastrar Administrador"):
        if email_novo and senha_novo:
            if email_novo in st.session_state.admins:
                st.warning("Este email já está cadastrado como administrador.")
            else:
                st.session_state.admins[email_novo] = senha_novo
                st.success(f"Administrador {email_novo} cadastrado com sucesso!")
        else:
            st.warning("Preencha email e senha para o novo administrador.")

    st.subheader("Administradores existentes")
    if not st.session_state.admins:
        st.info("Nenhum administrador comum cadastrado.")
    else:
        for email_admin in st.session_state.admins.keys():
            st.write(f"- {email_admin}")

else:
    if st.session_state.admin is None:
        st.info("Faça login como administrador para acessar funções administrativas.")
