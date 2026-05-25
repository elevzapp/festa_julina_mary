from datetime import datetime
from pathlib import Path
from uuid import uuid4
from collections import Counter
import base64

import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Festa Julina da Mary",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================
# ESTILO VISUAL
# =========================

st.markdown(
    """
<style>
:root {
    --cream: #fff4df;
    --cream-2: #fffaf0;
    --paper: #ffffff;
    --navy: #12355b;
    --navy-2: #1f4d7c;
    --orange: #df7f00;
    --orange-2: #bf6900;
    --yellow: #f7c948;
    --line: #ead9bc;
    --soft-line: #f0c987;
    --muted: #64748b;
    --text: #24364b;
    --green: #65a30d;
    --green-bg: #ecfbd3;
}

.stApp {
    background: var(--cream);
    color: var(--text);
}

.main .block-container {
    max-width: 100%;
    padding: 0;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    display: none;
}

h1, h2, h3, h4, p, div, span, label {
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

.content-wrap {
    width: min(1180px, calc(100% - 48px));
    margin: 0 auto;
}

.full-section {
    padding: 78px 0;
}

.white-section {
    background: #ffffff;
}

.cream-section {
    background: var(--cream);
}

.yellow-band {
    background: #f6c453;
    padding: 78px 0;
}

/* Admin */
.st-key-admin_lock {
    position: fixed;
    top: 18px;
    right: 20px;
    z-index: 9999;
}

.st-key-admin_lock button {
    width: 34px !important;
    height: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    border-radius: 999px !important;
    background: rgba(0,0,0,0.72) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18) !important;
}

.st-key-admin_lock button p {
    color: #ffffff !important;
    font-size: 0.9rem !important;
}

/* Hero */
.hero-image-full {
    width: 100%;
    height: clamp(280px, 42vw, 620px);
    object-fit: cover;
    object-position: center;
    display: block;
    border: none;
    border-radius: 0;
    box-shadow: none;
}

.hero-main {
    background: #ffffff;
    padding: 90px 0 86px;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(360px, 0.82fr);
    gap: 54px;
    align-items: center;
}

.hero-title {
    font-size: clamp(2.7rem, 5.7vw, 5.4rem);
    line-height: 1.04;
    letter-spacing: -0.05em;
    font-weight: 950;
    color: var(--navy);
    margin-bottom: 26px;
}

.hero-text {
    max-width: 720px;
    font-size: 1.27rem;
    line-height: 1.72;
    color: #405168;
    margin-bottom: 32px;
}

.how-card {
    background: #fff7e6;
    border: 1px solid var(--soft-line);
    border-left: 8px solid var(--orange);
    border-radius: 28px;
    padding: 34px;
    box-shadow: 0 14px 30px rgba(90, 60, 20, 0.08);
}

.how-title {
    color: var(--navy);
    font-weight: 950;
    font-size: 1.85rem;
    margin-bottom: 20px;
}

.how-text,
.quota-line {
    color: #405168;
    line-height: 1.75;
    font-size: 1.08rem;
}

.quota-line {
    margin: 14px 0;
}

.quota-line strong {
    color: var(--navy);
}

/* Buttons */
a.cta-button {
    display: inline-block;
    background: var(--orange);
    color: #ffffff !important;
    font-weight: 900;
    text-decoration: none;
    padding: 16px 36px;
    border-radius: 999px;
    box-shadow: 0 10px 24px rgba(90, 60, 20, 0.18);
}

.stButton > button,
button[kind="secondary"],
button[kind="primary"],
.stFormSubmitButton > button {
    border-radius: 999px !important;
    font-weight: 900 !important;
    border: none !important;
    background: var(--orange) !important;
    color: #ffffff !important;
    padding: 0.72rem 1.35rem !important;
    width: auto !important;
    min-width: 190px !important;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p,
.stFormSubmitButton > button p {
    color: #ffffff !important;
    font-weight: 900 !important;
}

.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {
    background: var(--orange-2) !important;
    color: #ffffff !important;
}

/* Included items */
.section-title-center {
    text-align: center;
    font-size: clamp(2rem, 4vw, 3.2rem);
    line-height: 1.08;
    font-weight: 950;
    color: var(--navy);
    margin-bottom: 18px;
}

.section-subtitle-center {
    text-align: center;
    font-size: 1.16rem;
    line-height: 1.7;
    color: #405168;
    max-width: 840px;
    margin: 0 auto 40px;
}

.included-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    margin-top: 34px;
}

.included-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 26px;
    padding: 26px 18px;
    min-height: 142px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 14px;
    text-align: center;
    box-shadow: 0 12px 28px rgba(90, 60, 20, 0.10);
    font-weight: 950;
    color: var(--navy);
}

.included-emoji {
    font-size: 2.15rem;
    line-height: 1;
}

.note-card-wide {
    margin: 30px auto 0;
    max-width: 980px;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 22px;
    padding: 20px 24px;
    color: #405168;
    line-height: 1.7;
    text-align: center;
}

.note-card-wide strong {
    color: var(--navy);
}

/* Form */
.form-section {
    padding: 82px 0;
}

.form-shell {
    width: min(980px, calc(100% - 48px));
    margin: 0 auto;
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 32px;
    padding: 42px;
    box-shadow: 0 14px 34px rgba(90, 60, 20, 0.08);
}

.form-title {
    color: var(--navy);
    font-size: clamp(2rem, 3vw, 2.9rem);
    line-height: 1.1;
    font-weight: 950;
    margin-bottom: 12px;
}

.form-subtitle {
    color: #526477;
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 28px;
}

.step-title {
    color: var(--navy);
    font-size: 1.55rem;
    font-weight: 950;
    margin: 28px 0 18px;
}

.person-box {
    background: #fffaf0;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 20px;
    margin: 16px 0;
}

.person-title {
    color: var(--navy);
    font-size: 1.15rem;
    font-weight: 950;
    margin-bottom: 12px;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 22px 0 30px;
}

.stat-card {
    background: #fffdf8;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(90, 60, 20, 0.05);
}

.stat-label {
    color: var(--muted);
    font-size: 0.95rem;
    margin-bottom: 10px;
}

.stat-value {
    color: var(--navy);
    font-size: 2rem;
    font-weight: 950;
}

.quota-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 14px 0 18px;
}

.quota-card,
.quota-card-selected {
    border-radius: 24px;
    padding: 22px;
    min-height: 210px;
    cursor: pointer;
    box-shadow: 0 8px 22px rgba(90, 60, 20, 0.06);
}

.quota-card {
    background: #fffdf8;
    border: 2px solid #e8d3ae;
}

.quota-card-selected {
    background: var(--green-bg);
    border: 3px solid var(--green);
}

.quota-title {
    font-size: 1.25rem;
    font-weight: 950;
    color: var(--navy);
    margin-bottom: 8px;
}

.quota-price {
    font-size: 2rem;
    font-weight: 950;
    color: #b85f00;
    margin-bottom: 10px;
}

.quota-desc {
    font-size: 0.96rem;
    color: #475569;
    line-height: 1.5;
}

.item-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin: 14px 0;
}

.item-card,
.item-card-selected {
    border-radius: 22px;
    padding: 18px;
    min-height: 128px;
    text-align: center;
}

.item-card {
    background: #fffdf8;
    border: 2px solid #e8d3ae;
}

.item-card-selected {
    background: var(--green-bg);
    border: 3px solid var(--green);
}

.item-title {
    color: var(--navy);
    font-weight: 950;
    font-size: 1.02rem;
    margin-top: 8px;
}

.item-meta {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 8px;
}

/* Payment */
.payment-card-main {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 32px;
    padding: 34px;
    box-shadow: 0 14px 34px rgba(90, 60, 20, 0.08);
    margin-top: 36px;
}

.payment-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 18px;
}

.payment-block {
    background: #fffdf8;
    border: 2px dashed #d8bd8b;
    border-radius: 24px;
    padding: 24px;
}

.payment-block-title {
    font-size: 1.35rem;
    font-weight: 950;
    color: var(--navy);
    margin-bottom: 14px;
}

.payment-line {
    margin: 8px 0;
    color: #405168;
    line-height: 1.5;
}

.payment-line strong {
    color: var(--navy);
}

.pix-key {
    display: inline-block;
    background: var(--navy);
    color: #ffffff;
    padding: 13px 16px;
    border-radius: 14px;
    font-size: 1.18rem;
    font-weight: 950;
    letter-spacing: 0.3px;
    margin-top: 8px;
}

.total-value {
    color: #b85f00;
    font-size: 1.45rem;
    font-weight: 950;
    margin-top: 16px;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 0.92rem;
    padding: 34px 0 42px;
    line-height: 1.7;
}

.footer-note strong {
    color: var(--navy);
}

/* Inputs */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stFileUploader label,
.stSelectbox label,
.stRadio label {
    color: var(--navy) !important;
    font-weight: 850 !important;
    font-size: 0.95rem !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border: 1px solid #d8c6a4 !important;
    border-radius: 14px !important;
}

div[data-baseweb="input"] input,
textarea {
    color: #1f2937 !important;
    background: #ffffff !important;
}

section[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #d8c6a4 !important;
    border-radius: 18px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #475569 !important;
}

section[data-testid="stFileUploaderDropzone"] button {
    background: var(--orange) !important;
    color: #ffffff !important;
    font-weight: 950 !important;
    border-radius: 999px !important;
    border: none !important;
}

section[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}

/* Streamlit button control */
.stButton > button,
button[kind="secondary"],
button[kind="primary"],
.stFormSubmitButton > button {
    border-radius: 999px !important;
    font-weight: 950 !important;
    border: none !important;
    background: var(--orange) !important;
    color: #ffffff !important;
    padding: 0.72rem 1.35rem !important;
    width: auto !important;
    min-width: 190px !important;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p,
.stFormSubmitButton > button p {
    color: #ffffff !important;
    font-weight: 950 !important;
}

@media (max-width: 900px) {
    .hero-grid,
    .included-grid,
    .quota-grid,
    .item-grid,
    .stat-grid {
        grid-template-columns: 1fr;
    }

    .hero-main {
        padding: 54px 0 60px;
    }

    .form-shell {
        width: min(100% - 28px, 980px);
        padding: 26px;
    }

    .content-wrap {
        width: min(100% - 28px, 1180px);
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# CONEXÃO COM SUPABASE
# =========================

@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_KEY"]
    return create_client(url, key)


supabase = get_supabase_client()


# =========================
# FUNÇÕES DE APOIO
# =========================

def html(content: str):
    st.markdown(content, unsafe_allow_html=True)


def money(valor: float):
    return f"R$ {valor:.2f}".replace(".", ",")


def image_as_base64(path: Path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_item_meta(nome_item):
    mapa = {
        "3 refrigerantes de 2 litros": {"emoji": "🥤", "titulo": "Refrigerantes", "subtitulo": "3 refrigerantes de 2 litros"},
        "Arroz doce": {"emoji": "🍚", "titulo": "Arroz doce", "subtitulo": ""},
        "Bolo doce": {"emoji": "🎂", "titulo": "Bolo doce", "subtitulo": ""},
        "Bolo salgado": {"emoji": "🥧", "titulo": "Bolo salgado", "subtitulo": ""},
        "Doces diversos: abóbora, batata doce, cocada etc.": {"emoji": "🍬", "titulo": "Doces diversos", "subtitulo": "abóbora, batata doce, cocada etc."},
        "Milho verde": {"emoji": "🌽", "titulo": "Milho verde", "subtitulo": ""},
        "Paçoca": {"emoji": "🥜", "titulo": "Paçoca", "subtitulo": ""},
        "Pipoca": {"emoji": "🍿", "titulo": "Pipoca", "subtitulo": ""},
        "Sagu": {"emoji": "🍮", "titulo": "Sagu", "subtitulo": ""},
    }
    return mapa.get(nome_item, {"emoji": "🧺", "titulo": nome_item, "subtitulo": ""})


def quota_meta(tipo):
    dados = {
        "completa_50": {
            "emoji": "🎟️",
            "titulo": "Cota R$50",
            "preco": 50.00,
            "descricao": "Para quem não tem tempo. Não precisa levar nenhum prato.",
        },
        "reduzida_25": {
            "emoji": "🧺",
            "titulo": "Cota R$25",
            "preco": 25.00,
            "descricao": "Você ajuda na organização e leva um prato dentre as opções.",
        },
        "minima_5": {
            "emoji": "🤝",
            "titulo": "Cota R$5",
            "preco": 5.00,
            "descricao": "Cota solidária para quem está apertado. Também precisa levar um prato.",
        },
    }
    return dados[tipo]


LIMITES_COTA = {
    "completa_50": 30,
    "reduzida_25": 20,
    "minima_5": 5,
}


# =========================
# FUNÇÕES DE BANCO
# =========================

def buscar_configuracao():
    response = (
        supabase
        .table("configuracoes_evento")
        .select("*")
        .eq("id", 1)
        .single()
        .execute()
    )
    return response.data


def contar_participantes_por_cota(tipo_cota):
    response = (
        supabase
        .table("participantes")
        .select("id", count="exact")
        .eq("tipo_cota", tipo_cota)
        .in_("status_pagamento", ["aguardando_conferencia", "confirmado"])
        .execute()
    )
    return response.count or 0


def buscar_itens_disponiveis():
    itens_response = (
        supabase
        .table("itens_levar")
        .select("*")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )

    participantes_response = (
        supabase
        .table("participantes")
        .select("item_levar")
        .in_("status_pagamento", ["aguardando_conferencia", "confirmado"])
        .execute()
    )

    ocupados = {}
    for participante in participantes_response.data:
        item = participante.get("item_levar")
        if item:
            ocupados[item] = ocupados.get(item, 0) + 1

    disponiveis = []
    for item in itens_response.data:
        nome = item["nome"]
        vagas_total = item["vagas_total"]
        vagas_ocupadas = ocupados.get(nome, 0)
        vagas_restantes = vagas_total - vagas_ocupadas

        if vagas_restantes > 0:
            disponiveis.append({
                "nome": nome,
                "vagas_total": vagas_total,
                "vagas_ocupadas": vagas_ocupadas,
                "vagas_restantes": vagas_restantes,
            })

    return disponiveis


def salvar_comprovante(arquivo, email):
    extensao = arquivo.name.split(".")[-1].lower()
    nome_seguro = email.replace("@", "_").replace(".", "_")
    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome_seguro}_{uuid4()}.{extensao}"

    conteudo = arquivo.getvalue()

    supabase.storage.from_("comprovantes").upload(
        path=nome_arquivo,
        file=conteudo,
        file_options={"content-type": arquivo.type}
    )

    return nome_arquivo


def cadastrar_participantes_grupo(
    responsavel_nome,
    email,
    whatsapp,
    adultos,
    criancas,
    comprovante_url,
):
    total = sum(quota_meta(adulto["tipo_cota"])["preco"] for adulto in adultos)
    familiares_texto = "; ".join(
        [f"Adulto: {a.get('nome') or '-'}" for a in adultos] +
        [f"Criança: {c}" for c in criancas if c]
    )

    registros = []
    for adulto in adultos:
        valor = quota_meta(adulto["tipo_cota"])["preco"]
        registros.append({
            "nome": adulto.get("nome") or responsavel_nome,
            "email": email.strip().lower(),
            "whatsapp": whatsapp.strip(),
            "tipo_cota": adulto["tipo_cota"],
            "valor_cota": valor,
            "item_levar": adulto.get("item_levar"),
            "status_pagamento": "aguardando_conferencia",
            "comprovante_url": comprovante_url,
            "qtd_adultos_pagantes": len(adultos),
            "qtd_criancas_ate_10": len([c for c in criancas if c]),
            "familiares": familiares_texto,
            "valor_total": total,
        })

    return supabase.table("participantes").insert(registros).execute().data


def buscar_participantes():
    response = (
        supabase
        .table("participantes")
        .select("*")
        .order("criado_em", desc=True)
        .execute()
    )
    return response.data


def atualizar_status(participante_id, novo_status):
    (
        supabase
        .table("participantes")
        .update({"status_pagamento": novo_status})
        .eq("id", participante_id)
        .execute()
    )


def gerar_link_comprovante(caminho):
    if not caminho:
        return None
    try:
        response = supabase.storage.from_("comprovantes").create_signed_url(path=caminho, expires_in=3600)
        return response.get("signedURL") or response.get("signedUrl")
    except Exception:
        return None


# =========================
# SESSION STATE
# =========================

if "modo_admin" not in st.session_state:
    st.session_state.modo_admin = False
if "dados_confirmados" not in st.session_state:
    st.session_state.dados_confirmados = False
if "adultos_confirmados" not in st.session_state:
    st.session_state.adultos_confirmados = []
if "criancas_confirmadas" not in st.session_state:
    st.session_state.criancas_confirmadas = []
if "adulto_cotas" not in st.session_state:
    st.session_state.adulto_cotas = {}
if "adulto_itens" not in st.session_state:
    st.session_state.adulto_itens = {}


# =========================
# DADOS PRINCIPAIS
# =========================

config = buscar_configuracao()

ocupacao_cotas = {
    "completa_50": contar_participantes_por_cota("completa_50"),
    "reduzida_25": contar_participantes_por_cota("reduzida_25"),
    "minima_5": contar_participantes_por_cota("minima_5"),
}

vagas_cotas = {
    tipo: max(LIMITES_COTA[tipo] - ocupacao_cotas[tipo], 0)
    for tipo in LIMITES_COTA
}

itens_disponiveis_base = buscar_itens_disponiveis()


# =========================
# ADMIN DISCRETO
# =========================

if st.button("🔒", key="admin_lock", help="Acesso administrativo"):
    st.session_state.modo_admin = not st.session_state.modo_admin
    st.rerun()


# =========================
# HERO FULL WIDTH
# =========================

banner_path = Path(__file__).parent / "banner_festa_julina.png"
if banner_path.exists():
    try:
        b64 = image_as_base64(banner_path)
        html(f'<img class="hero-image-full" src="data:image/png;base64,{b64}" alt="Festa Julina da Mary">')
    except Exception:
        st.error("O banner foi encontrado, mas não pôde ser carregado como imagem.")
else:
    st.error("Banner não encontrado. Confirme se banner_festa_julina.png está na raiz do projeto.")


# =========================
# ADMIN
# =========================

if st.session_state.modo_admin:
    html('<section class="full-section cream-section"><div class="content-wrap"><div class="form-shell"><div class="form-title">Painel administrativo</div><div class="form-subtitle">Acesso restrito à organização.</div>')

    senha_col, btn_col, voltar_col = st.columns([1.8, 0.6, 0.6])
    with senha_col:
        senha = st.text_input("Senha do admin", type="password")
    with btn_col:
        st.write("")
        acessar = st.button("Acessar", use_container_width=True)
    with voltar_col:
        st.write("")
        voltar = st.button("Voltar", use_container_width=True)

    if voltar:
        st.session_state.modo_admin = False
        st.rerun()

    senha_admin = st.secrets.get("ADMIN_PASSWORD", "admin123")

    if acessar and senha != senha_admin:
        st.warning("Senha incorreta.")

    if senha == senha_admin and senha:
        participantes = buscar_participantes()

        if not participantes:
            st.info("Ainda não há participantes cadastrados.")
        else:
            df = pd.DataFrame(participantes)
            total_previsto = df.get("valor_total", df["valor_cota"]).fillna(df["valor_cota"]).sum()
            total_confirmado = df[df["status_pagamento"] == "confirmado"]["valor_cota"].sum()

            c1, c2, c3 = st.columns(3)
            c1.metric("Inscrições adultas", len(df))
            c2.metric("Total previsto", money(float(total_previsto)))
            c3.metric("Total confirmado", money(float(total_confirmado)))

            st.markdown("### Participantes")
            for participante in participantes:
                with st.expander(f"{participante['nome']} - {money(float(participante['valor_cota']))}"):
                    st.write(f"**E-mail:** {participante['email']}")
                    st.write(f"**WhatsApp:** {participante.get('whatsapp', '')}")
                    st.write(f"**Tipo de cota:** {participante['tipo_cota']}")
                    st.write(f"**Item para levar:** {participante.get('item_levar') or '-'}")
                    st.write(f"**Crianças até 10 anos no grupo:** {participante.get('qtd_criancas_ate_10', 0)}")
                    st.write(f"**Familiares/acompanhantes:** {participante.get('familiares') or '-'}")
                    st.write(f"**Status:** {participante['status_pagamento']}")

                    link_comprovante = gerar_link_comprovante(participante.get("comprovante_url"))
                    if link_comprovante:
                        st.link_button("Abrir comprovante", link_comprovante)

                    status_opcoes = ["aguardando_conferencia", "confirmado", "recusado"]
                    novo_status = st.selectbox(
                        "Alterar status",
                        status_opcoes,
                        index=status_opcoes.index(participante["status_pagamento"]),
                        key=f"status_{participante['id']}",
                    )
                    if st.button("Salvar status", key=f"btn_{participante['id']}"):
                        atualizar_status(participante["id"], novo_status)
                        st.success("Status atualizado.")
                        st.rerun()

            st.markdown("### Tabela geral")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("Baixar lista em CSV", data=csv, file_name="participantes_festa_julina_mary.csv", mime="text/csv")

    html('</div></div></section><div class="footer-note">Festa Julina da Mary • Organização das inscrições e contribuições<br><strong>Desenvolvimento by Levz</strong></div>')
    st.stop()


# =========================
# LANDING
# =========================

html("""
<section class="hero-main">
<div class="content-wrap">
<div class="hero-grid">
<div>
<div class="hero-title">A Festa Julina da Mary está chegando. Vem participar com a gente!</div>
<div class="hero-text">Uma noite gostosa, divertida e bem organizada para reunir todo mundo. Quem participar já terá acesso às comidas principais, às brincadeiras, à estrutura preparada e a uma programação cheia de clima julino.</div>
<a class="cta-button" href="#inscricao">Quero me inscrever</a>
</div>
<div class="how-card">
<div class="how-title">Como funciona?</div>
<div class="how-text">Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente. Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.</div>
<div class="quota-line">🎟️ <strong>Cota R$50:</strong> esta cota é para quem não tem tempo. Com ela você não precisa levar nenhum prato.</div>
<div class="quota-line">🧺 <strong>Cota R$25:</strong> com esta cota, você ajuda na organização e leva um prato dentre as opções.</div>
<div class="quota-line">🤝 <strong>Cota R$5:</strong> cota solidária para quem está apertado. Você ajuda de forma simbólica e leva um prato dentre as opções.</div>
<div class="how-text" style="margin-top:18px;">A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.</div>
</div>
</div>
</div>
</section>
""")

html("""
<section class="yellow-band">
<div class="content-wrap">
<div class="section-title-center">O que já está incluso para quem participar?</div>
<div class="section-subtitle-center">A festa já está sendo preparada com comidas, estrutura e atrações para todo mundo aproveitar.</div>
<div class="included-grid">
<div class="included-card"><div class="included-emoji">🥟</div><div>Bolinho caipira</div></div>
<div class="included-card"><div class="included-emoji">🍲</div><div>Caldinhos</div></div>
<div class="included-card"><div class="included-emoji">🌭</div><div>Cachorro-quente</div></div>
<div class="included-card"><div class="included-emoji">🥤</div><div>Refrigerante</div></div>
<div class="included-card"><div class="included-emoji">🎤</div><div>Karaokê</div></div>
<div class="included-card"><div class="included-emoji">📺</div><div>Telão interativo</div></div>
<div class="included-card"><div class="included-emoji">🎯</div><div>Bingo</div></div>
<div class="included-card"><div class="included-emoji">🔥</div><div>Fogueira</div></div>
<div class="included-card"><div class="included-emoji">💋</div><div>Barraca do beijo</div></div>
<div class="included-card"><div class="included-emoji">🎣</div><div>Pescaria infantil</div></div>
<div class="included-card"><div class="included-emoji">💃</div><div>Quadrilha</div></div>
<div class="included-card"><div class="included-emoji">🎊</div><div>Decoração temática</div></div>
</div>
<div class="note-card-wide">🍻 <strong>Bebidas alcoólicas:</strong> cada pessoa leva a sua, caso queira consumir. &nbsp;•&nbsp; 🎁 <strong>Prendas para o bingo:</strong> quem quiser colaborar pode levar prendas extras à vontade.</div>
</div>
</section>
""")


# =========================
# INSCRIÇÃO - ETAPA 1
# =========================

html('<section id="inscricao" class="form-section cream-section"><div class="form-shell"><div class="form-title">Inscreva sua família</div><div class="form-subtitle">Primeiro, preencha os dados do responsável e informe quem vai participar. Depois disso, você escolherá a cota e o item de cada adulto.</div>')

if not st.session_state.dados_confirmados:
    with st.form("form_dados_familia", clear_on_submit=False):
        responsavel_nome = st.text_input("Nome completo do responsável")
        col_email, col_whatsapp = st.columns(2)
        with col_email:
            email = st.text_input("E-mail")
        with col_whatsapp:
            whatsapp = st.text_input("WhatsApp")

        col_adultos, col_criancas = st.columns(2)
        with col_adultos:
            qtd_adultos = st.number_input("Adultos pagantes", min_value=1, max_value=10, value=1, step=1)
        with col_criancas:
            qtd_criancas = st.number_input("Crianças até 10 anos", min_value=0, max_value=10, value=0, step=1)

        st.markdown('<div class="step-title">Nomes dos adultos</div>', unsafe_allow_html=True)
        nomes_adultos = []
        for i in range(1, int(qtd_adultos) + 1):
            nomes_adultos.append(st.text_input(f"Nome do adulto {i}", key=f"pre_adulto_{i}", placeholder="Pode repetir o nome do responsável, se for o caso"))

        nomes_criancas = []
        if int(qtd_criancas) > 0:
            st.markdown('<div class="step-title">Nomes das crianças até 10 anos</div>', unsafe_allow_html=True)
            for i in range(1, int(qtd_criancas) + 1):
                nomes_criancas.append(st.text_input(f"Nome da criança {i}", key=f"pre_crianca_{i}"))

        confirmar_dados = st.form_submit_button("Continuar para escolher as cotas")

        if confirmar_dados:
            if not responsavel_nome or not email or not whatsapp:
                st.error("Preencha nome do responsável, e-mail e WhatsApp.")
            elif any(not nome for nome in nomes_adultos):
                st.error("Preencha o nome de todos os adultos pagantes.")
            elif any(not nome for nome in nomes_criancas):
                st.error("Preencha o nome das crianças ou reduza a quantidade informada.")
            else:
                st.session_state.responsavel_nome = responsavel_nome
                st.session_state.email = email
                st.session_state.whatsapp = whatsapp
                st.session_state.adultos_confirmados = nomes_adultos
                st.session_state.criancas_confirmadas = nomes_criancas
                st.session_state.dados_confirmados = True
                st.rerun()

else:
    st.success("Dados da família confirmados. Agora escolha a cota de cada adulto.")
    if st.button("Editar dados da família"):
        st.session_state.dados_confirmados = False
        st.rerun()

html('</div></section>')


# =========================
# INSCRIÇÃO - ETAPA 2
# =========================

if st.session_state.dados_confirmados:
    html('<section class="form-section cream-section" style="padding-top:0;"><div class="form-shell"><div class="form-title">Escolha as cotas</div><div class="form-subtitle">Selecione uma cota para cada adulto. Quem escolher R$25 ou R$5 também precisa selecionar um item para levar.</div>')

    html(f"""
    <div class="stat-grid">
    <div class="stat-card"><div class="stat-label">Cotas R$50 disponíveis</div><div class="stat-value">{vagas_cotas['completa_50']}</div></div>
    <div class="stat-card"><div class="stat-label">Cotas R$25 + item disponíveis</div><div class="stat-value">{vagas_cotas['reduzida_25']}</div></div>
    <div class="stat-card"><div class="stat-label">Cotas solidárias R$5 disponíveis</div><div class="stat-value">{vagas_cotas['minima_5']}</div></div>
    </div>
    """)

    for idx, nome_adulto in enumerate(st.session_state.adultos_confirmados, start=1):
        html(f'<div class="person-box"><div class="person-title">Adulto {idx}: {nome_adulto}</div>')
        cols = st.columns(3)
        for col, tipo in zip(cols, ["completa_50", "reduzida_25", "minima_5"]):
            meta = quota_meta(tipo)
            selecionado = st.session_state.adulto_cotas.get(idx) == tipo
            classe = "quota-card-selected" if selecionado else "quota-card"
            with col:
                st.markdown(
                    f"""
                    <div class="{classe}">
                    <div class="quota-title">{meta['emoji']} {meta['titulo']}</div>
                    <div class="quota-price">{money(meta['preco'])}</div>
                    <div class="quota-desc">{meta['descricao']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Selecionar" if not selecionado else "Selecionado", key=f"cota_{idx}_{tipo}", use_container_width=True):
                    st.session_state.adulto_cotas[idx] = tipo
                    if tipo == "completa_50":
                        st.session_state.adulto_itens.pop(idx, None)
                    st.rerun()

        tipo_atual = st.session_state.adulto_cotas.get(idx)
        if tipo_atual in ["reduzida_25", "minima_5"]:
            st.markdown("**Escolha o item que este adulto vai levar:**")

            itens_ja_escolhidos = [
                item for adulto_idx, item in st.session_state.adulto_itens.items()
                if adulto_idx != idx and item
            ]
            contagem_local = Counter(itens_ja_escolhidos)
            opcoes_itens = []
            for item in itens_disponiveis_base:
                restantes = item["vagas_restantes"] - contagem_local.get(item["nome"], 0)
                if restantes > 0:
                    opcoes_itens.append({**item, "restantes_local": restantes})

            for linha in range(0, len(opcoes_itens), 3):
                item_cols = st.columns(3)
                for col, item in zip(item_cols, opcoes_itens[linha:linha + 3]):
                    meta_item = get_item_meta(item["nome"])
                    selecionado_item = st.session_state.adulto_itens.get(idx) == item["nome"]
                    classe_item = "item-card-selected" if selecionado_item else "item-card"
                    with col:
                        st.markdown(
                            f"""
                            <div class="{classe_item}">
                            <div class="included-emoji">{meta_item['emoji']}</div>
                            <div class="item-title">{meta_item['titulo']}</div>
                            <div class="item-meta">{item['restantes_local']} vaga(s)</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button("Selecionar" if not selecionado_item else "Selecionado", key=f"item_{idx}_{item['nome']}", use_container_width=True):
                            st.session_state.adulto_itens[idx] = item["nome"]
                            st.rerun()
        html('</div>')

    adultos_final = []
    for idx, nome_adulto in enumerate(st.session_state.adultos_confirmados, start=1):
        tipo = st.session_state.adulto_cotas.get(idx)
        adultos_final.append({
            "nome": nome_adulto,
            "tipo_cota": tipo,
            "item_levar": st.session_state.adulto_itens.get(idx),
        })

    cotas_ok = all(adulto["tipo_cota"] for adulto in adultos_final)
    itens_ok = all(
        adulto["tipo_cota"] == "completa_50" or adulto.get("item_levar")
        for adulto in adultos_final
        if adulto["tipo_cota"]
    )

    contagem_cotas_form = Counter([a["tipo_cota"] for a in adultos_final if a["tipo_cota"]])
    erros_disponibilidade = []
    for tipo, qtd in contagem_cotas_form.items():
        if qtd > vagas_cotas[tipo]:
            erros_disponibilidade.append(f"{quota_meta(tipo)['titulo']}: selecionadas {qtd}, disponíveis {vagas_cotas[tipo]}.")

    if cotas_ok:
        total = sum(quota_meta(adulto["tipo_cota"])["preco"] for adulto in adultos_final)
        resumo_linhas = "".join(
            f"<div class='payment-line'><strong>{adulto['nome']}:</strong> {quota_meta(adulto['tipo_cota'])['titulo']} • Item: {adulto.get('item_levar') or '-'}</div>"
            for adulto in adultos_final
        )
        criancas_txt = ", ".join(st.session_state.criancas_confirmadas) if st.session_state.criancas_confirmadas else "-"

        html(f"""
        <div class="payment-card-main">
        <div class="form-title">Resumo e pagamento</div>
        <div class="payment-grid">
        <div class="payment-block">
        <div class="payment-block-title">Resumo da inscrição</div>
        {resumo_linhas}
        <div class="payment-line"><strong>Crianças até 10 anos:</strong> {criancas_txt}</div>
        <div class="payment-line total-value">Total do Pix: {money(total)}</div>
        </div>
        <div class="payment-block">
        <div class="payment-block-title">Dados do Recebedor</div>
        <div class="payment-line">Copie o código Pix abaixo:</div>
        <div class="pix-key">{config['chave_pix']}</div>
        </div>
        <div class="payment-block">
        <div class="payment-block-title">Anexo do Comprovante</div>
        </div>
        """)

        comprovante = st.file_uploader("Anexe o comprovante do Pix", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
        html('</div></div>')

        col_submit_1, col_submit_2, col_submit_3 = st.columns([1, 1, 1])
        with col_submit_2:
            enviar = st.button("Confirmar minha inscrição", key="confirmar_inscricao", use_container_width=True)

        if enviar:
            if erros_disponibilidade:
                st.error("Não há vagas suficientes para as cotas escolhidas: " + " ".join(erros_disponibilidade))
            elif not itens_ok:
                st.error("Todos os adultos com cota R$25 ou R$5 precisam escolher um item para levar.")
            elif not comprovante:
                st.error("Anexe o comprovante do Pix.")
            else:
                try:
                    comprovante_url = salvar_comprovante(comprovante, st.session_state.email)
                    cadastrar_participantes_grupo(
                        responsavel_nome=st.session_state.responsavel_nome,
                        email=st.session_state.email,
                        whatsapp=st.session_state.whatsapp,
                        adultos=adultos_final,
                        criancas=st.session_state.criancas_confirmadas,
                        comprovante_url=comprovante_url,
                    )
                    st.success("Inscrição enviada com sucesso! O pagamento ficará aguardando conferência da organização.")
                    st.balloons()
                except Exception as erro:
                    st.error("Não foi possível salvar sua inscrição.")
                    st.exception(erro)

    html('</div></section>')


# =========================
# FOOTER
# =========================

html("""
<div class="footer-note">
Festa Julina da Mary • Organização das inscrições e contribuições<br>
<strong>Desenvolvimento by Levz</strong>
</div>
""")
