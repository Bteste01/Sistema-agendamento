import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta
from PIL import Image
import io

# ---------------------------
# Estado inicial
# ---------------------------
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin' not in st.session_state:
    st.session_state.admin = False
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = False
if 'admins' not in st.session_state:
    st.session_state.admins = {"admin@admin.com": "1234"}  # administrador principal
if 'empresa' not in st.session_state:
    st.session_state.empresa = {"nome": "Minha Empresa", "descricao": "Descrição da empresa", "logotipo": None}
if 'artistas' not in st.session_state:
    st.session_state.artistas = [
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

# ---------------------------
# Função para mostrar dados da empresa
# ---------------------------
def mostrar_empresa():
    st.title(st.session_state.empresa["nome"])
    st.write(st.session_state.empresa["descricao"])
    if st.session_state.empresa["logotipo"]:
        st.image(st.session_state.empresa["logotipo"], width=150)

# ---------------------------
# Função para verificar conflitos
# ---------------------------
def horario_disponivel(artista, data, inicio, fim):
    for ag in st.session_state.agendamentos:
        if ag["artista"] == artista and ag["data"] == data:
            ag_inicio = datetime.strptime(ag["inicio"], "%H:%M")
            ag_fim = datetime.strptime(ag["fim"], "%H:%M")
            novo_inicio = datetime.strptime(inicio, "%H:%M")
            novo_fim = datetime.strptime(fim, "%H:%M")
            if (novo_inicio < ag_fim and novo_fim > ag_inicio):
                return False
    return True

# ---------------------------
# Interface de Agendamento
# ---------------------------
def interface_agendamento():
    st.header("Agendar um artista")
    nome = st.text_input("Seu nome completo")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    cidade = st.text_input("Cidade")
    artista_nomes = [a['nome'] for a in st.session_state.artistas]
    artista_escolhido = st.selectbox("Escolha o artista", artista_nomes)
    artista = next(a for a in st.session_state.artistas if a['nome'] == artista_escolhido)
    servico_escolhido = st.selectbox("Escolha o serviço", [s['nome'] for s in artista['servicos']])
    preco = next(s['preco'] for s in artista['servicos'] if s['nome'] == servico_escolhido)
    data = st.date_input("Data do evento", min_value=datetime.today())
    inicio = st.time_input("Horário de início")
    fim = st.time_input("Horário de término", value=(datetime.combine(datetime.today(), inicio) + timedelta(hours=1)).time())

    if st.button("Confirmar agendamento"):
        if not horario_disponivel(artista_escolhido, data.strftime("%Y-%m-%d"), inicio.strftime("%H:%M"), fim.strftime("%H:%M")):
            st.error("Este horário já está agendado para este artista.")
        else:
            st.session_state.agendamentos.append({
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cidade": cidade,
                "artista": artista_escolhido,
                "servico": servico_escolhido,
                "preco": preco,
                "data": data.strftime("%Y-%m-%d"),
                "inicio": inicio.strftime("%H:%M"),
                "fim": fim.strftime("%H:%M")
            })
            st.success("Agendamento realizado com sucesso!")

# ---------------------------
# Interface de login
# ---------------------------
def login_admin():
    st.subheader("Login do Administrador")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    if st.button("Entrar"):
        if email in st.session_state.admins and st.session_state.admins[email] == senha:
            st.session_state.admin = True
            if email == "admin@admin.com":
                st.session_state.admin_principal = True
            st.success("Login realizado com sucesso")
        else:
            st.error("Email ou senha incorretos")

# ---------------------------
# Interface administrativa
# ---------------------------
def painel_admin():
    st.header("Painel do Administrador")

    aba = st.selectbox("Selecione a aba", ["Empresa", "Artistas", "Agendamentos", "Cadastrar Admin"] if st.session_state.admin_principal else ["Empresa", "Artistas", "Agendamentos"])

    if aba == "Empresa":
        st.subheader("Dados da empresa")
        st.session_state.empresa["nome"] = st.text_input("Nome da empresa", st.session_state.empresa["nome"])
        st.session_state.empresa["descricao"] = st.text_area("Descrição", st.session_state.empresa["descricao"])
        logo = st.file_uploader("Logotipo", type=["png", "jpg"])
        if logo:
            st.session_state.empresa["logotipo"] = logo

    elif aba == "Artistas":
        st.subheader("Lista de Artistas")
        for i, a in enumerate(st.session_state.artistas):
            st.markdown(f"**{a['nome']}** - {a['categoria']}")
            st.write(a['descricao'])
            if st.button(f"Excluir {a['nome']}"):
                st.session_state.artistas.pop(i)
                st.experimental_rerun()

        st.subheader("Cadastrar novo artista")
        nome = st.text_input("Nome do artista")
        categoria = st.text_input("Categoria do artista")
        descricao = st.text_area("Descrição")
        foto = st.file_uploader("Foto do artista", type=["jpg", "png"])
        servicos = []
        with st.expander("Serviços oferecidos"):
            for i in range(3):
                nome_serv = st.text_input(f"Nome do serviço {i+1}", key=f"servico_{i}")
                preco_serv = st.number_input(f"Preço do serviço {i+1}", key=f"preco_{i}", min_value=0.0)
                if nome_serv:
                    servicos.append({"nome": nome_serv, "preco": preco_serv})
        if st.button("Cadastrar artista") and nome and categoria and servicos:
            st.session_state.artistas.append({"nome": nome, "categoria": categoria, "descricao": descricao, "foto": foto, "servicos": servicos})
            st.success("Artista cadastrado com sucesso")

    elif aba == "Agendamentos":
        st.subheader("Agendamentos realizados")
        for ag in st.session_state.agendamentos:
            st.write(ag)

    elif aba == "Cadastrar Admin" and st.session_state.admin_principal:
        email_novo = st.text_input("Email do novo administrador")
        senha_nova = st.text_input("Senha", type="password")
        if st.button("Cadastrar novo admin"):
            if email_novo in st.session_state.admins:
                st.warning("Este email já está cadastrado")
            else:
                st.session_state.admins[email_novo] = senha_nova
                st.success("Administrador cadastrado")

# ---------------------------
# Interface principal
# ---------------------------
mostrar_empresa()
interface_agendamento()

st.markdown("---")
st.markdown("### Acesso administrativo")

if not st.session_state.admin:
    with st.expander("Login do administrador"):
        login_admin()
else:
    painel_admin()
