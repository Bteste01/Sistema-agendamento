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
            "servicos": [
                {"nome": "Show musical", "preco": 2500.00},
                {"nome": "Palestra musical", "preco": 3000.00}
            ],
            "foto": None,
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor"
        },
        {
            "nome": "Skreps",
            "servicos": [
                {"nome": "Palestra motivacional", "preco": 1800.00},
                {"nome": "Workshop de liderança", "preco": 2200.00}
            ],
            "foto": None,
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante"
        },
        {
            "nome": "Lú Almeida",
            "servicos": [
                {"nome": "Ministração gospel", "preco": 2000.00}
            ],
            "foto": None,
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora"
        }
    ]

if 'admins' not in st.session_state:
    # Um admin principal inicial para testes (email e senha: admin@empresa.com / admin123)
    st.session_state.admins = {
        "admin@empresa.com": {"senha": "admin123", "principal": True}
    }

if 'empresa' not in st.session_state:
    st.session_state.empresa = {
        "nome": "Minha Empresa",
        "descricao": "Descrição da empresa aqui.",
        "logo": None
    }


def login():
    st.title("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in st.session_state.admins:
            if st.session_state.admins[email]["senha"] == senha:
                st.session_state.admin = st.session_state.admins[email]
                st.session_state.admin_email = email
                st.success(f"Bem-vindo, {email}!")
                st.experimental_rerun()
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Administrador não encontrado.")


def logout():
    st.session_state.admin = None
    st.session_state.admin_email = None
    st.experimental_rerun()


def painel_empresa():
    st.header("Configurações da Empresa")
    nome = st.text_input("Nome da empresa", st.session_state.empresa.get("nome", ""))
    descricao = st.text_area("Descrição da empresa", st.session_state.empresa.get("descricao", ""))
    logo = st.file_uploader("Logotipo da empresa", type=["png", "jpg", "jpeg"])

    if st.button("Salvar dados da empresa"):
        st.session_state.empresa["nome"] = nome
        st.session_state.empresa["descricao"] = descricao
        if logo is not None:
            st.session_state.empresa["logo"] = logo.getvalue()
        st.success("Dados da empresa atualizados com sucesso!")


def listar_artistas():
    st.header("Lista de Artistas")
    for idx, artista in enumerate(st.session_state.artistas_disponiveis):
        col1, col2 = st.columns([1, 3])
        with col1:
            if artista["foto"]:
                img = Image.open(io.BytesIO(artista["foto"]))
                st.image(img, width=100)
            else:
                st.text("Sem foto")
        with col2:
            st.subheader(f"{artista['nome']} ({artista['categoria']})")
            st.write(artista["descricao"])
            for servico in artista["servicos"]:
                st.write(f"- {servico['nome']}: R$ {servico['preco']:.2f}")

            if st.session_state.admin and st.session_state.admin.get("principal", False):
                if st.button(f"Excluir artista {artista['nome']}", key=f"excluir_{idx}"):
                    st.session_state.artistas_disponiveis.pop(idx)
                    st.success(f"Artista {artista['nome']} excluído.")
                    st.experimental_rerun()
        st.markdown("---")


def cadastrar_artista():
    st.header("Cadastrar Novo Artista")
    nome = st.text_input("Nome do artista")
    categoria = st.selectbox("Categoria", ["Cantor", "Palestrante", "Pregador", "Outro"])
    descricao = st.text_area("Descrição")
    foto = st.file_uploader("Foto do artista", type=["png", "jpg", "jpeg"])
    servicos = []

    # Entrada de múltiplos serviços
    st.subheader("Serviços do artista")
    qtd_servicos = st.number_input("Quantos serviços deseja cadastrar?", min_value=1, max_value=10, value=1, step=1)

    for i in range(qtd_servicos):
        nome_servico = st.text_input(f"Nome do serviço {i+1}", key=f"servico_nome_{i}")
        preco_servico = st.number_input(f"Preço do serviço {i+1} (R$)", min_value=0.0, step=10.0, key=f"servico_preco_{i}")
        if nome_servico.strip() != "":
            servicos.append({"nome": nome_servico, "preco": preco_servico})

    if st.button("Salvar artista"):
        if nome.strip() == "" or len(servicos) == 0:
            st.error("Por favor, preencha o nome do artista e ao menos um serviço.")
        else:
            foto_bytes = None
            if foto:
                foto_bytes = foto.getvalue()
            novo_artista = {
                "nome": nome,
                "categoria": categoria,
                "descricao": descricao,
                "foto": foto_bytes,
                "servicos": servicos
            }
            st.session_state.artistas_disponiveis.append(novo_artista)
            st.success(f"Artista {nome} cadastrado com sucesso!")
            st.experimental_rerun()


def agendar():
    st.header("Agendamento")

    if not st.session_state.artistas_disponiveis:
        st.warning("Nenhum artista disponível para agendamento.")
        return

    artista_nome = st.selectbox("Escolha o artista", [a["nome"] for a in st.session_state.artistas_disponiveis])
    artista = next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista_nome)

    servico_nome = st.selectbox("Escolha o serviço", [s["nome"] for s in artista["servicos"]])
    servico = next(s for s in artista["servicos"] if s["nome"] == servico_nome)

    # Seleção de data
    data = st.date_input("Data do evento")
    hora = st.time_input("Hora do evento")

    # Dados contratante
    st.subheader("Dados do Contratante")
    nome_contratante = st.text_input("Nome do contratante")
    email_contratante = st.text_input("Email")
    telefone_contratante = st.text_input("Telefone")
    cidade_contratante = st.text_input("Cidade")

    # Verifica se o horário está disponível para o artista
    dt_evento = datetime.combine(data, hora)
    ocupado = False
    for ag in st.session_state.agendamentos:
        if (ag["artista"] == artista_nome and
            ag["data_hora"] == dt_evento):
            ocupado = True
            break

    if ocupado:
        st.error("Este horário já está reservado para este artista. Por favor, escolha outro.")
        return

    if st.button("Confirmar agendamento"):
        if not nome_contratante or not email_contratante or not telefone_contratante or not cidade_contratante:
            st.error("Por favor, preencha todos os dados do contratante.")
            return
        agendamento = {
            "artista": artista_nome,
            "servico": servico_nome,
            "preco": servico["preco"],
            "data_hora": dt_evento,
            "contratante": {
                "nome": nome_contratante,
                "email": email_contratante,
                "telefone": telefone_contratante,
                "cidade": cidade_contratante
            }
        }
        st.session_state.agendamentos.append(agendamento)
        st.success(f"Agendamento confirmado para {artista_nome} no dia {dt_evento.strftime('%d/%m/%Y %H:%M')}.")


