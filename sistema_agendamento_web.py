import streamlit as st
from datetime import datetime, time
from PIL import Image
import io

# --- Inicialização do estado da sessão ---

if 'empresa' not in st.session_state:
    st.session_state.empresa = {
        'nome': 'Sua Empresa',
        'descricao': 'Descrição da empresa de assessoria artística.',
        'logo': None
    }

if 'admins' not in st.session_state:
    # admin principal fixo
    st.session_state.admins = {
        'admin@empresa.com': {
            'senha': 'admin123',
            'principal': True
        }
    }

if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = False
if 'admin_email' not in st.session_state:
    st.session_state.admin_email = None
if 'mostrar_login_admin' not in st.session_state:
    st.session_state.mostrar_login_admin = False

if 'artistas' not in st.session_state:
    st.session_state.artistas = [
        {
            'nome': 'Bruno Cruz',
            'categoria': 'Cantor',
            'descricao': 'Cantor e compositor com repertório variado.',
            'servicos': [{'nome': 'Show musical', 'preco': 2500.0}],
            'foto': None
        },
        {
            'nome': 'Skreps',
            'categoria': 'Palestrante',
            'descricao': 'Palestrante e influenciador com foco em motivação pessoal.',
            'servicos': [{'nome': 'Palestra motivacional', 'preco': 1800.0}],
            'foto': None
        },
        {
            'nome': 'Lú Almeida',
            'categoria': 'Pregadora',
            'descricao': 'Cantora gospel com experiência em eventos religiosos.',
            'servicos': [{'nome': 'Ministração gospel', 'preco': 2000.0}],
            'foto': None
        }
    ]

if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []  # lista de dicts com dados dos agendamentos

# --- Funções de apoio ---

