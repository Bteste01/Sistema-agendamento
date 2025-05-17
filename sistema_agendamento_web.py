import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta
from PIL import Image
import io

# ------------------------ ESTADO INICIAL ------------------------
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
    st.session_state.admins = {"admin@admin.com": "admin123"}  # Admin principal
if 'empresa' not in st.session_state:
    st.session_state.empresa = {"nome": "", "descricao": "", "logo": None}

# ------------------------ FUNÇÕES AUXILIARES ------------------------
def verificar_disponibilidade(artista, data, inicio, fim):
    for ag in st.session_state.agendamentos:
        if ag['artista'] == artista and ag['data'] == data:
            ag_inicio = datetime.strptime(ag['inicio'], '%H:%M')
            ag_fim = datetime.strptime(ag['fim'], '%H:%M')
            novo_inicio = datetime.strptime(inicio, '%H:%M')
            novo_fim = datetime.strptime(fim, '%H:%M')
            if novo_inicio < ag_fim and novo_fim > ag_inicio:
                return False
    return True

# ------------------------ LOGIN ------------------------
st.title("Sistema de Agendamento de Artistas")
if not st.session_state.admin:
    st.subheader("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in st.session_state.admins and st.session_state.admins[email] == senha:
            st.session_state.admin = True
            st.session_state.admin_email = email
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Credenciais inválidas.")
else:
    menu = st.sidebar.radio("Menu", ["Agendamentos", "Cadastrar Artista", "Listar Artistas", "Empresa", "Novo Administrador", "Sair"])

    if menu == "Empresa":
        st.subheader("Dados da Empresa")
        st.session_state.empresa['nome'] = st.text_input("Nome da Empresa", st.session_state.empresa['nome'])
        st.session_state.empresa['descricao'] = st.text_area("Descrição", st.session_state.empresa['descricao'])
        logo = st.file_uploader("Logotipo", type=["png", "jpg", "jpeg"])
        if logo:
            st.session_state.empresa['logo'] = logo.read()
        st.success("Dados atualizados!")

    elif menu == "Cadastrar Artista":
        st.subheader("Cadastro de Artista")
        nome = st.text_input("Nome do Artista")
        categoria = st.text_input("Categoria")
        descricao = st.text_area("Descrição")
        foto = st.file_uploader("Foto do Artista", type=["png", "jpg", "jpeg"])

        servicos = []
        num_servicos = st.number_input("Quantos serviços esse artista oferece?", min_value=1, step=1)
        for i in range(num_servicos):
            with st.expander(f"Serviço {i+1}"):
                servico_nome = st.text_input(f"Nome do serviço {i+1}", key=f"sn{i}")
                preco = st.number_input(f"Preço do serviço {i+1}", min_value=0.0, step=0.01, key=f"pr{i}")
                servicos.append({"nome": servico_nome, "preco": preco})

        if st.button("Salvar Artista"):
            st.session_state.artistas_disponiveis.append({
                "nome": nome,
                "servicos": servicos,
                "foto": foto.read() if foto else None,
                "descricao": descricao,
                "categoria": categoria
            })
            st.success("Artista cadastrado com sucesso!")

    elif menu == "Listar Artistas":
        st.subheader("Artistas Cadastrados")
        for i, artista in enumerate(st.session_state.artistas_disponiveis):
            st.markdown(f"### {artista['nome']} ({artista['categoria']})")
            if artista['foto']:
                st.image(artista['foto'], width=150)
            st.write(artista['descricao'])
            st.write("**Serviços:**")
            for servico in artista['servicos']:
                st.write(f"- {servico['nome']} - R$ {servico['preco']:.2f}")
            if st.button(f"Excluir {artista['nome']}", key=f"excluir{i}"):
                del st.session_state.artistas_disponiveis[i]
                st.success("Artista excluído.")
                st.experimental_rerun()

    elif menu == "Agendamentos":
        st.subheader("Agendamento de Serviços")
        if st.session_state.empresa['logo']:
            st.image(st.session_state.empresa['logo'], width=100)
        st.write(f"**{st.session_state.empresa['nome']}**")
        st.write(st.session_state.empresa['descricao'])

        nome_cliente = st.text_input("Seu nome")
        email_cliente = st.text_input("Email")
        telefone = st.text_input("Telefone")
        cidade = st.text_input("Cidade")

        artista_nomes = [a['nome'] for a in st.session_state.artistas_disponiveis]
        artista_selecionado = st.selectbox("Escolha o artista", artista_nomes)
        artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)

        servico = st.selectbox("Serviço", [s['nome'] for s in artista_info['servicos']])
        data_evento = st.date_input("Data do Evento", min_value=datetime.now().date())
        hora_inicio = st.time_input("Horário de Início")
        hora_fim = st.time_input("Horário de Término")

        if st.button("Agendar"):
            if hora_fim <= hora_inicio:
                st.error("O horário de término deve ser após o de início.")
            elif not verificar_disponibilidade(artista_selecionado, data_evento, hora_inicio.strftime('%H:%M'), hora_fim.strftime('%H:%M')):
                st.error("Esse artista já está agendado nesse horário.")
            else:
                st.session_state.agendamentos.append({
                    "cliente": nome_cliente,
                    "email": email_cliente,
                    "telefone": telefone,
                    "cidade": cidade,
                    "artista": artista_selecionado,
                    "servico": servico,
                    "data": str(data_evento),
                    "inicio": hora_inicio.strftime('%H:%M'),
                    "fim": hora_fim.strftime('%H:%M')
                })
                st.success("Agendamento realizado com sucesso!")

    elif menu == "Novo Administrador":
        if st.session_state.admin_email != "admin@admin.com":
            st.warning("Apenas o administrador principal pode cadastrar novos administradores.")
        else:
            email_novo = st.text_input("Email do novo administrador")
            senha_novo = st.text_input("Senha", type="password")
            if st.button("Cadastrar"):
                if email_novo in st.session_state.admins:
                    st.error("Esse email já está cadastrado.")
                else:
                    st.session_state.admins[email_novo] = senha_novo
                    st.success("Novo administrador cadastrado com sucesso.")

    elif menu == "Sair":
        st.session_state.admin = None
        st.session_state.admin_email = None
        st.experimental_rerun()
        
