import streamlit as st
from fpdf import FPDF
from datetime import datetime
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
    # admin principal já cadastrado
    st.session_state.admins = {
        "admin@empresa.com": {"senha": "admin123", "principal": True}
    }

if 'empresa' not in st.session_state:
    st.session_state.empresa = {"nome": "", "descricao": "", "logo": None}


def salvar_imagem_em_bytes(img):
    if img is None:
        return None
    bytes_io = io.BytesIO()
    img.save(bytes_io, format='PNG')
    return bytes_io.getvalue()


def exibir_imagem_bytes(img_bytes):
    if img_bytes:
        st.image(img_bytes, width=150)


def verificar_disponibilidade(artista_nome, data_hora):
    for ag in st.session_state.agendamentos:
        if ag['artista'] == artista_nome and ag['data_hora'] == data_hora:
            return False
    return True


def login():
    st.title("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        admins = st.session_state.admins
        if email in admins and admins[email]["senha"] == senha:
            st.session_state.admin = admins[email]
            st.session_state.admin_email = email
            st.success("Login realizado com sucesso!")
        else:
            st.error("Email ou senha incorretos")


def logout():
    st.session_state.admin = None
    st.session_state.admin_email = None
    st.success("Logout realizado com sucesso!")


def painel_empresa():
    st.header("Configuração da Empresa")
    empresa = st.session_state.empresa
    nome = st.text_input("Nome da Empresa", value=empresa["nome"])
    descricao = st.text_area("Descrição da Empresa", value=empresa["descricao"])
    logo = st.file_uploader("Logotipo da Empresa", type=["png", "jpg", "jpeg"])

    if logo is not None:
        img = Image.open(logo)
        empresa["logo"] = salvar_imagem_em_bytes(img)
    empresa["nome"] = nome
    empresa["descricao"] = descricao

    st.markdown("### Logo atual:")
    exibir_imagem_bytes(empresa["logo"])


def listar_artistas():
    st.header("Lista de Artistas")
    artistas = st.session_state.artistas_disponiveis

    for i, artista in enumerate(artistas):
        with st.expander(f"{artista['nome']} - {artista['categoria']}"):
            st.write("Descrição:", artista.get("descricao", ""))
            exibir_imagem_bytes(artista["foto"])
            st.write("Serviços:")
            for serv in artista["servicos"]:
                st.write(f"- {serv['nome']} : R$ {serv['preco']:.2f}")

            if st.button(f"Excluir artista {artista['nome']}", key=f"del_{i}"):
                artistas.pop(i)
                st.success(f"Artista {artista['nome']} excluído.")
                st.experimental_rerun()


def cadastrar_artista():
    st.header("Cadastrar Novo Artista")
    nome = st.text_input("Nome do Artista")
    categoria = st.text_input("Categoria do Artista (ex: Cantor, Palestrante, Pregador)")
    descricao = st.text_area("Descrição do Artista")
    foto = st.file_uploader("Foto do Artista", type=["png", "jpg", "jpeg"])
    servicos = []

    st.markdown("### Serviços e Preços")
    novo_servico_nome = st.text_input("Nome do Serviço")
    novo_servico_preco = st.number_input("Preço do Serviço (R$)", min_value=0.0, format="%.2f")

    if st.button("Adicionar Serviço"):
        if novo_servico_nome.strip() != "":
            servicos.append({"nome": novo_servico_nome, "preco": novo_servico_preco})
            st.session_state['servicos_temp'] = servicos
            st.experimental_rerun()
        else:
            st.error("O nome do serviço não pode ser vazio.")

    servicos = st.session_state.get('servicos_temp', [])

    if servicos:
        st.markdown("Serviços adicionados:")
        for s in servicos:
            st.write(f"- {s['nome']} : R$ {s['preco']:.2f}")

    if st.button("Salvar Artista"):
        if nome.strip() == "" or not servicos:
            st.error("Por favor, preencha o nome e adicione pelo menos um serviço.")
        else:
            img_bytes = salvar_imagem_em_bytes(Image.open(foto)) if foto else None
            artista = {
                "nome": nome,
                "categoria": categoria,
                "descricao": descricao,
                "foto": img_bytes,
                "servicos": servicos,
            }
            st.session_state.artistas_disponiveis.append(artista)
            st.success(f"Artista {nome} cadastrado com sucesso!")
            st.session_state['servicos_temp'] = []
            st.experimental_rerun()


def agendar():
    st.header("Agendamento de Serviços")
    artistas = st.session_state.artistas_disponiveis

    if not artistas:
        st.warning("Nenhum artista disponível para agendamento.")
        return

    nome_cliente = st.text_input("Nome do contratante")
    email_cliente = st.text_input("Email do contratante")
    telefone_cliente = st.text_input("Telefone do contratante")
    cidade_cliente = st.text_input("Cidade do contratante")

    artista_selecionado = st.selectbox("Selecione o Artista", [a["nome"] for a in artistas])

    artista_obj = next(a for a in artistas if a["nome"] == artista_selecionado)

    servico_selecionado_nome = st.selectbox(
        "Selecione o Serviço",
        [s["nome"] for s in artista_obj["servicos"]],
    )
    servico_obj = next(s for s in artista_obj["servicos"] if s["nome"] == servico_selecionado_nome)

    data_str = st.date_input("Data do evento")
    hora_str = st.time_input("Hora do evento")

    data_hora = datetime.combine(data_str, hora_str)

    # Checar disponibilidade
    if not verificar_disponibilidade(artista_selecionado, data_hora):
        st.error("Este artista já possui um agendamento para esta data e horário.")
        return

    if st.button("Confirmar Agendamento"):
        agendamento = {
            "nome_cliente": nome_cliente,
            "email_cliente": email_cliente,
            "telefone_cliente": telefone_cliente,
            "cidade_cliente": cidade_cliente,
            "artista": artista_selecionado,
            "servico": servico_selecionado_nome,
            "preco": servico_obj["preco"],
            "data_hora": data_hora,
            "data_agendamento": datetime.now(),
        }
        st.session_state.agendamentos.append(agendamento)
        st.success("Agendamento realizado com sucesso!")


def listar_agendamentos():
    st.header("Agendamentos Realizados")
    agendamentos = st.session_state.agendamentos
    if not agendamentos:
        st.info("Nenhum agendamento realizado ainda.")
        return

    for ag in agendamentos:
        st.write(f"Cliente: {ag['nome_cliente']}, Email: {ag['email_cliente']}, Telefone: {ag['telefone_cliente']}, Cidade: {ag['cidade_cliente']}")
        st.write(f"Artista: {ag['artista']}")
        st.write(f"Serviço: {ag['servico']} - Preço: R$ {ag['preco']:.2f}")
        st.write(f"Data/Hora do evento: {ag['data_hora'].strftime('%d/%m/%Y %H:%M')}")
        st.write("---")


def painel_admin_principal():
    st.sidebar.header("Painel do Admin Principal")
    if st.sidebar.button("Cadastrar Novo Administrador"):
        st.title("Cadastrar Novo Administrador")
        email_novo = st.text_input("Email do novo administrador")
        senha_novo = st.text_input("Senha do novo administrador", type="password")
        if st.button("Salvar Administrador"):
            if email_novo.strip() == "" or senha_novo.strip() == "":
                st.error("Preencha todos os campos.")
            else:
                if email_novo in st
