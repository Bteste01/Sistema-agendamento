import streamlit as st 
from datetime import datetime, timedelta 
from PIL import Image 
import io

#Estado inicial

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = [] if 'admin_principal' not in st.session_state: st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin'} if 'admins' not in st.session_state: st.session_state.admins = [] if 'admin_logado' not in st.session_state: st.session_state.admin_logado = None if 'whatsapp' not in st.session_state: st.session_state.whatsapp = '' if 'empresa' not in st.session_state: st.session_state.empresa = {'nome': 'Grupo Reobote Serviços', 'descricao': '', 'logotipo': None} if 'artistas_disponiveis' not in st.session_state: st.session_state.artistas_disponiveis = [ { "nome": "Bruno Cruz", "servicos": [{"nome": "Show musical", "preco": 2500.00}], "foto": None, "descricao": "Cantor e compositor com repertório variado.", "categoria": "Cantor" }, { "nome": "Skreps", "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal.", "categoria": "Palestrante" }, { "nome": "Lú Almeida", "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos.", "categoria": "Pregadora" } ]

Interface pública (agendamento)

st.title("Grupo Reobote Serviços")

if st.session_state.empresa['nome']: if st.session_state.empresa['logotipo']: st.image(st.session_state.empresa['logotipo'], width=100) st.subheader(st.session_state.empresa['nome']) st.caption(st.session_state.empresa['descricao'])

st.header("Agendar um Artista")

artista_nomes = [a['nome'] for a in st.session_state.artistas_disponiveis] artista_selecionado = st.selectbox("Escolha um artista", artista_nomes)

artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado) if artista_info['foto']: st.image(artista_info['foto'], width=150) st.write("Descrição:", artista_info['descricao']) st.write("Categoria:", artista_info['categoria'])

servico_opcoes = [f"{s['nome']} - R${s['preco']:.2f}" for s in artista_info['servicos']] servico_escolhido = st.selectbox("Escolha o serviço", servico_opcoes)

nome_cliente = st.text_input("Seu nome") email_cliente = st.text_input("Email") telefone_cliente = st.text_input("Telefone") cidade_cliente = st.text_input("Cidade") data_evento = st.date_input("Data do evento") hora_inicio = st.time_input("Hora de início") hora_fim = st.time_input("Hora de término")

if st.button("Confirmar Agendamento"): inicio = datetime.combine(data_evento, hora_inicio) fim = datetime.combine(data_evento, hora_fim) conflito = any( ag['artista'] == artista_selecionado and not (fim <= ag['inicio'] or inicio >= ag['fim']) for ag in st.session_state.agendamentos ) if conflito: st.error("Esse horário já está ocupado para este artista.") else: st.session_state.agendamentos.append({ 'artista': artista_selecionado, 'servico': servico_escolhido, 'cliente': nome_cliente, 'email': email_cliente, 'telefone': telefone_cliente, 'cidade': cidade_cliente, 'inicio': inicio, 'fim': fim }) st.success("Agendamento realizado com sucesso!")

Botão de WhatsApp

if st.session_state.whatsapp: whatsapp_link = f"https://wa.me/{st.session_state.whatsapp.replace('+', '').replace(' ', '')}" st.markdown(f"Fale conosco no WhatsApp", unsafe_allow_html=True)

Botão de login do admin

st.markdown("---") with st.expander("Área do Administrador"): login_email = st.text_input("Email do administrador") login_senha = st.text_input("Senha", type="password") if st.button("Entrar"): if login_email == st.session_state.admin_principal['email'] and login_senha == st.session_state.admin_principal['senha']: st.session_state.admin_logado = 'principal' st.success("Login como administrador principal!") elif any(a['email'] == login_email and a['senha'] == login_senha for a in st.session_state.admins): st.session_state.admin_logado = login_email st.success("Login como administrador!") else: st.error("Credenciais inválidas.")

Interface do administrador principal

if st.session_state.admin_logado == 'principal': st.header("Painel do Administrador Principal") st.subheader("Cadastrar Novo Administrador") email_novo = st.text_input("Email do novo administrador") senha_nova = st.text_input("Senha", type="password") if st.button("Cadastrar Novo Administrador"): if any(a['email'] == email_novo for a in st.session_state.admins): st.warning("Administrador já cadastrado") else: st.session_state.admins.append({"email": email_novo, "senha": senha_nova}) st.success("Novo administrador cadastrado com sucesso")

st.subheader("Configurações da Empresa")
nome_empresa = st.text_input("Nome da empresa", value=st.session_state.empresa['nome'])
descricao_empresa = st.text_area("Descrição", value=st.session_state.empresa['descricao'])
logotipo = st.file_uploader("Logotipo", type=["png", "jpg"])
whatsapp_numero = st.text_input("Número de WhatsApp para contato", value=st.session_state.whatsapp)
if st.button("Salvar Dados da Empresa"):
    st.session_state.empresa['nome'] = nome_empresa
    st.session_state.empresa['descricao'] = descricao_empresa
    if logotipo:
        st.session_state.empresa['logotipo'] = Image.open(logotipo)
    st.session_state.whatsapp = whatsapp_numero
    st.success("Dados da empresa atualizados com sucesso")

st.subheader("Lista de Agendamentos")
for ag in st.session_state.agendamentos:
    st.write(f"{ag['cliente']} agendou {ag['servico']} com {ag['artista']} em {ag['inicio']} até {ag['fim']} - {ag['cidade']} - {ag['telefone']}")

st.subheader("Excluir Artista")
artistas = [a['nome'] for a in st.session_state.artistas_disponiveis]
artista_excluir = st.selectbox("Escolha um artista para excluir", artistas)
if st.button("Excluir Artista"):
    st.session_state.artistas_disponiveis = [a for a in st.session_state.artistas_disponiveis if a['nome'] != artista_excluir]
    st.success(f"Artista {artista_excluir} removido com sucesso")

