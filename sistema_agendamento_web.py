import streamlit as st
from fpdf
import FPDF
from datetime
import datetime
from PIL import Image
import io

#Estado inicial

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = [] if 'admin' not in st.session_state: st.session_state.admin = None if 'admin_email' not in st.session_state: st.session_state.admin_email = None if 'artistas_disponiveis' not in st.session_state: st.session_state.artistas_disponiveis = [ { "nome": "Bruno Cruz", "servicos": [ {"nome": "Show musical", "preco": 2500.00}, ], "foto": None, "descricao": "Cantor e compositor com repertório variado.", "categoria": "Cantor" }, { "nome": "Skreps", "servicos": [ {"nome": "Palestra motivacional", "preco": 1800.00}, ], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal.", "categoria": "Palestrante" }, { "nome": "Lú Almeida", "servicos": [ {"nome": "Ministração gospel", "preco": 2000.00}, ], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos.", "categoria": "Pregadora" } ] if 'admins' not in st.session_state: st.session_state.admins = {} if 'empresa' not in st.session_state: st.session_state.empresa = {"nome": "", "descricao": "", "logotipo": None}

Função de login

st.title("Sistema de Agendamento de Artistas") st.sidebar.header("Login do Administrador")

email = st.sidebar.text_input("Email") senha = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Entrar"): if email in st.session_state.admins and st.session_state.admins[email] == senha: st.session_state.admin = True st.session_state.admin_email = email st.success("Login realizado com sucesso!") elif email == "admin@principal.com" and senha == "admin123": st.session_state.admin = True st.session_state.admin_email = email st.success("Login como Administrador Principal!") else: st.error("Credenciais inválidas")

Interface para todos: agendamento

st.subheader("Agendamento de Evento") empresa = st.session_state.empresa if empresa["logotipo"]: st.image(empresa["logotipo"], width=100) st.write(f"{empresa['nome']}") st.write(empresa["descricao"])

nome = st.text_input("Seu nome") email_cliente = st.text_input("Seu e-mail") telefone = st.text_input("Telefone") cidade = st.text_input("Cidade") artista = st.selectbox("Escolha um artista", [a["nome"] for a in st.session_state.artistas_disponiveis]) servico = st.selectbox("Escolha o serviço", next(a for a in st.session_state.artistas_disponiveis if a["nome"] == artista)["servicos"]) data_evento = st.date_input("Data do Evento") horario_inicio = st.time_input("Horário de Início") horario_fim = st.time_input("Horário de Término")

if st.button("Agendar"): conflito = False for ag in st.session_state.agendamentos: if ag["artista"] == artista and ag["data"] == data_evento: if (horario_inicio < ag["horario_fim"] and horario_fim > ag["horario_inicio"]): conflito = True break if conflito: st.error("Este artista já

