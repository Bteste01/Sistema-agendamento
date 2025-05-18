import streamlit as st
from datetime import datetime
from PIL import Image

# Inicializa sessão
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin'}
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = None
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = ''
if 'empresa' not in st.session_state:
    st.session_state.empresa = {'nome': 'Grupo Reobote Serviços', 'descricao': '', 'logotipo': None}
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = [
        {
            "nome": "Bruno Cruz",
            "servicos": [{"nome": "Show musical", "preco": 2500.00}],
            "foto": None,
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor",
            "redes_sociais": {"Instagram": "https://instagram.com/brunocruz", "YouTube": "https://youtube.com/brunocruz"}
        },
        {
            "nome": "Skreps",
            "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
            "foto": None,
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante",
            "redes_sociais": {"Instagram": "https://instagram.com/skreps"}
        },
        {
            "nome": "Lú Almeida",
            "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
            "foto": None,
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora",
            "redes_sociais": {"Facebook": "https://facebook.com/lu.almeida"}
        }
    ]

# --- Interface Pública ---

st.title(st.session_state.empresa['nome'])
if st.session_state.empresa['logotipo']:
    st.image(st.session_state.empresa['logotipo'], width=100)
if st.session_state.empresa['descricao']:
    st.write(st.session_state.empresa['descricao'])

st.header("Agendar um Artista")

# Seleciona artista
nomes_artistas = [a['nome'] for a in st.session_state.artistas_disponiveis]
artista_selecionado = st.selectbox("Escolha um artista", nomes_artistas)

# Info artista
artista = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)
if artista['foto']:
    st.image(artista['foto'], width=150)
st.write("Descrição:", artista['descricao'])
st.write("Categoria:", artista['categoria'])

# Redes sociais do artista
if artista.get('redes_sociais'):
    st.write("Redes Sociais:")
    for rede, url in artista['redes_sociais'].items():
        st.markdown(f"- [{rede}]({url})")

# Serviços e preços
servicos_opcoes = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista['servicos']]
servico_selecionado = st.selectbox("Escolha o serviço", servicos_opcoes)

# Dados do cliente
nome_cliente = st.text_input("Seu nome")
email_cliente = st.text_input("Seu email")
telefone_cliente = st.text_input("Seu telefone")
cidade_cliente = st.text_input("Sua cidade")
data_evento = st.date_input("Data do evento")
hora_inicio = st.time_input("Hora de início")
hora_fim = st.time_input("Hora de término")

if st.button("Confirmar agendamento"):
    inicio = datetime.combine(data_evento, hora_inicio)
    fim = datetime.combine(data_evento, hora_fim)
    # Checa conflito
    conflito = any(
        ag['artista'] == artista_selecionado and
        not (fim <= ag['inicio'] or inicio >= ag['fim'])
        for ag in st.session_state.agendamentos
    )
    if conflito:
        st.error("Esse horário já está ocupado para este artista.")
    elif not (nome_cliente and email_cliente):
        st.error("Preencha seu nome e email.")
    else:
        st.session_state.agendamentos.append({
            'artista': artista_selecionado,
            'servico': servico_selecionado,
            'cliente': nome_cliente,
            'email': email_cliente,
            'telefone': telefone_cliente,
            'cidade': cidade_cliente,
            'inicio': inicio,
            'fim': fim
        })
        st.success("Agendamento realizado com sucesso!")

# Parcerias e vínculo
st.header("Parcerias com a Empresa")
st.text_input("Nome da empresa parceira", key="parceria_nome")
st.text_input("Email para contato da empresa", key="parceria_email")
st.text_area("Mensagem ou proposta", key="parceria_mensagem")
if st.button("Enviar proposta de parceria"):
    st.success("Proposta de parceria enviada! Entraremos em contato.")

st.header("Quero ser Assessorado")
st.text_input("Nome completo", key="vinculo_nome")
st.text_input("Email", key="vinculo_email")
st.text_area("Conte-nos sobre você e seu trabalho artístico", key="vinculo_info")
if st.button("Enviar solicitação de vínculo"):
    st.success("Solicitação enviada! Nossa equipe entrará em contato.")

# WhatsApp contato
if st.session_state.whatsapp:
    whatsapp_link = st.session_state.whatsapp.replace("+", "").replace(" ", "")
    st.markdown(f"[Fale conosco no WhatsApp](https://wa.me/{whatsapp_link})")

st.markdown("---")

# --- Login do Administrador ---
with st.expander("Área do Administrador"):
    if st.session_state.admin_logado is None:
        email_login = st.text_input("Email do administrador", key="login_email")
        senha_login = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", key="btn_login"):
            if email_login == st.session_state.admin_principal['email'] and senha_login == st.session_state.admin_principal['senha']:
                st.session_state.admin_logado = 'principal'
                st.success("Logado como administrador principal.")
            elif any(a['email'] == email_login and a['senha'] == senha_login for a in st.session_state.admins):
                st.session_state.admin_logado = email_login
                st.success("Logado como administrador.")
            else:
                st.error("Email ou senha inválidos.")
    else:
        st.write(f"Logado como: {st.session_state.admin_logado}")
        if st.button("Sair"):
            st.session_state.admin_logado = None

# --- Área do Administrador Principal ---
if st.session_state.admin_logado == 'principal':
    st.header("Painel do Administrador Principal")

    # Cadastrar novo artista
    st.subheader("Cadastrar Novo Artista")
    nome_artista = st.text_input("Nome do artista", key="novo_artista_nome")
    descricao_artista = st.text_area("Descrição", key="novo_artista_desc")
    categoria_artista = st.text_input("Categoria", key="novo_artista_categoria")

    # Upload foto
    foto_upload = st.file_uploader("Foto do artista (PNG/JPG)", type=['png', 'jpg'], key="novo_artista_foto")

    # Redes sociais
    redes_input = st.text_area("Redes sociais (formato: Nome=URL, um por linha)", key="novo_artista_redes")

    servico_nome = st.text_input("Nome do serviço", key="novo_artista_servico_nome")
    servico_preco = st.number_input("Preço do serviço (R$)", min_value=0.0, format="%.2f", key="novo_artista_servico_preco")

    if st.button("Cadastrar artista"):
        if not nome_artista.strip():
            st.error("Nome do artista é obrigatório.")
        else:
            redes_dict = {}
            for linha in redes_input.strip().split("\n"):
                if "=" in linha:
                    k, v = linha.split("=", 1)
                    redes_dict[k.strip()] = v.strip()
            foto = Image.open(foto_upload) if foto_upload else None
            novo_artista = {
                "nome": nome_artista.strip(),
                "descricao": descricao_artista.strip(),
                "categoria": categoria_artista.strip(),
                "foto": foto,
                "redes_sociais": redes_dict,
                "servicos": [{"nome": servico_nome.strip(), "preco": servico_preco}] if servico_nome.strip() else []
            }
            st.session_state.artistas_disponiveis.append(novo_artista)
            st.success(f"Artista {nome_artista} cadastrado com sucesso.")

    # Listar artistas para excluir
    st.subheader("Excluir Artista")
    nomes_artistas_admin = [a['nome'] for a in st.session_state.artistas_dispon
