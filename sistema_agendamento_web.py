import streamlit as st
from fpdf import FPDF

Inicialização do estado da sessão

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = []

Lista fixa de artistas

artistas_disponiveis = [ {"nome": "Bruno Cruz", "servico": "Show musical", "preco": 2500.00}, {"nome": "Skreps", "servico": "Palestra motivacional", "preco": 1800.00}, {"nome": "Lú Almeida", "servico": "Ministração gospel", "preco": 2000.00} ]

Menu lateral

menu = st.sidebar.selectbox("Menu", ["Agendar", "Ver Agendamentos", "Exportar PDF"])

Página: Agendar

if menu == "Agendar": st.title("Agendamento")

artista_nomes = [a["nome"] for a in artistas_disponiveis]
artista_escolhido = st.selectbox("Escolha o artista", artista_nomes)
artista_info = next(a for a in artistas_disponiveis if a["nome"] == artista_escolhido)

st.write(f"**Serviço:** {artista_info['servico']}")
st.write(f"**Preço:** R$ {artista_info['preco']:.2f}")

data = st.date_input("Data do agendamento")
hora = st.time_input("Horário")

st.subheader("Dados do contratante")
contratante = st.text_input("Nome do contratante")
email = st.text_input("Email do contratante")
telefone = st.text_input("Telefone do contratante")
cidade = st.text_input("Cidade do contratante")

if st.button("Agendar"):
    st.session_state.agendamentos.append({
        "artista": artista_escolhido,
        "servico": artista_info['servico'],
        "preco": artista_info['preco'],
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

