import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF

# ---------- Armazenamento simples em JSON ----------
def salvar_dados(dados):
    with open("dados_artistas.json", "w") as f:
        json.dump(dados, f, indent=4)

def carregar_dados():
    try:
        with open("dados_artistas.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

dados = carregar_dados()

# ---------- Cabeçalho com dados da empresa ----------
st.title("Sistema de Agendamento")
empresa = st.text_input("Nome da empresa", value="Minha Assessoria")
descricao = st.text_area("Descrição da empresa")
logo = st.file_uploader("Logotipo (opcional)", type=["png", "jpg"])

st.markdown("---")

# ---------- Aba de navegação ----------
aba = st.sidebar.selectbox("Menu", ["Cadastrar Artista", "Agendar", "Ver Agendamentos", "Exportar PDF"])

# ---------- Cadastrar artista ----------
if aba == "Cadastrar Artista":
    st.header("Cadastrar Novo Artista")
    nome = st.text_input("Nome do Artista")
    servico = st.text_input("Serviço (ex: show, palestra)")
    preco = st.number_input("Preço", step=50.0)
    disponibilidade = st.text_area("Datas disponíveis (separadas por vírgula, formato DD/MM/AAAA HH:MM)")

    if st.button("Salvar Artista"):
        if nome:
            dados[nome] = {
                "servico": servico,
                "preco": preco,
                "disponibilidade": [d.strip() for d in disponibilidade.split(",")],
                "agendamentos": []
            }
            salvar_dados(dados)
            st.success("Artista cadastrado com sucesso!")

# ---------- Agendar artista ----------
elif aba == "Agendar":
    st.header("Agendar Artista")
    artistas = list(dados.keys())
    if artistas:
        artista = st.selectbox("Escolha o artista", artistas)
        disponiveis = dados[artista]["disponibilidade"]
        data = st.selectbox("Data disponível", disponiveis)
        cliente = st.text_input("Nome do contratante")

        if st.button("Agendar"):
            if cliente:
                dados[artista]["agendamentos"].append({
                    "cliente": cliente,
                    "data": data
                })
                dados[artista]["disponibilidade"].remove(data)
                salvar_dados(dados)
                st.success("Agendamento feito com sucesso!")
    else:
        st.warning("Cadastre um artista primeiro.")

# ---------- Ver agendamentos ----------
elif aba == "Ver Agendamentos":
    st.header("Agendamentos")
    for artista, info in dados.items():
        st.subheader(artista)
        for ag in info["agendamentos"]:
            col1, col2, col3 = st.columns(3)
            col1.write(f"**Cliente:** {ag['cliente']}")
            col2.write(f"**Data:** {ag['data']}")
            if col3.button("Cancelar", key=f"{artista}-{ag['data']}"):
                info["agendamentos"].remove(ag)
                info["disponibilidade"].append(ag['data'])
                salvar_dados(dados)
                st.warning("Agendamento cancelado.")

# ---------- Exportar PDF ----------
elif aba == "Exportar PDF":
    st.header("Exportar Agendamentos em PDF")

    if st.button("Gerar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, empresa, ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, descricao)
        pdf.ln(5)

        for artista, info in dados.items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"Artista: {artista}", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"Serviço: {info['servico']} - Preço: R${info['preco']:.2f}", ln=True)
            pdf.cell(0, 8, "Agendamentos:", ln=True)
            for ag in info["agendamentos"]:
                pdf.cell(0, 8, f"  - {ag['data']} | {ag['cliente']}", ln=True)
            pdf.ln(5)

        nome_arquivo = "agendamentos.pdf"
        pdf.output(nome_arquivo)

        with open(nome_arquivo, "rb") as f:
            st.download_button("Clique para baixar o PDF", f, file_name=nome_arquivo, mime="application/pdf")
