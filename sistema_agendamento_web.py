# sistema_agendamento_web.py

import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import base64
import io

# Dados simulados (memória temporária)
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admins' not in st.session_state:
    st.session_state.admins = {'admin@admin.com': 'admin'}
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = False
if 'parcerias' not in st.session_state:
    st.session_state.parcerias = []
if 'vinculos' not in st.session_state:
    st.session_state.vinculos = []

artistas_disponiveis = [
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
        "descricao": "Palestrante e influenciador.",
        "categoria": "Palestrante"
    },
    {
        "nome": "Lú Almeida",
        "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
        "foto": None,
        "descricao": "Cantora gospel para eventos religiosos.",
        "categoria": "Pregadora"
    }
]

# Função para verificar conflito de horário
def tem_conflito(artista, data, inicio, fim):
    for ag in st.session_state.agendamentos:
        if ag['artista'] == artista and ag['data'] == data:
            if not (fim <= ag['inicio'] or inicio >= ag['fim']):
                return True
    return False

# Função IA simulada de atendimento
def ia_responde(pergunta):
    perguntas_frequentes = {
        "como agendar": "Você pode agendar um artista pela aba de Agendamento público.",
        "quais os preços": "Os preços estão listados ao lado dos nomes dos artistas.",
        "como me tornar parceiro": "Acesse a aba Parceria e envie seus dados.",
        "assessoria": "Acesse a aba Vínculo de Assessoria para solicitar ingresso."
    }
    pergunta = pergunta.lower()
    for chave, resposta in perguntas_frequentes.items():
        if chave in pergunta:
            return resposta
    return "Desculpe, não entendi sua pergunta. Tente reformular."

st.title("Sistema de Agendamento de Artistas")

# Telas públicas
menu = st.sidebar.radio("Menu", ["Agendamento", "Parceria", "Vínculo de Assessoria", "Agrupamento (IA)", "Área do Administrador"])

if menu == "Agendamento":
    st.header("Agendamento de Artistas")
    st.write("Bem-vindo ao agendamento! Escolha um artista, serviço e horário disponível.")

    artista_selecionado = st.selectbox("Artista", [a['nome'] for a in artistas_disponiveis])
    artista = next(a for a in artistas_disponiveis if a['nome'] == artista_selecionado)

    servico = st.selectbox("Serviço", [s['nome'] for s in artista['servicos']])
    preco = next(s['preco'] for s in artista['servicos'] if s['nome'] == servico)
    st.write(f"**Preço:** R$ {preco:.2f}")

    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    telefone = st.text_input("Telefone")
    cidade = st.text_input("Cidade")

    data = st.date_input("Data do evento", min_value=datetime.today())
    inicio = st.time_input("Início do evento")
    fim = st.time_input("Término do evento")

    if st.button("Confirmar Agendamento"):
        if tem_conflito(artista['nome'], data, inicio, fim):
            st.error("Este horário já está ocupado para este artista. Escolha outro.")
        else:
            st.session_state.agendamentos.append({
                "artista": artista['nome'],
                "servico": servico,
                "cliente": nome,
                "email": email,
                "telefone": telefone,
                "cidade": cidade,
                "data": data,
                "inicio": inicio,
                "fim": fim
            })
            st.success("Agendamento realizado com sucesso!")

    st.markdown("---")
    st.markdown("**Fale conosco no WhatsApp:**")
    st.markdown("[Clique aqui para abrir o WhatsApp](https://wa.me/5511999999999)")

elif menu == "Parceria":
    st.header("Proposta de Parceria")
    nome_empresa = st.text_input("Nome da empresa")
    nome_resp = st.text_input("Nome do responsável")
    email_parc = st.text_input("Email para contato")
    tel_parc = st.text_input("Telefone")
    tipo = st.text_input("Tipo de parceria")
    mensagem = st.text_area("Mensagem")

    if st.button("Enviar proposta"):
        st.session_state.parcerias.append({
            "empresa": nome_empresa,
            "responsavel": nome_resp,
            "email": email_parc,
            "telefone": tel_parc,
            "tipo": tipo,
            "mensagem": mensagem
        })
        st.success("Proposta enviada com sucesso!")

elif menu == "Vínculo de Assessoria":
    st.header("Solicitação de Vínculo com Assessoria")
    nome_artistico = st.text_input("Nome artístico")
    categoria = st.text_input("Categoria (Cantor, Palestrante...)")
    estilo = st.text_input("Estilo musical ou atuação")
    contato_email = st.text_input("Email")
    contato_tel = st.text_input("Telefone")
    portfolio = st.text_input("Link do portfólio")
    foto = st.file_uploader("Foto do artista", type=["jpg", "png"])
    apresentacao = st.text_area("Mensagem de apresentação")

    if st.button("Solicitar vínculo"):
        st.session_state.vinculos.append({
            "nome": nome_artistico,
            "categoria": categoria,
            "estilo": estilo,
            "email": contato_email,
            "telefone": contato_tel,
            "portfolio": portfolio,
            "foto": foto,
            "apresentacao": apresentacao
        })
        st.success("Solicitação enviada com sucesso!")

elif menu == "Agrupamento (IA)":
    st.header("Atendimento Automático")
    pergunta = st.text_input("Digite sua pergunta")
    if st.button("Perguntar"):
        resposta = ia_responde(pergunta)
        st.info(resposta)

elif menu == "Área do Administrador":
    if not st.session_state.admin_logado:
        st.subheader("Login do Administrador")
        login = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if st.session_state.admins.get(login) == senha:
                st.session_state.admin_logado = True
                st.success("Login realizado com sucesso!")
            else:
                st.error("Credenciais inválidas")

    if st.session_state.admin_logado:
        st.subheader("Área do Administrador")
        st.write("Agendamentos confirmados:")
        for ag in st.session_state.agendamentos:
            st.markdown(f"**{ag['data']} - {ag['artista']} ({ag['servico']})** - {ag['inicio']} até {ag['fim']}, Cliente: {ag['cliente']} - {ag['cidade']}")

        if st.checkbox("Visualizar solicitações de parceria"):
            for p in st.session_state.parcerias:
                st.write(p)

        if st.checkbox("Visualizar solicitações de vínculo de assessoria"):
            for v in st.session_state.vinculos:
                st.write(v)

        if st.button("Sair do sistema"):
            st.session_state.admin_logado = False
