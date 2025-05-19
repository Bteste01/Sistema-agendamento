import streamlit as st
from datetime import datetime
from PIL import Image
import json
import os

# Funções para salvar e carregar dados
CAMINHO_ARQUIVO = "dados.json"

def salvar_dados():
    dados = {
        "agendamentos": st.session_state.agendamentos,
        "artistas_disponiveis": st.session_state.artistas_disponiveis,
        "admins": st.session_state.admins
    }
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar_dados():
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            st.session_state.agendamentos = dados.get("agendamentos", [])
            st.session_state.artistas_disponiveis = dados.get("artistas_disponiveis", [])
            st.session_state.admins = dados.get("admins", [])

# Inicializa estados
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
    carregar_dados()
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin123'}
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = '+5599999999999'
if 'empresa' not in st.session_state:
    st.session_state.empresa = {'nome': 'Grupo Reobote Serviços', 'descricao': 'Sistema de Agendamento e Assessoria'}
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = []

# Interface pública
st.title(st.session_state.empresa['nome'])
st.write(st.session_state.empresa['descricao'])

st.header("Agendar um Artista")

if not st.session_state.artistas_disponiveis:
    st.info("Nenhum artista cadastrado ainda.")
else:
    artista_nomes = [a['nome'] for a in st.session_state.artistas_disponiveis]
    artista_selecionado = st.selectbox("Escolha um artista", artista_nomes)
    artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)

    if artista_info['foto']:
        st.image(artista_info['foto'], width=150)
    st.write("**Descrição:**", artista_info['descricao'])
    st.write("**Categoria:**", artista_info['categoria'])

    if artista_info['redes']:
        st.write("**Redes sociais:**")
        for rede in artista_info['redes']:
            st.markdown(f"- [{rede}]({rede})")

    servico_opcoes = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info['servicos']]
    servico_escolhido = st.selectbox("Escolha o serviço", servico_opcoes)

    nome_cliente = st.text_input("Seu nome")
    email_cliente = st.text_input("Email")
    telefone_cliente = st.text_input("Telefone")
    cidade_cliente = st.text_input("Cidade")
    data_evento = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")

    if st.button("Confirmar Agendamento"):
        inicio = datetime.combine(data_evento, hora_inicio)
        fim = datetime.combine(data_evento, hora_fim)
        conflito = any(
            ag['artista'] == artista_selecionado and not (fim <= ag['inicio'] or inicio >= ag['fim'])
            for ag in st.session_state.agendamentos
        )
        if conflito:
            st.error("Esse horário já está ocupado para este artista.")
        elif not nome_cliente or not email_cliente:
            st.error("Por favor, preencha seu nome e email.")
        else:
            st.session_state.agendamentos.append({
                'artista': artista_selecionado,
                'servico': servico_escolhido,
                'cliente': nome_cliente,
                'email': email_cliente,
                'telefone': telefone_cliente,
                'cidade': cidade_cliente,
                'inicio': inicio.isoformat(),
                'fim': fim.isoformat()
            })
            salvar_dados()
            st.success("Agendamento realizado com sucesso!")

st.markdown("---")

st.header("Parcerias com a Empresa")
nome_parceira = st.text_input("Nome da Empresa Parceira", key="parceria_nome")
email_parceira = st.text_input("Email para Contato", key="parceria_email")
mensagem_parceira = st.text_area("Mensagem ou Proposta", key="parceria_mensagem")
if st.button("Enviar Proposta de Parceria"):
    if nome_parceira and email_parceira:
        st.success("Proposta de parceria enviada com sucesso!")
    else:
        st.error("Preencha nome e email para enviar a proposta.")

st.markdown("---")

st.header("Quero ser Assessorado")
nome_assessorado = st.text_input("Nome Completo", key="assessoria_nome")
email_assessorado = st.text_input("Email", key="assessoria_email")
descricao_assessorado = st.text_area("Conte-nos sobre você e seu trabalho artístico", key="assessoria_descricao")
if st.button("Enviar Solicitação de Vínculo"):
    if nome_assessorado and email_assessorado:
        st.success("Solicitação de vínculo enviada com sucesso!")
    else:
        st.error("Preencha nome e email para enviar a solicitação.")

st.markdown("---")

if st.session_state.whatsapp:
    whatsapp_link = f"https://wa.me/{st.session_state.whatsapp.replace('+', '').replace(' ', '')}"
    st.markdown(f"[Fale conosco no WhatsApp]({whatsapp_link})", unsafe_allow_html=True)

st.markdown("---")

with st.expander("Área do Administrador"):
    login_email = st.text_input("Email do administrador", key="login_email")
    login_senha = st.text_input("Senha", type="password", key="login_senha")
    if st.button("Entrar", key="botao_entrar"):
        if login_email == st.session_state.admin_principal['email'] and login_senha == st.session_state.admin_principal['senha']:
            st.session_state.admin_logado = 'principal'
            st.success("Login como administrador principal!")
        elif any(a['email'] == login_email and a['senha'] == login_senha for a in st.session_state.admins):
            st.session_state.admin_logado = login_email
            st.success("Login como administrador!")
        else:
            st.error("Credenciais inválidas.")

if st.session_state.get('admin_logado') == 'principal':
    st.header("Painel do Administrador Principal")

    st.subheader("Cadastrar Novo Administrador")
    novo_admin_email = st.text_input("Email do novo administrador", key="novo_admin_email")
    novo_admin_senha = st.text_input("Senha do novo administrador", key="novo_admin_senha")
    if st.button("Cadastrar Administrador"):
        if novo_admin_email and novo_admin_senha:
            st.session_state.admins.append({"email": novo_admin_email, "senha": novo_admin_senha})
            salvar_dados()
            st.success("Novo administrador cadastrado!")
        else:
            st.error("Preencha email e senha.")

    st.subheader("Cadastrar Novo Artista")
    nome_artista = st.text_input("Nome do artista")
    descricao_artista = st.text_area("Descrição")
    categoria_artista = st.text_input("Categoria")
    redes_artista = st.text_area("Redes sociais (separadas por vírgula)")
    servicos = []
    nome_servico = st.text_input("Nome do serviço")
    preco_servico = st.number_input("Preço do serviço", min_value=0.0, step=0.01)
    if st.button("Adicionar serviço ao artista"):
        servicos.append({"nome": nome_servico, "preco": preco_servico})

    foto_upload = st.file_uploader("Foto do artista", type=["jpg", "png"])
    foto = Image.open(foto_upload) if foto_upload else None
    if st.button("Salvar Artista"):
        if nome_artista and descricao_artista:
            novo_artista = {
                "nome": nome_artista,
                "descricao": descricao_artista,
                "categoria": categoria_artista,
                "redes": [r.strip() for r in redes_artista.split(",")],
                "servicos": servicos,
                "foto": None  # Fotos não são serializáveis, precisam de outro tratamento
            }
            st.session_state.artistas_disponiveis.append(novo_artista)
            salvar_dados()
            st.success("Artista cadastrado com sucesso!")

    st.subheader("Excluir Artista")
    nomes_artistas = [a['nome'] for a in st.session_state.artistas_disponiveis]
    artista_excluir = st.selectbox("Selecione o artista para excluir", nomes_artistas)
    if st.button("Excluir Artista"):
        st.session_state.artistas_disponiveis = [a for a in st.session_state.artistas_disponiveis if a['nome'] != artista_excluir]
        salvar_dados()
        st.success("Artista excluído com sucesso!")
    
