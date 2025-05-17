import streamlit as st
from PIL import Image
import io
from fpdf import FPDF

# Verifica login de administrador
if 'admin' not in st.session_state or not st.session_state.admin:
    st.error("Acesso restrito. Faça login como administrador pela página principal.")
    st.stop()

st.title("Painel do Administrador")

# Seção: Dados da Empresa
st.header("Dados da Empresa")
nome_empresa = st.text_input("Nome da empresa", st.session_state.empresa['nome'])
descricao_empresa = st.text_area("Descrição", st.session_state.empresa['descricao'])
logo = st.file_uploader("Logotipo da empresa", type=['png', 'jpg', 'jpeg'])
if logo:
    st.session_state.empresa['logo'] = logo.getvalue()
st.session_state.empresa['nome'] = nome_empresa
st.session_state.empresa['descricao'] = descricao_empresa

# Seção: Gerenciar Artistas
st.header("Artistas Cadastrados")
for i, artista in enumerate(st.session_state.artistas_disponiveis):
    st.subheader(artista['nome'])
    st.markdown(f"**Categoria:** {artista['categoria']}")
    st.markdown(f"**Descrição:** {artista['descricao']}")
    if artista['foto']:
        st.image(artista['foto'], width=100)
    for serv in artista['servicos']:
        st.markdown(f"- {serv['nome']} (R$ {serv['preco']:.2f})")
    if st.button(f"Excluir {artista['nome']}", key=f"del_{i}"):
        st.session_state.artistas_disponiveis.pop(i)
        st.experimental_rerun()

# Seção: Cadastrar novo artista
st.header("Cadastrar Novo Artista")
with st.form("novo_artista"):
    nome = st.text_input("Nome do artista")
    categoria = st.text_input("Categoria")
    descricao = st.text_area("Descrição")
    foto_file = st.file_uploader("Foto", type=['png', 'jpg', 'jpeg'])

    servicos = []
    for i in range(1, 4):
        nome_serv = st.text_input(f"Serviço {i}", key=f"serv_{i}")
        preco = st.number_input(f"Preço do serviço {i}", key=f"preco_{i}", min_value=0.0, step=0.01)
        if nome_serv:
            servicos.append({"nome": nome_serv, "preco": preco})

    enviar = st.form_submit_button("Cadastrar Artista")
    if enviar and nome and servicos:
        novo_artista = {
            "nome": nome,
            "categoria": categoria,
            "descricao": descricao,
            "foto": foto_file.read() if foto_file else None,
            "servicos": servicos
        }
        st.session_state.artistas_disponiveis.append(novo_artista)
        st.success("Artista cadastrado com sucesso!")

# Seção: Agendamentos
st.header("Agendamentos Realizados")
if not st.session_state.agendamentos:
    st.info("Nenhum agendamento registrado.")
else:
    for ag in st.session_state.agendamentos:
        st.markdown(f"**{ag['nome']}** - {ag['artista']} - {ag['data']} das {ag['inicio']} às {ag['fim']}")
        st.markdown(f"Email: {ag['email']} | Telefone: {ag['telefone']} | Cidade: {ag['cidade']}")
        st.markdown(f"Serviço: {ag['servico']} | Preço: R$ {ag['preco']:.2f}")
        st.markdown("---")

    if st.button("Exportar Agendamentos em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for ag in st.session_state.agendamentos:
            pdf.cell(200, 10, txt=f"{ag['nome']} - {ag['artista']} - {ag['data']} - {ag['inicio']} às {ag['fim']}", ln=True)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        st.download_button("Baixar PDF", data=pdf_output.getvalue(), file_name="agendamentos.pdf")

# Seção: Gerenciar administradores
if st.session_state.admin_email == "admin@admin.com":
    st.header("Gerenciar Administradores")
    with st.form("novo_admin"):
        email_novo = st.text_input("E-mail do novo administrador")
        senha_nova = st.text_input("Senha", type="password")
        enviar_admin = st.form_submit_button("Cadastrar administrador")
        if enviar_admin:
            if email_novo in st.session_state.admins:
                st.warning("Este e-mail já está cadastrado.")
            else:
                st.session_state.admins[email_novo] = senha_nova
                st.success("Administrador adicionado com sucesso.")
    
