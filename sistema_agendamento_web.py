import streamlit as st
from datetime import datetime
from PIL import Image

# Estado inicial
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin123'}
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = '+5599999999999'  # Seu WhatsApp aqui
if 'empresa' not in st.session_state:
    st.session_state.empresa = {'nome': 'Grupo Reobote Serviços', 'descricao': 'Sistema de Agendamento e Assessoria'}
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = [
        {
            "nome": "Bruno Cruz",
            "servicos": [{"nome": "Show musical", "preco": 2500.00}],
            "foto": None,
            "descricao": "Cantor e compositor com repertório variado.",
            "categoria": "Cantor",
            "redes": ["https://instagram.com/brunocruz", "https://facebook.com/brunocruz"]
        },
        {
            "nome": "Skreps",
            "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}],
            "foto": None,
            "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
            "categoria": "Palestrante",
            "redes": ["https://instagram.com/skreps"]
        },
        {
            "nome": "Lú Almeida",
            "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}],
            "foto": None,
            "descricao": "Cantora gospel com experiência em eventos religiosos.",
            "categoria": "Pregadora",
            "redes": ["https://facebook.com/lu.almeida"]
        }
    ]

# Título e descrição da empresa
st.title(st.session_state.empresa['nome'])
st.write(st.session_state.empresa['descricao'])

# --- Área Pública: Agendamento ---
st.header("Agendar um Artista")

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

st.markdown("---")

# --- Área Pública: Parcerias ---
st.header("Parcerias com a Empresa")
nome_parceira = st.text_input("Nome da Empresa Parceira", key="parceria_nome")
email_parceira = st.text_input("Email para Contato", key="parceria_email")
mensagem_parceira = st.text_area("Mensagem ou Proposta", key="parceria_mensagem")
if st.button("Enviar Proposta de Parceria"):
    if nome_parceira and email_parceira:
        st.success("Proposta de parceria enviada com sucesso!")
        # Aqui poderia salvar ou enviar por email
    else:
        st.error("Preencha nome e email para enviar a proposta.")

st.markdown("---")

# --- Área Pública: Vínculo de Assessoria ---
st.header("Quero ser Assessorado")
nome_assessorado = st.text_input("Nome Completo", key="assessoria_nome")
email_assessorado = st.text_input("Email", key="assessoria_email")
descricao_assessorado = st.text_area("Conte-nos sobre você e seu trabalho artístico", key="assessoria_descricao")
if st.button("Enviar Solicitação de Vínculo"):
    if nome_assessorado and email_assessorado:
        st.success("Solicitação de vínculo enviada com sucesso!")
        # Aqui poderia salvar ou enviar por email
    else:
        st.error("Preencha nome e email para enviar a solicitação.")

st.markdown("---")

# WhatsApp fixo no rodapé
if st.session_state.whatsapp:
    whatsapp_link = f"https://wa.me/{st.session_state.whatsapp.replace('+', '').replace(' ', '')}"
    st.markdown(f"[Fale conosco no WhatsApp]({whatsapp_link})", unsafe_allow_html=True)

st.markdown("---")

# --- Área do Administrador ---
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

