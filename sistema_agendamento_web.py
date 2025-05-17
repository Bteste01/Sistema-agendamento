import streamlit as st
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Inicializa estados da sessão
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
    st.session_state.empresa = {"nome": "Minha Empresa", "descricao": "Descrição da empresa", "logotipo": None}

# ADMINISTRADOR PADRÃO
if 'admin@empresa.com' not in st.session_state.admins:
    st.session_state.admins['admin@empresa.com'] = 'admin123'

# Função para mostrar dados da empresa no topo
def mostrar_dados_empresa():
    st.title(st.session_state.empresa["nome"])
    st.write(st.session_state.empresa["descricao"])
    if st.session_state.empresa["logotipo"]:
        st.image(st.session_state.empresa["logotipo"], width=150)

# Função para verificar conflito de horário
def conflito_horario(artista, data, inicio, fim):
    for ag in st.session_state.agendamentos:
        if ag['artista'] == artista and ag['data'] == data:
            # Verifica se os horários se sobrepõem
            if not (fim <= ag['hora_inicio'] or inicio >= ag['hora_fim']):
                return True
    return False

# Tela pública de agendamento (sem login)
def tela_agendamento():
    mostrar_dados_empresa()
    st.header("Agendamento de Artista")

    nome_cliente = st.text_input("Nome do contratante")
    email_cliente = st.text_input("Email do contratante")
    telefone_cliente = st.text_input("Telefone do contratante")
    cidade_cliente = st.text_input("Cidade do contratante")

    artista = st.selectbox("Escolha o artista", [a['nome'] for a in st.session_state.artistas_disponiveis])
    artista_obj = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista)

    servico = st.selectbox("Escolha o serviço", [s['nome'] for s in artista_obj['servicos']])

    data = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")

    # Botão para confirmar agendamento
    if st.button("Agendar"):
        if nome_cliente.strip() == "" or email_cliente.strip() == "":
            st.error("Preencha nome e email do contratante.")
            return
        if hora_fim <= hora_inicio:
            st.error("Hora de término deve ser depois da hora de início.")
            return
        if conflito_horario(artista, data.strftime("%Y-%m-%d"), hora_inicio.strftime("%H:%M"), hora_fim.strftime("%H:%M")):
            st.error("Já existe agendamento nesse horário para este artista.")
            return
        # Busca preço do serviço
        preco = next(s['preco'] for s in artista_obj['servicos'] if s['nome'] == servico)
        agendamento = {
            "nome_cliente": nome_cliente,
            "email_cliente": email_cliente,
            "telefone_cliente": telefone_cliente,
            "cidade_cliente": cidade_cliente,
            "artista": artista,
            "servico": servico,
            "preco": preco,
            "data": data.strftime("%Y-%m-%d"),
            "hora_inicio": hora_inicio.strftime("%H:%M"),
            "hora_fim": hora_fim.strftime("%H:%M"),
            "status": "Agendado"
        }
        st.session_state.agendamentos.append(agendamento)
        st.success("Agendamento realizado com sucesso!")

# Tela de login do administrador
def tela_login():
    st.header("Login do Administrador")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in st.session_state.admins and st.session_state.admins[email] == senha:
            st.session_state.admin = True
            st.session_state.admin_email = email
            st.success("Login efetuado com sucesso!")
        else:
            st.error("E-mail ou senha incorretos.")

# Tela administrativa (após login)
def tela_admin():
    st.sidebar.header(f"Admin: {st.session_state.admin_email}")
    if st.sidebar.button("Logout"):
        st.session_state.admin = None
        st.session_state.admin_email = None
        st.experimental_rerun()

    st.title("Área administrativa")

    # Gestão da empresa
    st.subheader("Dados da Empresa")
    nome_empresa = st.text_input("Nome da empresa", st.session_state.empresa["nome"])
    descricao_empresa = st.text_area("Descrição da empresa", st.session_state.empresa["descricao"])
    logo = st.file_uploader("Logotipo da empresa", type=["png", "jpg", "jpeg"])
    if logo:
        st.session_state.empresa["logotipo"] = logo.read()
    if st.button("Salvar dados da empresa"):
        st.session_state.empresa["nome"] = nome_empresa
        st.session_state.empresa["descricao"] = descricao_empresa
        st.success("Dados da empresa salvos.")

    # Lista de artistas
    st.subheader("Artistas disponíveis")
    for i, artista in enumerate(st.session_state.artistas_disponiveis):
        st.write(f"**{artista['nome']}** - Categoria: {artista['categoria']}")
        st.write(artista['descricao'])
        servicos = ", ".join([f"{s['nome']} (R${s['preco']:.2f})" for s in artista['servicos']])
        st.write(f"Serviços: {servicos}")
        if artista['foto']:
            image = Image.open(io.BytesIO(artista['foto']))
            st.image(image, width=120)
        if st.button(f"Excluir artista {artista['nome']}", key=f"excluir_{i}"):
            del st.session_state.artistas_disponiveis[i]
            st.experimental_rerun()

    # Lista de agendamentos
    st.subheader("Agendamentos")
    for ag in st.session_state.agendamentos:
        st.write(f"Cliente: {ag['nome_cliente']} | Artista: {ag['artista']} | Serviço: {ag['servico']} | Data: {ag['data']} | Horário: {ag['hora_inicio']} - {ag['hora_fim']}")

# Aplicação principal
def main():
    st.sidebar.title("Sistema de Agendamento")
    # Área de login/área pública
    if st.session_state.admin:
        tela_admin()
    else:
        tela_agendamento()
        with st.expander("Área do administrador"):
            tela_login()

if __name__ == "__main__":
    main()