def salvar_logo():
    uploaded_file = st.file_uploader("Carregar logotipo da empresa (PNG/JPG)", type=['png','jpg','jpeg'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.empresa['logo'] = image
        st.success("Logo salva!")

def mostrar_logo():
    if st.session_state.empresa['logo']:
        st.image(st.session_state.empresa['logo'], width=150)

def login_admin():
    st.title("Login do Administrador")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in st.session_state.admins and st.session_state.admins[email]['senha'] == senha:
            st.session_state.admin_logado = True
            st.session_state.admin_email = email
            st.session_state.mostrar_login_admin = False
            st.success("Login realizado!")
        else:
            st.error("Email ou senha inválidos")

def logout_admin():
    st.session_state.admin_logado = False
    st.session_state.admin_email = None
    st.success("Você saiu da conta.")

def cadastrar_artista():
    st.header("Cadastrar Novo Artista")
    nome = st.text_input("Nome do Artista")
    categoria = st.selectbox("Categoria", ["Cantor", "Palestrante", "Pregador", "Outro"])
    descricao = st.text_area("Descrição do artista")
    foto_file = st.file_uploader("Foto do artista (PNG/JPG)", type=['png','jpg','jpeg'])
    servicos = []
    with st.expander("Adicionar Serviços"):
        n_servicos = st.number_input("Quantos serviços deseja adicionar?", min_value=1, step=1, key="num_servicos")
        for i in range(int(n_servicos)):
            nome_serv = st.text_input(f"Nome do serviço #{i+1}", key=f"serv_nome_{i}")
            preco_serv = st.number_input(f"Preço do serviço #{i+1}", min_value=0.0, format="%.2f", key=f"serv_preco_{i}")
            if nome_serv.strip() != "":
                servicos.append({'nome': nome_serv, 'preco': preco_serv})

    if st.button("Salvar Artista"):
        if not nome.strip():
            st.error("O nome do artista é obrigatório.")
            return
        foto = None
        if foto_file:
            foto = Image.open(foto_file)
        st.session_state.artistas.append({
            'nome': nome,
            'categoria': categoria,
            'descricao': descricao,
            'foto': foto,
            'servicos': servicos
        })
        st.success(f"Artista '{nome}' cadastrado com sucesso!")

def listar_artistas():
    st.header("Lista de Artistas")
    if not st.session_state.artistas:
        st.info("Nenhum artista cadastrado.")
        return
    for i, artista in enumerate(st.session_state.artistas):
        cols = st.columns([1,4,1])
        with cols[0]:
            if artista['foto']:
                st.image(artista['foto'], width=80)
            else:
                st.write("[Sem foto]")
        with cols[1]:
            st.subheader(artista['nome'])
            st.write(f"Categoria: {artista['categoria']}")
            st.write(f"Descrição: {artista['descricao']}")
            st.write("Serviços:")
            for s in artista['servicos']:
                st.write(f"- {s['nome']} - R$ {s['preco']:.2f}")
        with cols[2]:
            if st.button(f"Excluir", key=f"del_{i}"):
                st.session_state.artistas.pop(i)
                st.experimental_rerun()

def cadastrar_administrador():
    st.header("Cadastrar Novo Administrador (Apenas admin principal)")
    if not st.session_state.admins[st.session_state.admin_email]['principal']:
        st.warning("Somente o administrador principal pode cadastrar novos administradores.")
        return
    email_novo = st.text_input("Email do novo administrador")
    senha_nova = st.text_input("Senha", type="password")
    principal = st.checkbox("Administrador Principal?", value=False)
    if st.button("Cadastrar Administrador"):
        if not email_novo.strip() or not senha_nova.strip():
            st.error("Email e senha são obrigatórios.")
            return
        if email_novo in st.session_state.admins:
            st.error("Este email já está cadastrado.")
            return
        st.session_state.admins[email_novo] = {'senha': senha_nova, 'principal': principal}
        st.success(f"Administrador '{email_novo}' cadastrado com sucesso!")

def mostrar_dados_empresa():
    st.markdown("### Sobre a Empresa")
    mostrar_logo()
    st.write(st.session_state.empresa['nome'])
    st.write(st.session_state.empresa['descricao'])

def alterar_dados_empresa():
    st.header("Dados da Empresa (Admin Principal)")
    if not st.session_state.admins[st.session_state.admin_email]['principal']:
        st.warning("Somente o administrador principal pode alterar os dados da empresa.")
        return
    nome = st.text_input("Nome da empresa", value=st.session_state.empresa['nome'])
    descricao = st.text_area("Descrição da empresa", value=st.session_state.empresa['descricao'])
    foto_file = st.file_uploader("Alterar logotipo (PNG/JPG)", type=['png','jpg','jpeg'])
    if st.button("Salvar Dados"):
        st.session_state.empresa['nome'] = nome
        st.session_state.empresa['descricao'] = descricao
        if foto_file:
            st.session_state.empresa['logo'] = Image.open(foto_file)
        st.success("Dados da empresa atualizados!")

def verificar_conflito(artista_nome, data, inicio, fim):
    for ag in st.session_state.agendamentos:
        if ag['artista'] == artista_nome and ag['data'] == data:
            # Verifica se os horários conflitam
            inicio_existente = ag['hora_inicio']
            fim_existente = ag['hora_fim']
            if (inicio < fim_existente and fim > inicio_existente):
                return True
    return False

def agendar_evento():
    st.header("Agendamento de Evento")
    mostrar_dados_empresa()
    st.write("---")

    # Escolher artista
    nomes_artistas = [a['nome'] for a in st.session_state.artistas]
    artista_selecionado = st.selectbox("Escolha o artista", nomes_artistas)
    artista_obj = next((a for a in st.session_state.artistas if a['nome'] == artista_selecionado), None)

    # Mostrar serviços do artista
    servicos = artista_obj['servicos']
    nomes_servicos = [s['nome'] for s in servicos]
    servico_selecionado = st.selectbox("Escolha o serviço", nomes_servicos)
    servico_obj = next(s for s in servicos if s['nome'] == servico_selecionado)
    st.write(f"Preço: R$ {servico_obj['preco']:.2f}")

    data_evento = st.date_input("Data do evento", min_value=datetime.today())
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")

    if hora_fim <= hora_inicio:
        st.warning("Hora de término deve ser depois da hora de início.")

    # Dados do contratante
    st.subheader("Dados do contratante")
    nome_cliente = st.text_input("Nome completo")
    email_cliente = st.text_input("Email")
    telefone_cliente = st.text_input("Telefone")
    cidade_cliente = st.text_input("Cidade")

    if st.button("Agendar"):
        if not nome_cliente or not email_cliente or not telefone_cliente or not cidade_cliente:
            st.error("Preencha todos os dados do contratante.")
            return
        if verificar_conflito(artista_selecionado, data_evento, hora_inicio, hora_fim):
            st.error("Conflito: O artista já possui um evento nesse horário.")
            return
        novo_agendamento = {
            'artista': artista_selecionado,
            'servico': servico_selecionado,
            'preco': servico_obj['preco'],
            'data': data_evento,
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'cliente_nome': nome_cliente,
            'cliente_email': email_cliente,
            'cliente_telefone': telefone_cliente,
            'cliente_cidade': cidade_cliente,
            'data_agendamento': datetime.now()
        }
        st.session_state.agendamentos.append(novo_agendamento)
        st.success("Agendamento realizado com sucesso!")

def lista_agendamentos():
    st.header("Lista de Agendamentos")
    if not st.session_state.agendamentos:
        st.info("Nenhum agendamento registrado.")
        return
    for i, ag in enumerate(st.session_state.agendamentos):
        st.write(f"**Artista:** {ag['artista']} | **Serviço:** {ag['servico']} | **Data:** {ag['data'].strftime('%d/%m/%Y')}")
        st.write(f"Horário: {ag['hora_inicio'].strftime('%H:%M')} - {ag['hora_fim'].strftime('%H:%M')}")
        st.write(f"Cliente: {ag['cliente_nome']} | Email: {ag['cliente_email']} | Telefone: {ag['cliente_telefone']} | Cidade: {ag['cliente_cidade']}")
        st.write("---")

def menu_admin():
    st.sidebar.title(f"Bem-vindo, {st.session_state.admin_email}")
    if st.sidebar.button("Sair"):
        logout_admin()
        st.experimental_rerun()

    pagina = st.sidebar.radio("Menu", [
        "Dados da Empresa",
        "Cadastrar Artista",
        "Lista de Artistas",
        "Cadastrar Administrador",
        "Lista de Agendamentos"
    ])

    if pagina == "Dados da Empresa":
        alterar_dados_empresa()
    elif pagina == "Cadastrar Artista":
        cadastrar_artista()
    elif pagina == "Lista de Artistas":
        listar_artistas()
    elif pagina == "Cadastrar Administrador":
        cadastrar_administrador()
    elif pagina == "Lista de Agendamentos":
        lista_agendamentos()

# --- Interface pública (cliente) ---

def tela_agendamento_publico():
    st.title("Agende seu evento com nossos artistas")
    agendar_evento()

    st.markdown("---")
    # Botão para login do administrador
    if st.button("Login do Administrador"):
        st.session_state.mostrar_login_admin = True
        st.experimental_rerun()

    # Botão WhatsApp fixo (exemplo com link aberto)
    st.markdown(
        """
        <style>
        .whatsapp_float {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 40px;
            right: 40px;
            background-color: #25d366;
            color: #FFF;
            border-radius: 50px;
            text-align: center;
            font-size: 30px;
            box-shadow: 2px 2px 3px #999;
            z-index:100;
        }
        .whatsapp_float:hover {
            background-color:#128C7E;
            color:#fff;
        }
        </style>
        <a href="https://wa.me/5511999999999" class="whatsapp_float" target="_blank" title="WhatsApp">
            &#128222;
        </a>
        """, unsafe_allow_html=True)

# --- Fluxo principal ---

if st.session_state.mostrar_login_admin:
    login_admin()
else:
    if st.session_state.admin_logado:
        menu_admin()
    else:
        tela_agendamento_publico()
