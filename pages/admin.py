
import json
import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Admin | Festa Julina da Mary",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

.stApp {
    background: #fff5e6;
    color: #12355b;
}

.main .block-container {
    max-width: 1080px;
    padding-top: 2rem;
}

.admin-card {
    background: #ffffff;
    border: 1px solid #efd3a1;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 12px 28px rgba(90, 60, 20, 0.08);
    margin-bottom: 24px;
}

.admin-title {
    font-size: 2.2rem;
    font-weight: 950;
    color: #12355b;
    margin-bottom: 6px;
}

.admin-subtitle {
    color: #64748b;
}

.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    border-radius: 999px !important;
    background: #df7f00 !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 850 !important;
}

.stButton > button p,
button[kind="primary"] p,
button[kind="secondary"] p {
    color: #ffffff !important;
    font-weight: 850 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_supabase_client():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_KEY"])


supabase = get_supabase_client()


def buscar_participantes():
    return (
        supabase.table("participantes")
        .select("*")
        .order("criado_em", desc=True)
        .execute()
        .data
    )


def atualizar_status(participante_id, novo_status):
    supabase.table("participantes").update({"status_pagamento": novo_status}).eq("id", participante_id).execute()


def gerar_link_comprovante(caminho):
    if not caminho:
        return None

    try:
        response = supabase.storage.from_("comprovantes").create_signed_url(path=caminho, expires_in=3600)
        return response.get("signedURL") or response.get("signedUrl")
    except Exception:
        return None


st.markdown(
    """
<div class="admin-card">
    <div class="admin-title">Painel administrativo</div>
    <div class="admin-subtitle">Acesso restrito à organização da Festa Julina da Mary.</div>
</div>
""",
    unsafe_allow_html=True,
)

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if not st.session_state.admin_logado:
    with st.form("login_admin"):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            senha = st.text_input("Senha", type="password")
            acessar = st.form_submit_button("Acessar", use_container_width=True)

        if acessar:
            if senha == st.secrets.get("ADMIN_PASSWORD", "admin123"):
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("Senha incorreta.")

    st.stop()

col_back, col_logout = st.columns([1, 1])
with col_back:
    if st.button("Voltar para inscrição"):
        st.switch_page("app.py")
with col_logout:
    if st.button("Sair do admin"):
        st.session_state.admin_logado = False
        st.rerun()

participantes = buscar_participantes()

if not participantes:
    st.info("Ainda não há participantes cadastrados.")
    st.stop()

df = pd.DataFrame(participantes)

total_previsto = df["valor_cota"].sum() if "valor_cota" in df.columns else 0
total_confirmado = df[df["status_pagamento"] == "confirmado"]["valor_cota"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Registros", len(df))
col2.metric("Adultos únicos", df["nome"].nunique())
col3.metric("Total previsto", f"R$ {total_previsto:.2f}")
col4.metric("Total confirmado", f"R$ {total_confirmado:.2f}")

st.markdown("### Participantes")

for participante in participantes:
    titulo = f"{participante['nome']} - R$ {float(participante['valor_cota']):.2f}"

    with st.expander(titulo):
        st.write(f"**E-mail:** {participante.get('email', '')}")
        st.write(f"**WhatsApp:** {participante.get('whatsapp', '')}")
        st.write(f"**Tipo de cota:** {participante.get('tipo_cota', '')}")
        st.write(f"**Item para levar:** {participante.get('item_levar') or '-'}")
        st.write(f"**Status:** {participante.get('status_pagamento', '')}")

        familiares = participante.get("familiares")
        if familiares:
            try:
                dados = json.loads(familiares)
                st.write(f"**Responsável:** {dados.get('responsavel', '-')}")
                st.write(f"**Crianças:** {', '.join(dados.get('criancas', [])) or '-'}")
            except Exception:
                st.write(f"**Familiares:** {familiares}")

        comprovante_path = participante.get("comprovante_url")
        st.write(f"**Arquivo do comprovante:** {comprovante_path or '-'}")

        link_comprovante = gerar_link_comprovante(comprovante_path)
        if link_comprovante:
            st.link_button("Abrir comprovante", link_comprovante)

        status_opcoes = ["aguardando_conferencia", "confirmado", "recusado"]
        atual = participante.get("status_pagamento", "aguardando_conferencia")
        index_atual = status_opcoes.index(atual) if atual in status_opcoes else 0

        novo_status = st.selectbox(
            "Alterar status",
            status_opcoes,
            index=index_atual,
            key=f"status_{participante['id']}",
        )

        if st.button("Salvar status", key=f"btn_{participante['id']}"):
            atualizar_status(participante["id"], novo_status)
            st.success("Status atualizado.")
            st.rerun()

st.markdown("### Tabela geral")
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Baixar lista em CSV",
    data=csv,
    file_name="participantes_festa_julina_mary.csv",
    mime="text/csv",
)
