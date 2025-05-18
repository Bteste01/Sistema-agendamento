import streamlit as st
from datetime import datetime, time
from PIL import Image
import json
import os

# --- Funções para salvar e carregar dados JSON ---
DATA_FILE = "dados_sistema.json"

def salvar_dados():
    dados = {
        "empresa": {
            "nome": st.session_state.empresa.get("nome", ""),
            "descricao": st.session_state.empresa.get("descricao", ""),
            "whatsapp": st.session_state.whatsapp,
        },
        "admins": st.session_state.admins,
        "admin_principal": st.session_state.admin_principal,
        "agendamentos": [
            {
                "artista": ag["artista"],
                "servico": ag["servico"],
                "cliente": ag["cliente"],
                "email": ag["email"],
                "telefone": ag["telefone"],
                "cidade": ag["cidade"],
                "inicio": ag["inicio"].isoformat(),
                "fim": ag["fim"].isoformat(),
            }
            for ag in st.session_state.agendamentos
        ],
        "artistas_disponiveis": [
            {
                "nome": a["nome"],
                "servicos": a["servicos"],
                "descricao": a.get("descricao", ""),
                "categoria": a.get("categoria", ""),
                "foto_bytes": a["foto_bytes"].decode('latin1') if a["foto_bytes"] else None,
            }
            for a in st.session_state.artistas_disponiveis
        ],
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados():
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)
    st.session_state.empresa = dados.get("empresa", {"nome":"","descricao":""})
    st.session_state.whatsapp = dados.get("empresa", {}).get("whatsapp", "")
    st.session_state.admins = dados.get("admins", [])
    st.session_state.admin_principal = dados.get("admin_principal", {"email": "admin@admin.com", "senha": "admin"})
    st.session_state.agendamentos = []
    for ag in dados.get("agendamentos", []):
        st.session_state.agendamentos.append({
            "artista": ag["artista"],
            "servico": ag["servico"],
            "cliente": ag["cliente"],
            "email": ag["email"],
            "telefone": ag["telefone"],
            "cidade": ag["cidade"],
            "inicio": datetime.fromisoformat(ag["inicio"]),
            "fim": datetime.fromisoformat(ag["fim"]),
        })
    st.session_state.artistas_disponiveis = []
    for a in dados.get("artistas_disponiveis", []):
        foto_bytes = a["foto_bytes"].encode('latin1') if a["foto_bytes"] else None
        st.session_state.artistas_disponiveis.append({
            "nome": a["nome"],
            "servicos": a["servicos"],
            "descricao": a.get("descricao", ""),
            "categoria": a.get("categoria", ""),
            "foto_bytes": foto_bytes,
        })

# --- Estado inicial ---
if "empresa" not in st.session_state:
    st.session_state.empresa = {"nome": "", "descricao": ""}
if "whatsapp" not in st.session_state:
    st.session_state.whatsapp = ""
if "admin_principal" not in st.session_state:
    st.session_state.admin_principal = {"email": "admin@admin.com", "senha": "admin"}
if "admins" not in st.session_state:
    st.session_state.admins = []
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = None
if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = []
if "artistas_disponiveis" not in st.session_state:
    # Exemplos iniciais, sem fotos
    st.session_state.artistas_disponiveis = [
        {
            "nome": "Bruno Cruz",
            "servicos": [{"nome": "Show musical", "preco": 2500.00}],
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor",
            "foto_bytes": None,
        },
        {
            "nome": "Skreps",
            "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante",
            "foto_bytes": None,
        },
        {
            "nome": "Lú Almeida",
            "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora",
            "foto_bytes": None,
        },
    ]

# Carregar dados salvos
carregar_dados()

# --- Função para exibir imagem a partir dos bytes ---
def foto_from_bytes(foto_bytes):
    if foto_bytes:
        return Image.open(io.BytesIO(foto_bytes))
    return None

# --- Interface pública: Agendamento ---
st.title("Grupo Reobote Serviços: Sistema de Agradecimento")

if st.session_state.empresa['nome']:
    st.image(foto_from_bytes(st.session_state.empresa.get('logotipo', None)) if st.session_state.empresa.get('logotipo', None) else None, width=100)
    st.subheader(st.session_state.empresa['nome'])
    st.caption(st.session_state.empresa['descricao'])

st.header("Agendar um Artista")

if not st.session_state.artistas_disponiveis:
    st.warning("Nenhum artista disponível no momento.")
else:
    artistas_nomes = [a["nome"] for a in st.session_state.artistas_disponiveis]
    artista_sel = st.selectbox("Escolha um artista", artistas_nomes)
    artista_info = next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista_sel)
    
    if artista_info["foto_bytes"]:
        st.image(foto_from_bytes(artista_info["foto_bytes"]), width=150)
    st.write("**Descrição:**", artista_info.get("descricao", ""))
    st.write("**Categoria:**", artista_info.get("categoria", ""))
    
    servicos_opcoes = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info["servicos"]]
    servico_sel = st.selectbox("Escolha o serviço", servicos_opcoes)
    
    nome_cliente = st.text_input("Seu nome")
    email_cliente = st.text_input("Email")
    telefone_cliente = st.text_input("Telefone")
    cidade_cliente = st.text_input("Cidade")
    data_evento = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início", value=time(18,0))
    hora_fim = st.time_input("Hora de término", value=time(19,0))
    
    if st.button("Confirmar Agendamento"):
        inicio_dt = datetime.combine(data_evento, hora_inicio)
        fim_dt = datetime.combine(data_evento, hora_fim)
        if fim_dt <= inicio_dt:
            st.error("Hora de término deve ser depois da hora de início.")
        else:
            conflito = any(
                ag["artista"] == artista_sel and
                not (fim_dt <= ag["inicio"] or inicio_dt >= ag["fim"])
                for ag in st.session_state.agendamentos
            )
            if conflito:
                st.error("Este horário já está ocupado para este artista.")
            elif not nome_cliente.strip() or not email_cliente.strip():
                st.error("Por favor, preencha seu nome e email.")
            else:
                st.session_state.agendamentos.append({
                    "artista": artista_sel,
                    "servico": servico_sel,
                    "cliente": nome_cliente,
                    "email": email_cliente,
                    "telefone": telefone_cliente,
                    "cidade": cidade_cliente,
                    "inicio": inicio_dt,
                    "fim": fim_dt,
                })
                salvar_dados()
                st.success("Agendamento realizado com sucesso!")

# --- Áreas públicas extras ---

st.markdown("---")
st.header("Parcerias com a Empresa")
with st.form("form_parceria"):
    nome_parceira = st.text_input("Nome da empresa parceira")
    email_parceira = st.text_input("Email para contato")
    mensagem_parceria = st.text_area("Mensagem ou proposta")
    enviar_parceria = st.form_submit_button("Enviar Proposta de Parceria")
    if enviar_parceria:
        # Aqui pode enviar por email ou salvar em arquivo - por simplicidade só mostra sucesso
        st.success("Proposta enviada! Entraremos em contato.")

st.markdown("---")
st.header("Quero ser Assessorado")
with st.form("form_assessoria"):
    nome_assess = st.text_input("Nome completo")
    email_assess = st.text_input("Email")
    descricao_assess = st.text_area("Conte-nos sobre você e seu trabalho artístico")
    enviar_assess = st.form_submit_button("Enviar Solicitação de Vínculo")
    if enviar_assess:
        st.success("Solicitação enviada! Aguarde nosso contato.")

st.markdown("---")
st.header("Atendimento Automatizado (Agrupamento)")
per
