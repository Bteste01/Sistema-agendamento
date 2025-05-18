import streamlit as st
from datetime import datetime
from PIL import Image

# Inicialização do estado
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin'}
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = None
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = '+5511999999999'  # Exemplo
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = [
        {
            "nome": "Bruno Cruz",
            "servicos": [{"nome": "Show musical", "preco": 2500.00}],
            "foto": None,
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor",
            "redes_sociais": {
                "Instagram": "https://instagram.com/brunocruz",
                "YouTube": "https://youtube.com/brunocruz"
            }
        },
        {
            "nome": "Skreps",
            "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
            "foto": None,
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante",
            "redes_sociais": {
                "LinkedIn": "https://linkedin.com/in/skreps",
                "Instagram": "https://instagram.com/skreps"
            }
        },
        {
            "nome": "Lú Almeida",
            "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
            "foto": None,
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora",
            "redes_sociais": {
                "Facebook": "https://facebook.com/lualmeida",
                "Instagram": "https://instagram.com/lualmeida"
            }
        }
    ]

# Título geral
st.title("Grupo Reobote Serviços")

# === ÁREA PÚBLICA ===

st.header("Agendamento de Artistas")

# Seleciona artista
artista_nomes = [a['nome'] for a in st.session_state.artistas_disponiveis]
artista_selecionado = st.selectbox("Escolha um artista", artista_nomes)

# Exibe informações do artista
artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)
if artista_info['foto']:
    st.image(artista_info['foto'], width=150)
st.write(f"**Descrição:** {artista_info['descricao']}")
st.write(f"**Categoria:** {artista_info['categoria']}")
st.write("**Redes sociais:**")
for rede, link in artista_info['redes_sociais'].items():
    st.markdown(f"- [{rede}]({link})")

# Seleção de serviço e mostra preço
servico_opcoes = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info['servicos']]
servico_escolhido = st.selectbox("Escolha o serviço", servico_opcoes)

# Dados do cliente para agendamento
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
        ag['artista'] == artista_selecionado and
        not (fim <= ag['inicio'] or inicio >= ag['fim'])
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
            'inicio': inicio,
            'fim': fim
        })
        st.success("Agendamento realizado com sucesso!")

# ÁREA PÚBLICA - PARCERIA
st.header("Parceria com a Empresa")
nome_empresa_parceria = st.text_input("Nome da empresa parceira", key="nome_empresa_parceria")
email_parceria = st.text_input("Email para contato", key="email_parceria")
mensagem_parceria = st.text_area("Mensagem ou proposta", key="mensagem_parceria")
if st.button("Enviar Proposta de Parceria"):
    st.success("Proposta enviada. Entraremos em contato!")

# ÁREA PÚBLICA - VÍNCULO DE ASSESSORIA
st.header("Vínculo de Assessoria para Novos Artistas")
nome_candidato = st.text_input("Nome completo", key="nome_candidato")
email_candidato = st.text_input("Email", key="email_candidato")
descricao_artista = st.text_area("Conte-nos sobre você e seu trabalho artístico", key="descricao_artista")
if st.button("Enviar Solicitação de Vínculo"):
    st.success("Solicitação enviada com sucesso! Entraremos em contato.")

# Botão do WhatsApp fixo no rodapé
whatsapp_link = f"https://wa.me/{st.session_state.whatsapp.replace('+', '').replace(' ', '')}"
st.markdown(f"[Fale conosco pelo WhatsApp]({whatsapp_link})")

# === LOGIN DO ADMINISTRADOR PRINCIPAL ===

st.markdown("---")
with st.expander("Área do Administrador"):
    if st.session_state.admin_logado:
        st.success(f"Logado como: {st.session_state.admin_logado}")
        if st.button("Logout"):
            st.session_state.admin_logado = None
    else:
        login_email = st.text_input("Email do administrador", key="login_email")
        login_senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar"):
            if (login_email == st.session_state.admin_principal['email'] and
                login_senha == st.session_state.admin_principal['senha']):
                st.session_state.admin_logado = 'Administrador Principal'
                st.success("Login como administrador principal realizado!")
            elif any(a['email'] == login_email and a['senha'] == login_senha for a in st.session_state.admins):
                st.session_state.admin_logado = login_email
                st.success("Login como administrador!")
            else:
                st.error("Credenciais inválidas.")

# === ÁREA DO ADMINISTRADOR PRINCIPAL ===
if st.session_state.admin_logado == 'Administrador Principal':
    st.header("Painel do Administrador Principal")

    # Cadastrar novo administrador
    st.subheader("Cadastrar Novo Administrador")
    novo_email = st.text_input("Email do novo administrador", key="novo_email")
    nova_senha = st.text_input("Senha do novo administrador", type="password", key="nova_senha")
    if st.button("Cadastrar Novo Administrador"):
        if any(a['email'] == novo_email for a in st.session_state.admins):
            st.warning("Este administrador já existe.")
        elif novo_email.strip() == '' or nova_senha.strip() == '':
            st.error("Email e senha não podem ser vazios.")
        else:
            st.session_state.admins.append({"email": novo_email, "senha": nova_senha})
            st.success("Novo administrador cadastrado com sucesso!")

    # Listar artistas cadastrados
    st.subheader("Lista de Artistas Cadastrados")
    for i, artista in enumerate(st.session_state.artistas_disponiveis):
        st.write(f"**{artista['nome']}** - {artista['categoria']}")
        if st.button(f"Excluir {artista['nome']}", key=f"excluir_{i}"):
            st.session_state.artistas_disponiveis.pop(i)
            st.experimental_rerun()

    # Listar agendamentos
    st.subheader("Agendamentos Realizados")
    if len(st.session_state.agendamentos) == 0:
        st.info("Nenhum agendamento realizado.")
    else:
        for ag in st.session_state.agendamentos:
            st.write(f"{ag['cliente']} agendou {ag['servico']} com {ag['artista']} em {ag['inicio']} até {ag['fim']} - {ag['cidade']} - {ag['telefone']}")