# --- Painel do Administrador Principal ---
if st.session_state.get('admin_logado') == 'principal':
    st.header("Painel do Administrador Principal")

    # Cadastrar novo administrador
    st.subheader("Cadastrar Novo Administrador")
    novo_admin_email = st.text_input("Email do novo administrador", key="novo_admin_email")
    novo_admin_senha = st.text_input("Senha do novo administrador", type="password", key="novo_admin_senha")
    if st.button("Cadastrar Novo Administrador"):
        if not novo_admin_email.strip() or not novo_admin_senha.strip():
            st.error("Email e senha são obrigatórios para cadastrar um administrador.")
        else:
            if any(admin['email'] == novo_admin_email for admin in st.session_state.admins):
                st.error("Esse administrador já existe.")
            else:
                st.session_state.admins.append({'email': novo_admin_email, 'senha': novo_admin_senha})
                st.success(f"Administrador {novo_admin_email} cadastrado com sucesso!")

    st.markdown("---")

    # Cadastrar novo artista com múltiplos serviços
    st.subheader("Cadastrar Novo Artista")
    nome_artista_novo = st.text_input("Nome do artista", key="novo_artista_nome")
    descricao_artista_novo = st.text_area("Descrição do artista", key="novo_artista_descricao")
    categoria_artista_novo = st.text_input("Categoria do artista", key="novo_artista_categoria")
    foto_artista_novo = st.file_uploader("Foto do artista (png, jpg)", type=["png", "jpg"], key="novo_artista_foto")
    redes_artista_novo = st.text_area("Redes sociais (URLs, separadas por vírgula)", key="novo_artista_redes")

    st.write("Cadastre os serviços do artista:")
    if 'servicos_temp' not in st.session_state:
        st.session_state.servicos_temp = []

    nome_servico = st.text_input("Nome do serviço", key="novo_servico_nome")
    preco_servico = st.number_input("Preço do serviço (R$)", min_value=0.0, step=0.01, key="novo_servico_preco")

    if st.button("Adicionar serviço"):
        if not nome_servico.strip():
            st.error("O nome do serviço é obrigatório.")
        else:
            st.session_state.servicos_temp.append({"nome": nome_servico, "preco": preco_servico})
            st.success(f"Serviço '{nome_servico}' adicionado para o artista.")

    if st.button("Cadastrar Artista"):
        if not nome_artista_novo or not descricao_artista_novo or not categoria_artista_novo:
            st.error("Preencha todos os campos obrigatórios.")
        elif not st.session_state.servicos_temp:
            st.error("Cadastre pelo menos um serviço para o artista.")
        else:
            st.session_state.artistas_disponiveis.append({
                "nome": nome_artista_novo,
                "servicos": st.session_state.servicos_temp,
                "foto": foto_artista_novo,
                "descricao": descricao_artista_novo,
                "categoria": categoria_artista_novo,
                "redes": [r.strip() for r in redes_artista_novo.split(",") if r.strip()]
            })
            st.success(f"Artista '{nome_artista_novo}' cadastrado com sucesso!")
            st.session_state.servicos_temp = []

    st.markdown("---")

    # Listar e excluir artistas
    st.subheader("Artistas Cadastrados")
    for idx, artista in enumerate(st.session_state.artistas_disponiveis):
        with st.expander(f"{artista['nome']}"):
            st.write("Categoria:", artista["categoria"])
            st.write("Descrição:", artista["descricao"])
            if artista["redes"]:
                for rede in artista["redes"]:
                    st.markdown(f"- [{rede}]({rede})")
            for s in artista["servicos"]:
                st.write(f"Serviço: {s['nome']} - R$ {s['preco']:.2f}")
            if st.button(f"Excluir {artista['nome']}", key=f"excluir_{idx}"):
                st.session_state.artistas_disponiveis.pop(idx)
                st.success(f"Artista '{artista['nome']}' excluído com sucesso!")
                st.experimental_rerun()

    st.markdown("---")

    # Listar agendamentos
    st.subheader("Agendamentos Realizados")
    for ag in st.session_state.agendamentos:
        st.write(f"**Artista:** {ag['artista']} | **Cliente:** {ag['cliente']} | **Serviço:** {ag['servico']}")
        st.write(f"Data: {ag['inicio'].strftime('%d/%m/%Y')} - {ag['inicio'].strftime('%H:%M')} até {ag['fim'].strftime('%H:%M')}")
        st.write(f"Cidade: {ag['cidade']} | Email: {ag['email']} | Telefone: {ag['telefone']}")
        st.markdown("---")

# --- FIM DO CÓDIGO ---

st.info("Sistema de agendamento online finalizado.")
