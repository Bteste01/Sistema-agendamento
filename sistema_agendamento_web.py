import streamlit as st from fpdf import FPDF from datetime import datetime from PIL import Image import io import json import os

Estado inicial

if 'agendamentos' not in st.session_state: st.session_state.agendamentos = []

if 'admin' not in st.session_state: st.session_state.admin = None

if 'admin_email' not in st.session_state: st.session_state.admin_email = None

if 'artistas_disponiveis' not in st.session_state: st.session_state.artistas_disponiveis = [ { "nome": "Bruno Cruz", "servicos": [{"nome": "Show musical", "preco": 2500.00}], "foto": None, "descricao": "Cantor e compositor com repertório variado.", "categoria": "Cantor" }, { "nome": "Skreps", "servicos": [{"nome": "Palestra motivacional", "preco": 1800.00}], "foto": None, "descricao": "Palestrante e influenciador com foco em motivação pessoal.", "categoria": "Palestrante" }, { "nome": "Lú Almeida", "servicos": [{"nome": "Ministração gospel", "preco": 2000.00}], "foto": None, "descricao": "Cantora gospel com experiência em eventos religiosos.", "categoria": "Pregadora" } ]

if 'admins' not in st.session_state: st.session_state.admins = {}

if 'empresa' not in st.session_state: st.session_state.empresa = {"nome": "", "descricao": "", "logo": None}
    
