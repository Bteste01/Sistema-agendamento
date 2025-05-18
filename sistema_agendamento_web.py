import streamlit as st
from datetime import datetime, time
from PIL import Image
import io

# --- Inicializa estado da aplicação ---
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []

if 'admins' not in st.session_state:
    # admin principal inicial (email e senha fixos)
    st.session_state.admins = {
        'admin@empresa.com': {
            'senha': 'Bteste01',
            'principal': True
        }
    }

if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = None

if 'empresa' not in st.session_state:
    st.session_state.empresa = {
        'nome': 'Sua Empresa de Assessoria',
        'descricao': 'Empresa especializada em agendamento de artistas.',
        'logo': None
    }

if 'artistas' not in st.session_state:
    st.session_state.artistas = [
        {
            'nome': 'Bruno Cruz',
            'categoria': 'Cantor',
            'descricao': 'Cantor e compositor com repertório variado.',
            'foto': None,
            'servicos': [
                {'nome': 'Show musical', 'preco': 2500.0}
            ]
        },
        {
            'nome': 'Skreps',
            'categoria': 'Palestrante',
            'descricao': 'Palestrante e influenciador com foco em motivação pessoal.',
            'foto': None,
            'servicos': [
                {'nome': 'Palestra motivacional', 'preco': 1800.0}
            ]
        },
        {
            'nome': 'Lú Almeida',
            'categoria': 'Pregadora',
            'descricao': 'Cantora gospel com experiência em eventos religiosos.',
            'foto': None,
            'servicos': [
                {'nome': 'Ministração gospel', 'preco': 2000.0}
            ]
        }
    ]

# --- Funções ---

def salvar_logo(uploaded_file):
    if uploaded_file:
        img = Image.open(uploaded_file)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        st.session_state.empresa['logo'] = buffer.getvalue()

def mostrar_logo():
    logo = st.session_state.empresa['logo']
    if logo:
        img = Image.open(io.BytesIO(logo))
        st.image(img, width=150)

