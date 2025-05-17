import streamlit as st
from fpdf import FPDF from datetime import datetime from PIL import Image import io

Inicialização do estado da sessão

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = [] if 'admin' not in st.session_state: st.session_state.admin = False if 'artistas_disponiveis' not in st.session_state: st.session_state.artistas_disponiveis = [ {"nome": "Bruno Cruz", "servicos": [{"nome": "Show musical", "preco": 2500.00}], "foto": None, "descricao": "Cantor e compositor com repertório variado."}, {"nome": "Skreps", "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal."}, {"nome": "Lú Almeida", "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos."} ]

Login do administrador

with st.sidebar.expander("Entrar como administrador"): senha = st.text_input("Senha", type="password") if st.button("Entrar"): if senha == "admin123": st.session_state.admin = True st.success("Acesso concedido como administrador.") else: st.error("Senha incorreta.")

Menu lateral com base no modo admin

menu_opcoes = ["Agendar", "Ver Agendamentos", "Exportar PDF", "Lista de Artistas"] if st.session_state.admin: menu_opcoes.append("Cadastrar Artista") menu = st.sidebar.selectbox("Menu", menu_opcoes)

Página: Agendar

if menu == "Agendar": st.title("Agendamento")

artista_nomes = [a["nome"] for a in st.session_state.artistas_disponiveis]
artista_escolhido = st.selectbox("Escolha o artista", artista_nomes)
artista_info = next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista_escolhido)

if artista_info.get("foto"):
    st.image(artista_info["foto"], width=150)
if artista_info.get("descricao"):
    st.info(artista_info["descricao"])

servicos = [s["nome"] for s in artista_info["servicos"]]
servico_escolhido = st.selectbox("Escolha o serviço", servicos)
preco = next(s['preco'] for s in artista_info['servicos'] if s['nome'] == servico_escolhido)

st.write(f"**Preço:** R$ {preco:.2f}")

data = st.date_input("Data do agendamento")
hora = st.time_input("Horário")

conflito = any(
    ag['artista'] == artista_escolhido and ag['data'] == data and ag['hora'] == hora
    for ag in st.session_state.agendamentos
)

st.subheader("Dados do contratante")
contratante = st.text_input("Nome do contratante")
email = st.text_input("Email do contratante")
telefone = st.text_input("Telefone do contratante")
cidade = st.text_input("Cidade do contratante")

if st.button("Agendar"):
    if conflito:
        st.error("Este artista já está agendado para essa data e horário.")
    else:
        st.session_state.agendamentos.append({
            "artista": artista_escolhido,
            "servico": servico_escolhido,
            "preco": preco,
            "data": data,
            "hora": hora,
            "contratante": contratante,
            "email": email,
            "telefone": telefone,
            "cidade": cidade
        })
        st.success("Agendamento realizado com sucesso!")

Página: Ver Agendamentos

elif menu == "Ver Agendamentos": st.title("Agendamentos Realizados") if not st.session_state.agendamentos: st.info("Nenhum agendamento realizado.") else: for i, ag in enumerate(st.session_state.agendamentos): st.write(f"{i+1}. Artista: {ag['artista']} | Serviço: {ag['servico']} | Preço: R$ {ag['preco']:.2f}") st.write(f"   Data: {ag['data']} | Hora: {ag['hora']}") st.write(f"   Contratante: {ag['contratante']} | Email: {ag['email']} | Telefone: {ag['telefone']} | Cidade: {ag['cidade']}") if st.button(f"Cancelar agendamento {i+1}"): st.session_state.agendamentos.pop(i) st.success("Agendamento cancelado.") st.experimental_rerun()

Página: Exportar PDF

elif menu == "Exportar PDF": st.title("Exportar Agendamentos")

if not st.session_state.agendamentos:
    st.info("Nenhum agendamento para exportar.")
else:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Agendamentos", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)

    for ag in st.session_state.agendamentos:
        pdf.cell(0, 10, f"Artista: {ag['artista']} - Serviço: {ag['servico']} - Preço: R$ {ag['preco']:.2f}", ln=True)
        pdf.cell(0, 10, f"Data: {ag['data']} - Hora: {ag['hora']}", ln=True)
        pdf.cell(0, 10, f"Contratante: {ag['contratante']} - Email: {ag['email']} - Tel: {ag['telefone']} - Cidade: {ag['cidade']}", ln=True)
        pdf.ln(5)

    pdf_output = "agendamentos.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button("Baixar PDF", f, file_name="agendamentos.pdf")

Página: Lista de Artistas

elif menu == "Lista de Artistas": st.title("Artistas Disponíveis") for artista in st.session_state.artistas_disponiveis: st.subheader(artista['nome']) if artista.get("foto"): st.image(artista["foto"], width=150) if artista.get("descricao"): st.caption(artista["descricao"]) for servico in artista['servicos']: st.write(f"- {servico['nome']} (R$ {servico['preco']:.2f})")

Página: Cadastrar Artista (somente admin)

elif menu == "Cadastrar Artista" and st.session_state.admin: st.title("Cadastrar Novo Artista")

nome = st.text_input("Nome do artista")
descricao = st.text_area("Descrição do artista")
foto = st.file_uploader("Foto do artista", type=["jpg", "jpeg", "png"])
servicos = []

num_servicos = st.number_input("Quantos serviços o artista oferece?", min_value=1, step=1)

for i in range(int(num_servicos)):
    st.markdown(f"### Serviço {i+1}")
    nome_servico = st.text_input(f"Nome do serviço {i+1}", key=f"servico_{i}")
    preco_servico = st.number_input(f"Preço do serviço {i+1}", min_value=0.0, step=100.0, key=f"preco_{i}")
    servicos.append({"nome": nome_servico, "preco": preco_servico})

if st.button("Cadastrar Artista"):
    if nome and all(s['nome'] for s in servicos):
        foto_bytes = foto.read() if foto else None
        st.session_state.artistas_disponiveis.append({"nome": nome, "descricao": descricao, "servicos": servicos, "foto": foto_bytes})
        st.success("Artista cadastrado com sucesso!")
    else:
        st.warning("Preencha todos os campos dos serviços.")

