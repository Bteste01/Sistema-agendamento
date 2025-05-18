import streamlit as st
from datetime import datetime
from PIL import Image
import json
import os

# --- Funções para salvar e carregar dados JSON ---
DATA_PATH = 'data'
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def salvar_dados(nome_arquivo, dados):
    caminho = os.path.join(DATA_PATH, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados(nome_arquivo, default):
    caminho = os.path.join(DATA_PATH, nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

# --- Estado inicial ---
if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = False
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Home'

# --- Dados iniciais ---
empresa = carregar_dados('empresa.json', {
    "nome": "Grupo Reobote Serviços",
    "descricao": "Serviços de qualidade com foco em entretenimento e assessoria.",
    "logotipo": None,
    "whatsapp": "+5511999999999"
})

artistas = carregar_dados('artistas.json', [
    {
        "nome": "Bruno Cruz",
        "servicos": [{"nome": "Show musical", "preco": 2500.0}],
        "descricao": "Cantor e compositor com repertório variado.",
        "categoria": "Cantor",
        "redes_sociais": ["https://instagram.com/brunocruz", "https://facebook.com/brunocruz"],
        "foto": None
    },
    {
        "nome": "Skreps",
        "servicos": [{"nome": "Palestra motivacional", "preco": 1800.0}],
        "descricao": "Palestrante e influenciador com foco em motivação pessoal.",
        "categoria": "Palestrante",
        "redes_sociais": ["https://linkedin.com/in/skreps"],
        "foto": None
    }
])

agendamentos = carregar_dados('agendamentos.json', [])

# Admin fixo
ADMIN_EMAIL = "admin@admin.com"
ADMIN_SENHA = "admin"

def salvar_todos():
    salvar_dados('empresa.json', empresa)
    salvar_dados('artistas.json', artistas)
    salvar_dados('agendamentos.json', agendamentos)

# --- Menu lateral para navegação ---
menu = ["Home", "Artistas", "Agendar", "Contato", "Admin"]

st.sidebar.title("Menu")
opcao = st.sidebar.radio("Ir para:", menu)
st.session_state.pagina = opcao

# --- Página Home ---
if st.session_state.pagina == "Home":
    st.title(empresa["nome"])
    if empresa["logotipo"]:
        try:
            img = Image.open(empresa["logotipo"])
            st.image(img, width=200)
        except:
            pass
    st.write(empresa["descricao"])

# --- Página Artistas ---
elif st.session_state.pagina == "Artistas":
    st.title("Nossos Artistas")
    for artista in artistas:
        st.subheader(artista["nome"])
        if artista["foto"]:
            try:
                img = Image.open(artista["foto"])
                st.image(img, width=150)
            except:
                pass
        st.write(f"**Categoria:** {artista['categoria']}")
        st.write(f"**Descrição:** {artista['descricao']}")
        st.write("**Redes Sociais:**")
        for rede in artista.get("redes_sociais", []):
            st.markdown(f"- [{rede}]({rede})")
        st.markdown("---")

# --- Página Agendar ---
elif st.session_state.pagina == "Agendar":
    st.title("Agendar um Artista")

    nomes_artistas = [a['nome'] for a in artistas]
    artista_escolhido = st.selectbox("Escolha o artista", nomes_artistas)

    artista_info = next((a for a in artistas if a['nome'] == artista_escolhido), None)
    if artista_info:
        st.write(f"**Descrição:** {artista_info['descricao']}")
        st.write(f"**Categoria:** {artista_info['categoria']}")
        if artista_info.get("redes_sociais"):
            st.write("**Redes Sociais:**")
            for rede in artista_info["redes_sociais"]:
                st.markdown(f"- [{rede}]({rede})")

        servicos_descr = [f"{s['nome']} - R$ {s['preco']:.2f}" for s in artista_info['servicos']]
        servico_escolhido = st.selectbox("Escolha o serviço", servicos_descr)

        nome_cliente = st.text_input("Seu nome")
        email_cliente = st.text_input("Seu email")
        telefone_cliente = st.text_input("Seu telefone")
        cidade_cliente = st.text_input("Sua cidade")
        data_evento = st.date_input("Data do evento")
        hora_inicio = st.time_input("Hora de início")
        hora_fim = st.time_input("Hora de término")

        if st.button("Confirmar Agendamento"):
            inicio = datetime.combine(data_evento, hora_inicio)
            fim = datetime.combine(data_evento, hora_fim)
            conflito = any(
                ag['artista'] == artista_escolhido and
                not (fim <= datetime.fromisoformat(ag['inicio']) or inicio >= datetime.fromisoformat(ag['fim']))
                for ag in agendamentos
            )
            if conflito:
                st.error("Esse horário já está ocupado para este artista.")
            elif not nome_cliente or not email_cliente:
                st.error("Por favor, preencha seu nome e email.")
            else:
                agendamento = {
                    "artista": artista_escolhido,
                    "servico": servico_escolhido,
                    "cliente": nome_cliente,
                    "email": email_cliente,
                    "telefone": telefone_cliente,
                    "cidade": cidade_cliente,
                    "inicio": inicio.isoformat(),
                    "fim": fim.isoformat()
                }
                agendamentos.append(agendamento)
                salvar_dados('agendamentos.json', agendamentos)
                st.success("Agendamento confirmado!")

# --- Página Contato ---
elif st.session_state.pagina == "Contato":
    st.title("Contato")
    st.write(f"Fale conosco pelo WhatsApp:")
    whatsapp = empresa.get("whatsapp", "")
    if whatsapp:
        whatsapp_num = whatsapp.replace("+", "").replace(" ", "")
        st.markdown(f"[WhatsApp: {whatsapp}](https://wa.me/{whatsapp_num})")
    else:
        st.write("WhatsApp não informado.")

# --- Página Admin ---
elif st.session_state.pagina == "Admin":
    st.title("Área do Administrador")

    if not st.session_state.admin_logado:
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
                st.session_state.admin_logado = True
                st.success("Logado com sucesso!")
            else:
                st.error("Credenciais incorretas.")
    else:
        st.success("Administrador logado")

        st.subheader("Configurações da Empresa")
        nome_emp = st.text_input("Nome da empresa", value=empresa["nome"])
        descricao_emp = st.text_area("Descrição da empresa", value=empresa["descricao"])
        whatsapp_emp = st.text_input("WhatsApp", value=empresa["whatsapp"])

        logotipo_emp = st.file_uploader("Logotipo (PNG/JPG)", type=["png","jpg"])

        if st.button("Salvar dados da empresa"):
            empresa["nome"] = nome_emp
            empresa["descricao"] = descricao_emp
            empresa["whatsapp"] = whatsapp_emp
            if logotipo_emp:
                img = Image.open(logotipo_emp)
                caminho_logo = os.path.join(DATA_PATH, "logo.png")
                img.save(caminho_logo)
                empresa["logotipo"] = caminho_logo
            salvar_dados('empresa.json', empresa)
            st.success("Dados da empresa atualizados.")

        st.markdown("---")

        st.subheader("Gerenciar Artistas")
        nomes_artistas = [a['nome'] for a in artistas]
        artista_sel = st.selectbox("Selecione artista para editar/excluir", nomes_artistas)

        artista_atual = next((a for a in artistas if a['nome'] == artista_sel), None)
        if artista_atual:
            nome_artista = st.text_input("Nome do artista", value=artista_atual["nome"])
            categoria_artista = st.text_input("Categoria", value=artista_atual.get("categoria", ""))
            descricao_artista = st.text_area("Descrição", value=artista_atual.get("descricao", ""))

            # Redes sociais
            redes_sociais = artista_atual.get("redes_sociais", [])
            st.write("Redes sociais (URLs):")
            for i in range(len(redes_sociais)):
                redes_sociais[i] = st.text_input(f"Rede social {i+1}", value=redes_sociais[i], key=f"rede_{i}")

            if st.button("Adicionar Rede Social"):
                redes_sociais.append("")
            
            # Serviços do artista
            servicos = artista_atual.get("servicos", [])
            for idx, serv in enumerate(servicos):
                serv_nome = st.text_input(f"Serviço {idx+1} Nome", value=serv["nome"], key=f"serv_nome_{idx}")
                serv_preco = st.number_input(f"Serviço {idx+1} Preço", value=serv["preco"], key=f"serv_preco_{idx}")
                servicos[idx]["nome"] = serv_nome
                servicos[idx]["preco"] = serv_preco

            if st.button("Adicionar Serviço"):
                servicos.append({"nome":"", "preco":0.0})

            if st.button("Salvar alterações do artista"):
                artista_atual["nome"] = nome_artista
                artista_atual["categoria"] = categoria_artista
                artista_atual["descricao"] = descricao_artista
                artista_atual["redes_sociais"] = [r for r in redes_sociais if r.strip() != ""]
                artista_atual["servicos"] = servicos
                salvar_dados('artistas.json', artistas)
                st.success("Artista atualizado!")

            if st.button("Excluir artista"):
                artistas.remove(artista_atual)
                salvar_dados('artistas.json', artistas)
                st.success("Artista removido!")

        if st.button("Logout"):
            st.session_state.admin_logado = False
            st.experimental_rerun()