def login_admin():
    st.subheader("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type='password')
    if st.button("Entrar"):
        admins = st.session_state.admins
        if email in admins and admins[email]['senha'] == senha:
            st.session_state.admin_logado = email
            st.success(f"Logado como {email}")
        else:
            st.error("Email ou senha incorretos.")

def logout_admin():
    st.session_state.admin_logado = None
    st.success("Logout realizado com sucesso.")

def is_admin_principal(email):
    return st.session_state.admins.get(email, {}).get('principal', False)

def adicionar_artista():
    st.subheader("Cadastrar Novo Artista")
    nome = st.text_input("Nome do artista")
    categoria = st.selectbox("Categoria", ['Cantor', 'Palestrante', 'Pregador', 'Outro'])
    descricao = st.text_area("Descrição")
    foto = st.file_uploader("Foto do artista", type=['png', 'jpg', 'jpeg'])
    servicos = []

    with st.expander("Adicionar serviços e preços"):
        servico_nome = st.text_input("Nome do serviço")
        servico_preco = st.number_input("Preço do serviço", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Adicionar serviço"):
            if servico_nome and servico_preco > 0:
                servicos.append({'nome': servico_nome, 'preco': servico_preco})
                st.success(f"Serviço '{servico_nome}' adicionado!")
            else:
                st.error("Preencha nome e preço válidos do serviço.")

    if st.button("Salvar artista"):
        if not nome.strip():
            st.error("Nome do artista é obrigatório.")
            return
        if len(servicos) == 0:
            st.error("Adicione pelo menos um serviço.")
            return
        # salvar foto
        foto_bytes = None
        if foto:
            img = Image.open(foto)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            foto_bytes = buf.getvalue()
        st.session_state.artistas.append({
            'nome': nome,
            'categoria': categoria,
            'descricao': descricao,
            'foto': foto_bytes,
            'servicos': servicos
        })
        st.success(f"Artista '{nome}' cadastrado com sucesso.")

def listar_artistas():
    st.subheader("Lista de Artistas")
    for idx, artista in enumerate(st.session_state.artistas):
        st.markdown(f"### {artista['nome']} ({artista['categoria']})")
        if artista['foto']:
            img = Image.open(io.BytesIO(artista['foto']))
            st.image(img, width=150)
        st.write(artista['descricao'])
        st.write("Serviços:")
        for serv in artista['servicos']:
            st.write(f"- {serv['nome']}: R$ {serv['preco']:.2f}")
        if is_admin_principal(st.session_state.admin_logado):
            if st.button(f"Excluir artista {artista['nome']}", key=f"excluir_{idx}"):
                del st.session_state.artistas[idx]
                st.experimental_rerun()

def adicionar_admin():
    if not is_admin_principal(st.session_state.admin_logado):
        st.error("Apenas o administrador principal pode cadastrar outros administradores.")
        return
    st.subheader("Cadastrar Novo Administrador")
    email_novo = st.text_input("Email do novo administrador")
    senha_nova = st.text_input("Senha", type="password")
    principal = st.checkbox("Administrador principal?")
    if st.button("Cadastrar administrador"):
        if not email_novo.strip() or not senha_nova.strip():
            st.error("Email e senha são obrigatórios.")
            return
        if email_novo in st.session_state.admins:
            st.error("Esse email já está cadastrado.")
            return
        st.session_state.admins[email_novo] = {'senha': senha_nova, 'principal': principal}
        st.success(f"Administrador {email_novo} cadastrado.")

def editar_empresa():
    st.subheader("Editar dados da empresa")
    nome = st.text_input("Nome da empresa", value=st.session_state.empresa['nome'])
    descricao = st.text_area("Descrição da empresa", value=st.session_state.empresa['descricao'])
    logo = st.file_uploader("Logotipo da empresa", type=['png', 'jpg', 'jpeg'])
    if logo:
        salvar_logo(logo)
        st.success("Logotipo atualizado.")
    if st.button("Salvar dados da empresa"):
        st.session_state.empresa['nome'] = nome
        st.session_state.empresa['descricao'] = descricao
        st.success("Dados da empresa atualizados.")

def agendamento_cliente():
    st.title(f"Agendamento - {st.session_state.empresa['nome']}")
    mostrar_logo()
    st.write(st.session_state.empresa['descricao'])
    st.markdown("---")
    st.subheader("Agende um artista")

    # Seleção de artista
    nomes_artistas = [a['nome'] for a in st.session_state.artistas]
    artista_selecionado = st.selectbox("Selecione o artista", nomes_artistas)

    # Busca artista selecionado
    artista = next((a for a in st.session_state.artistas if a['nome'] == artista_selecionado), None)

    # Seleciona serviço
    servico_nomes = [s['nome'] for s in artista['servicos']]
    servico_selecionado = st.selectbox("Selecione o serviço", servico_nomes)

    # Busca preço do serviço selecionado
    servico = next((s for s in artista['servicos'] if s['nome'] == servico_selecionado), None)

    # Dados do contratante
    st.subheader("Dados do contratante")
    nome_contratante = st.text_input("Nome completo")
    email_contratante = st.text_input("Email")
    telefone_contratante = st.text_input("Telefone")
    cidade_contratante = st.text_input("Cidade")

    # Data e horário do evento
    st.subheader("Data e horário do evento")
    data_evento = st.date_input("Data")
    hora_inicio = st.time_input("Hora início", value=time(19, 0))
    hora_fim = st.time_input("Hora fim", value=time(21, 0))

    # Verificar conflito de agendamento
    def verifica_conflito(artista_nome, data_ev, hora_ini, hora_fim):
        for ag in st.session_state.agendamentos:
            if ag['artista'] == artista_nome and ag['data'] == data_ev:
                # Conflito se horário inicial for antes do fim do agendamento existente e horário fim for após o início do existente
                ag_inicio = ag['hora_inicio']
                ag_fim = ag['hora_fim']
                if (hora_ini < ag_fim and hora_fim > ag_inicio):
                    return True
        return False

    if st.button("Agendar"):
        if not nome_contratante.strip() or not email_contratante.strip():
            st.error("Nome e email do contratante são obrigatórios.")
        elif hora_fim <= hora_inicio:
            st.error("Hora fim deve ser maior que hora início.")
        elif verifica_conflito(artista_selecionado, data_evento, hora_inicio, hora_fim):
            st.error("Já existe agendamento para esse artista nesse dia e horário.")
        else:
            st.session_state.agendamentos.append({
                'artista': artista_selecionado,
                'servico': servico_selecionado,
                'preco': servico['preco'],
                'nome_contratante': nome_contratante,
                'email_contratante': email_contratante,
                'telefone_contratante': telefone_contratante,
                'cidade_contratante': cidade_contratante,
                'data': data_evento,
                'hora_inicio': hora_inicio,
                'hora_fim': hora_fim
            })
            st.success("Agendamento realizado com sucesso!")

    st.markdown("---")
    st.markdown("**Contato via WhatsApp:**")
    whatsapp_url = "https://wa.me/5511999999999"  # Troque para o número real
    if st.button("Enviar mensagem no WhatsApp"):
        st.write(f"[Clique aqui para abrir o WhatsApp]({whatsapp_url})")

def admin_area():
    st.sidebar.title("Área do Administrador")
    if st.button("Logout"):
        logout_admin()
        st.experimental_rerun()

    st.sidebar.markdown(f"**Logado como:** {st.session_state.admin_logado}")
    st.title("Painel do Administrador")

    menu = st.sidebar.radio("Menu", ["Lista de Artistas", "Cadastrar Artista", "Cadastrar Administrador", "Editar Dados da Empresa", "Ver Agendamentos"])

    if menu == "Lista de Artistas":
        listar_artistas()
    elif menu == "Cadastrar Artista":
        adicionar_artista()
    elif menu == "Cadastrar Administrador":
        adicionar_admin()
    elif menu == "Editar Dados da Empresa":
        editar_empresa()
    elif menu == "Ver Agendamentos":
        st.subheader("Agendamentos")
        if len(st.session_state.agendamentos) == 0:
            st.info("Nenhum agendamento realizado.")
        else:
            for ag in st.session_state.agendamentos:
                st.write(f"Artista: {ag['artista']}")
                st.write(f"Serviço: {ag['servico']} - R$ {ag['preco']:.2f}")
                st.write(f"Contratante: {ag['nome_contratante']} ({ag['email_contratante']}, {ag['telefone_contratante']}, {ag['cidade_contratante']})")
                st.write(f"Data: {ag['data'].strftime('%d/%m/%Y')}")
                st.write(f"Horário: {ag['hora_inicio'].strftime('%H:%M')} às {ag['hora_fim'].strftime('%H:%M')}")
                st.markdown("---")

# --- Interface principal ---

st.set_page_config(page_title="Sistema de Agendamento", layout="centered")

st.sidebar.title("Navegação")

if st.session_state.admin_logado:
    admin_area()
else:
    # Tela pública de agendamento com botão para login admin
    agendamento_cliente()
    st.markdown("---")
    st.write("Área restrita para administradores:")
    if st.button("Login do administrador"):
        st.session_state.show_login = True

    if st.session_state.get('show_login', False):
        login_admin()
