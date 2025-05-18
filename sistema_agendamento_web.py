import streamlit as st
from datetime import datetime
from PIL import Image
import io
import json
import os

DATA_FILE = "dados_sistema.json"

# --- Funções para salvar/carregar dados ---

def salvar_dados():
    dados = {
        "agendamentos": st.session_state.agendamentos,
        "admins": st.session_state.admins,
        "admin_principal": st.session_state.admin_principal,
        "empresa": {
            "nome": st.session_state.empresa['nome'],
            "descricao": st.session_state.empresa['descricao'],
            "logotipo": None,
        },
        "whatsapp": st.session_state.whatsapp,
        "artistas_disponiveis": [],
    }
    import base64
    if st.session_state.empresa['logotipo']:
        buffer = io.BytesIO()
        st.session_state.empresa['logotipo'].save(buffer, format='PNG')
        logo_b64 = base64.b64encode(buffer.getvalue()).decode()
        dados['empresa']['logotipo'] = logo_b64
    else:
        dados['empresa']['logotipo'] = None

    artistas_serializados = []
    for a in st.session_state.artistas_disponiveis:
        foto_b64 = None
        if a['foto']:
            buffer = io.BytesIO()
            a['foto'].save(buffer, format='PNG')
            foto_b64 = base64.b64encode(buffer.getvalue()).decode()
        artistas_serializados.append({
            "nome": a['nome'],
            "servicos": a['servicos'],
            "foto": foto_b64,
            "descricao": a['descricao'],
            "categoria": a['categoria']
        })
    dados['artistas_disponiveis'] = artistas_serializados

    with open(DATA_FILE, "w") as f:
        json.dump(dados, f)

def carregar_dados():
    if not os.path.exists(DATA_FILE):
        return False
    import base64
    with open(DATA_FILE, "r") as f:
        dados = json.load(f)
    st.session_state.agendamentos = dados.get("agendamentos", [])
    st.session_state.admins = dados.get("admins", [])
    st.session_state.admin_principal = dados.get("admin_principal", {'email':'admin@admin.com', 'senha':'admin'})
    st.session_state.empresa['nome'] = dados.get("empresa", {}).get('nome', '')
    st.session_state.empresa['descricao'] = dados.get("empresa", {}).get('descricao', '')
    logo_b64 = dados.get("empresa", {}).get('logotipo')
    if logo_b64:
        logo_bytes = base64.b64decode(logo_b64)
        st.session_state.empresa['logotipo'] = Image.open(io.BytesIO(logo_bytes))
    else:
        st.session_state.empresa['logotipo'] = None
    st.session_state.whatsapp = dados.get("whatsapp", "")
    artistas = dados.get("artistas_disponiveis", [])
    artistas_carregados = []
    for a in artistas:
        foto = None
        if a.get("foto"):
            foto_bytes = base64.b64decode(a["foto"])
            foto = Image.open(io.BytesIO(foto_bytes))
        artistas_carregados.append({
            "nome": a.get("nome", ""),
            "servicos": a.get("servicos", []),
            "foto": foto,
            "descricao": a.get("descricao", ""),
            "categoria": a.get("categoria", "")
        })
    st.session_state.artistas_disponiveis = artistas_carregados
    return True

# --- Inicialização do estado ---
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin'}
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = None
if 'empresa' not in st.session_state:
    st.session_state.empresa = {'nome': '', 'descricao': '', 'logotipo': None}
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = ''
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

carregar_dados()

# --- Interface pública ---
st.title("Grupo Reobote Serviços")

if st.session_state.empresa['nome']:
    if st.session_state.empresa['logotipo']:
        st.image(st.session_state.empresa['logotipo'], width=120)
    st.subheader(st.session_state.empresa['nome'])
    st.caption(st.session_state.empresa['descricao'])

st.header("Agende um Artista")

nomes_artistas = [a['nome'] for a in st.session_state.artistas_disponiveis]
if not nomes_artistas:
    st.warning("Nenhum artista disponível no momento.")
else:
    artista_selecionado = st.selectbox("Escolha um artista", nomes_artistas)
    artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)

    if artista_info['foto']:
        st.image(artista_info['foto'], width=150)
    st.write(f"**Descrição:** {artista_info['descricao']}")
    st.write(f"**Categoria:** {artista_info['categoria']}")

    servicos_opcoes = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info['servicos']]
    servico_selecionado = st.selectbox("Escolha o serviço", servicos_opcoes)

    nome_cliente = st.text_input("Seu nome")
    email_cliente = st.text_input("Seu email")
    telefone_cliente = st.text_input("Seu telefone")
    cidade_cliente = st.text_input("Sua cidade")
    data_evento = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")

    if st.button("Confirmar Agendamento"):
        inicio = datetime.combine(data_evento, hora_inicio)
        fim = datetime.combine(data_evento, hora_fim)
        if fim <= inicio:
            st.error("Hora de término deve ser após a hora de início.")
        else:
            conflito = any(
                ag['artista'] == artista_selecionado and
                not (fim <= datetime.fromisoformat(ag['inicio']) or inicio >= datetime.fromisoformat(ag['fim']))
                for ag in st.session_state.agendamentos
            )
            if conflito:
                st.error("Já existe um agendamento neste horário para este artista.")
            elif not nome_cliente.strip() or not email_cliente.strip():
                st.error("Por favor, preencha seu nome e email.")
            else:
                novo_agendamento = {
                    "artista": artista_selecionado,
                    "servico": servico_selecionado,
                    "cliente": nome_cliente,
                    "email": email_cliente,
                    "telefone": telefone_cliente,
                    "cidade": cidade_cliente,
                    "inicio": inicio.isoformat(),
                    "fim": fim.isoformat()
                }
                st.session_state.agendamentos.append(novo_agendamento)
                salvar_dados()
                st.success("Agendamento realizado com sucesso!")

# --- Parcerias ---
st.header("Parcerias com a Empresa")
with st.form("form_parceria"):
    nome_empresa_parceria = st.text_input("Nome da empresa parceira")
    email_parceria = st.text_input("Email para contato")
    mensagem_parceria = st.text_area("Mensagem ou proposta")
    enviar_parceria = st.form_submit_button("Enviar Proposta de Parceria")
if enviar_parceria:
    st.success("Proposta de parceria enviada! Entraremos em contato em breve.")

# --- Vínculo de Assessoria ---
st.header("Quero ser Assessorado")
with st.form("form_assessoria"):
    nome_assessorado = st.text_input("Nome completo")
    email_assessoria = st.text_input("Email")
    mensagem_assessoria = st.text_area("Conte-nos sobre você e seu trabalho artístico")
    enviar_assessoria = st.form_submit_button("Enviar Solicitação de Vínculo")
if enviar_assessoria:
    st.success("Solicitação enviada! Entraremos em contato em breve.")

# --- WhatsApp contato ---
if st.session_state.wh
