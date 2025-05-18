import streamlit as st
from datetime import datetime
from PIL import Image
import json
import os

# --- Funções para persistência JSON ---
DATA_PATH = 'data'
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def salvar_dados(nome_arquivo, dados):
    caminho = os.path.join(DATA_PATH, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados(nome_arquivo, default):
    caminho = os.path.join(DATA_PATH, nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

# --- Estado Inicial ---
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = False

# Carregar dados ou usar padrão
st.session_state.empresa = carregar_dados('empresa.json', {
    "nome": "Grupo Reobote Serviços",
    "descricao": "",
    "logotipo": None,
    "whatsapp": ""
})

st.session_state.artistas = carregar_dados('artistas.json', [
    {
        "nome": "Bruno Cruz",
        "servicos": [{"nome": "Show musical", "preco": 2500.00}],
        "descricao": "Cantor e compositor com repertório variado.",
        "categoria": "Cantor",
        "redes_sociais": ["https://instagram.com/brunocruz", "https://facebook.com/brunocruz"]
    },
    {
        "nome": "Skreps",
        "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
        "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
        "categoria": "Palestrante",
        "redes_sociais": ["https://linkedin.com/in/skreps"]
    }
])

st.session_state.agendamentos = carregar_dados('agendamentos.json', [])

# Admin principal fixo
ADMIN_EMAIL = "admin@admin.com"
ADMIN_SENHA = "admin"

# --- Função para salvar todos dados ---
def salvar_todos_dados():
    salvar_dados('empresa.json', st.session_state.empresa)
    salvar_dados('artistas.json', st.session_state.artistas)
    salvar_dados('agendamentos.json', st.session_state.agendamentos)

# --- Interface Pública ---

st.title(st.session_state.empresa["nome"])

if st.session_state.empresa["logotipo"]:
    try:
        img = Image.open(st.session_state.empresa["logotipo"])
        st.image(img, width=150)
    except:
        pass

if st.session_state.empresa["descricao"]:
    st.write(st.session_state.empresa["descricao"])

st.header("Agendar um Artista")

# Selecionar artista
nomes_artistas = [a['nome'] for a in st.session_state.artistas]
artista_escolhido = st.selectbox("Escolha o artista", nomes_artistas)

# Detalhes artista selecionado
artista_info = next((a for a in st.session_state.artistas if a['nome'] == artista_escolhido), None)
if artista_info:
    st.write(f"**Descrição:** {artista_info['descricao']}")
    st.write(f"**Categoria:** {artista_info['categoria']}")
    if artista_info.get("redes_sociais"):
        st.write("**Redes Sociais:**")
        for rede in artista_info["redes_sociais"]:
            st.markdown(f"- [{rede}]({rede})")

    # Serviços disponíveis
    servicos_descr = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info['servicos']]
    servico_escolhido = st.selectbox("Escolha o serviço", servicos_descr)

    # Dados do cliente
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

        # Verificar conflito de horário
        conflito = any(
            ag['artista'] == artista_escolhido and
            not (fim <= datetime.fromisoformat(ag['inicio']) or inicio >= datetime.fromisoformat(ag['fim']))
            for ag in st.session_state.agendamentos
        )
        if conflito:
            st.error("Esse horário já está ocupado para este artista.")
        elif not nome_cliente or not email_cliente:
            st.error("Por favor, preencha seu nome e email.")
        else:
            agendamento = {
                "artista": artista_escolhido,
                "servico": servico_escolhido,
                "cliente": nome_cliente,
                "email": email_cliente,
                "telefone": telefone_cliente,
                "cidade": cidade_cliente,
                "inicio": inicio.isoformat(),
                "fim": fim.isoformat()
            }
            st.session_state.agendamentos.append(agendamento)
            salvar_dados('agendamentos.json', st.session_state.agendamentos)
            st.success("Agendamento confirmado!")

# Botão WhatsApp fixo se existir
if st.session_state.empresa.get("whatsapp"):
    whatsapp = st.session_state.empresa["whatsapp"].replace(" ", "").replace("+", "")
    st.markdown(f"[Fale conosco pelo WhatsApp](https://wa.me/{whatsapp})")

st.markdown("---")
# Link para área admin
with st.expander("Área do Administrador - Login"):
    login_email = st.text_input("Email do administrador")
    login_senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if login_email == ADMIN_EMAIL and login_senha == ADMIN_SENHA:
            st.session_state.admin_logado = True
            st.success("Logado como Administrador Principal!")
        else:
            st.error("Credenciais incorretas.")

# --- Interface Administrador ---

if st.session_state.admin_logado:

    st.header("Painel do Administrador Principal")

    # Dados da empresa
    st.subheader("Configurações da Empresa")
    nome_emp = st.text_input("Nome da empresa", value=st.session_state.empresa["nome"])
    descricao_emp = st.text_area("Descrição da empresa", value=st.session_state.empresa["descricao"])
    logotipo_emp = st.file_uploader("Logotipo da empresa (PNG/JPG)", type=["png", "jpg"])

    whatsapp_emp = st.text_input("WhatsApp para contato (com código do país)", value=st.session_state.empresa.get("whatsapp", ""))

    if st.button("Salvar dados da empresa"):
        st.session_state.empresa["nome"] = nome_emp
        st.session_state.empresa["descricao"] = descricao_emp
        if logotipo_emp:
            # Salvar imagem em disco e guardar caminho
            img = Image.open(logotipo_emp)
            caminho_logo = os.path.join(DATA_PATH, "logo.png")
            img.save(caminho_logo)
            st.session_state.empresa["logotipo"] = caminho_logo
        st.session_state.empresa["whatsapp"] = whatsapp_emp
        salvar_dados('empresa.json', st.session_state.empresa)
        st.success("Dados da empresa atualizados!")

    st.markdown("---")

    # Gerenciar artistas
    st.subheader("Gerenciar Artistas")

    artistas_lista = st.session_state.artistas
    nomes_artistas = [a['nome'] for a in artistas_lista]

    # Escolher artista para editar/excluir
    artista_sel = st.selectbox("Selecionar artista para editar/excluir", nomes_artistas)

    artista_atual = next((a for a in artistas_lista if a['nome'] == artista_sel), None)
    if artista_atual:
        nome_artista = st.text_input("Nome do artista", value=artista_atual["nome"])
        categoria_artista = st.text_input("Categoria", value=artista_atual.get("categoria", ""))
        descricao_artista = st.text_area("Descrição", value=artista_atual.get("descricao", ""))
        
        # Redes sociais - mostrar lista e permitir edição
        redes_sociais = artista_atual.get("redes_sociais", [])
        st.write("Redes Sociais (URLs):")
        for i in range(len(redes_sociais)):
            redes_sociais[i] = st.text_input(f"Rede social {i+1}", value=redes_sociais[i], key=f"rede_{i}")
        # Adicionar nova rede social
        if st.button("Adicionar Rede Social"):
            redes_sociais.append("")