def listar_agendamentos():
    st.header("Agendamentos")
    if not st.session_state.agendamentos:
        st.info("Nenhum agendamento realizado.")
        return

    for idx, ag in enumerate(st.session_state.agendamentos):
        st.markdown("---")
        st.write(f"**Artista:** {ag['artista']}")
        st.write(f"**Serviço:** {ag['servico']}")
        st.write(f"**Preço:** R$ {ag['preco']:.2f}")
        st.write(f"**Data e Hora:** {ag['data_hora'].strftime('%d/%m/%Y %H:%M')}")
        st.write(f"**Contratante:** {ag['contratante']['nome']}")
        st.write(f"**Email:** {ag['contratante']['email']}")
        st.write(f"**Telefone:** {ag['contratante']['telefone']}")
        st.write(f"**Cidade:** {ag['contratante']['cidade']}")

        if st.session_state.admin and st.session_state.admin.get("principal", False):
            if st.button(f"Excluir agendamento {idx}", key=f"excluir_ag_{idx}"):
                st.session_state.agendamentos.pop(idx)
                st.success("Agendamento excluído.")
                st.experimental_rerun()


def painel_admin_principal():
    st.sidebar.header("Painel do Admin Principal")
    st.title("Cadastrar Novo Administrador")
    email_novo = st.text_input("Email do novo administrador")
    senha_novo = st.text_input("Senha do novo administrador", type="password")
    if st.button("Salvar Administrador"):
        if email_novo.strip() == "" or senha_novo.strip() == "":
            st.error("Preencha todos os campos.")
        else:
            if email_novo in st.session_state.admins:
                st.error("Este email já está cadastrado como administrador.")
            else:
                st.session_state.admins[email_novo] = {"senha": senha_novo, "principal": False}
                st.success(f"Administrador {email_novo} cadastrado com sucesso!")


def main():
    st.sidebar.title("Sistema de Agendamento")

    if st.session_state.admin is None:
        login()
        return

    st.sidebar.write(f"Logado como: {st.session_state.admin_email}")
    if st.sidebar.button("Logout"):
        logout()
        return

    is_principal = st.session_state.admin.get("principal", False)

    menu = ["Agendar", "Listar Agendamentos", "Configurar Empresa", "Lista de Artistas"]
    if is_principal:
        menu.append("Cadastrar Artista")
        menu.append("Painel Admin Principal")

    escolha = st.sidebar.radio("Navegação", menu)

    if escolha == "Agendar":
        agendar()
    elif escolha == "Listar Agendamentos":
        listar_agendamentos()
    elif escolha == "Configurar Empresa":
        painel_empresa()
    elif escolha == "Lista de Artistas":
        listar_artistas()
    elif escolha == "Cadastrar Artista" and is_principal:
        cadastrar_artista()
    elif escolha == "Painel Admin Principal" and is_principal:
        painel_admin_principal()


if __name__ == "__main__":
    main()
