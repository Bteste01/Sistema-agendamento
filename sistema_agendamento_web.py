import streamlit as st
from fpdf import FPDF
Inicialização do estado da sessão

if 'artistas' not in st.session_state: st.session_state.artistas = [] if 'agendamentos' not in st.session_state: st.session_state.agendamentos = []

Menu

menu = st.sidebar.selectbox("Menu", ["Cadastrar Artista", "Agendar", "Ver Agendamentos", "Exportar PDF"])

Página: Cadastrar Artista

if menu == "Cadastrar Artista": st.title("Cadastro de Artista") nome = st.text_input("Nome do Artista") servico = st.text_input("Serviço oferecido") preco = st.number_input("Preço do serviço (R$)", min_value=0.0, format="%.2f") disponibilidade = st.date_input("Disponibilidade de data") horario = st.time_input("Horário disponível")

if st.button("Cadastrar"):
    st.session_state.artistas.append({
        "nome": nome,
        "servico": servico,
        "preco": preco,
        "disponibilidade": disponibilidade,
        "horario": horario
    })
    st.success("Artista cadastrado com sucesso!")

Página: Agendar

elif menu == "Agendar": st.title("Agendamento") if not st.session_state.artistas: st.warning("Nenhum artista cadastrado.") else: artista = st.selectbox("Escolha um artista", [a['nome'] for a in st.session_state.artistas]) data = st.date_input("Data do agendamento") hora = st.time_input("Horário")

st.subheader("Dados do contratante")
    contratante = st.text_input("Nome do contratante")
    email = st.text_input("Email do contratante")
    telefone = st.text_input("Telefone do contratante")
    cidade = st.text_input("Cidade do contratante")

    if st.button("Agendar"):
        st.session_state.agendamentos.append({
            "artista": artista,
            "data": data,
            "hora": hora,
            "contratante": contratante,
            "email": email,
            "telefone": telefone,
            "cidade": cidade
        })
        st.success("Agendamento realizado com sucesso!")

Página: Ver Agendamentos

elif menu == "Ver Agendamentos": st.title("Agendamentos Realizados") if not st.session_state.agendamentos: st.info("Nenhum agendamento realizado.") else: for i, ag in enumerate(st.session_state.agendamentos): st.write(f"{i+1}. Artista: {ag['artista']} | Data: {ag['data']} | Hora: {ag['hora']}") st.write(f"   Contratante: {ag['contratante']} | Email: {ag['email']} | Telefone: {ag['telefone']} | Cidade: {ag['cidade']}") if st.button(f"Cancelar agendamento {i+1}"): st.session_state.agendamentos.pop(i) st.success("Agendamento cancelado.") st.experimental_rerun()

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
        pdf.cell(0, 10, f"Artista: {ag['artista']}", ln=True)
        pdf.cell(0, 10, f"Data: {ag['data']} - Hora: {ag['hora']}", ln=True)
        pdf.cell(0, 10, f"Contratante: {ag['contratante']} - Email: {ag['email']} - Tel: {ag['telefone']} - Cidade: {ag['cidade']}", ln=True)
        pdf.ln(5)

    pdf_output = "agendamentos.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button("Baixar PDF", f, file_name="agendamentos.pdf")

