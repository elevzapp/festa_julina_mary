
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from collections import Counter

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
    --paper: #fffdf8;
    --white: #ffffff;
    --navy: #12355b;
    --navy-2: #1e4d80;
    --orange: #df7f00;
    --orange-2: #bf6900;
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

/* Layout */
.page-shell {
    width: 100%;
}

.top-admin {
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 1000;
}

.content-wrap {
    width: min(1120px, calc(100% - 40px));
    margin: 0 auto;
}

.hero-section {
    background: linear-gradient(180deg, #fff4df 0%, #fffaf0 100%);
    padding: 28px 0 52px;
}

.hero-image-card {
    width: min(1120px, calc(100% - 40px));
    margin: 0 auto;
}

.hero-image-card img {
    width: 100%;
    border-radius: 28px;
    box-shadow: 0 18px 44px rgba(90, 60, 20, 0.16);
    border: 1px solid var(--line);
}

/* Section blocks */
.full-section {
    padding: 76px 0;
}

.white-section {
    background: #ffffff;
}

.cream-section {
    background: #fff4df;
}

.yellow-band {
    background: #f6c453;
    padding: 68px 0;
}

.section-title-center {
    text-align: center;
    font-size: clamp(2rem, 4vw, 3rem);
    line-height: 1.1;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 18px;
}

.section-subtitle-center {
    text-align: center;
    font-size: 1.1rem;
    line-height: 1.7;
    color: #405168;
    max-width: 820px;
    margin: 0 auto 34px;
}

.intro-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 34px;
    align-items: center;
}

.intro-title {
    font-size: clamp(2.4rem, 5vw, 4.2rem);
    font-weight: 950;
    line-height: 1.05;
    color: var(--navy);
    margin-bottom: 20px;
    letter-spacing: -0.03em;
}

.intro-text {
    font-size: 1.13rem;
    line-height: 1.75;
    color: #405168;
    margin-bottom: 26px;
}

.info-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 14px 34px rgba(90, 60, 20, 0.10);
}

.how-card {
    background: #fff7e6;
    border: 1px solid var(--soft-line);
    border-left: 8px solid var(--orange);
    border-radius: 24px;
    padding: 26px;
}

.how-title {
    color: var(--navy);
    font-weight: 900;
    font-size: 1.55rem;
    margin-bottom: 18px;
}

.how-text {
    color: #405168;
    line-height: 1.75;
    font-size: 1.05rem;
    margin-bottom: 18px;
}

.quota-line {
    margin: 10px 0;
    font-size: 1.02rem;
    line-height: 1.55;
}

.quota-line strong {
    color: var(--navy);
}

/* Included items */
.included-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-top: 30px;
}

.included-pill {
    background: var(--paper);
    border: 1px solid var(--soft-line);
    border-radius: 22px;
    padding: 18px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    min-height: 74px;
    box-shadow: 0 8px 20px rgba(90, 60, 20, 0.07);
    font-weight: 850;
    color: var(--navy);
}

.included-emoji {
    font-size: 1.45rem;
    flex: 0 0 auto;
}

.note-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 28px;
}

.note-card {
    background: #eef6ff;
    border: 1px solid #c7ddf7;
    border-radius: 22px;
    padding: 20px;
    color: #244766;
    line-height: 1.55;
}

.note-card strong {
    color: var(--navy);
}

/* CTA */
.cta-wrap {
    margin-top: 30px;
}

a.cta-button,
.cta-button {
    display: inline-block;
    background: var(--orange);
    color: #ffffff !important;
    font-weight: 900;
    text-decoration: none !important;
    padding: 15px 34px;
    border-radius: 999px;
    box-shadow: 0 10px 22px rgba(150, 80, 0, 0.18);
    text-align: center;
}

a.cta-button:hover,
.cta-button:hover {
    background: var(--orange-2);
    color: #ffffff !important;
}

/* Forms */
.form-shell {
    background: #ffffff;
    border-radius: 32px;
    border: 1px solid var(--line);
    box-shadow: 0 16px 44px rgba(90, 60, 20, 0.10);
    padding: 38px;
    margin-top: 28px;
}

.form-title {
    font-size: clamp(2rem, 4vw, 3rem);
    color: var(--navy);
    font-weight: 950;
    margin-bottom: 10px;
    letter-spacing: -0.03em;
}

.form-subtitle {
    color: #405168;
    line-height: 1.65;
    font-size: 1.05rem;
    margin-bottom: 30px;
}

.step-title {
    font-size: 1.8rem;
    color: var(--navy);
    font-weight: 900;
    margin: 36px 0 16px;
}

.step-subtitle {
    color: var(--muted);
    margin-top: -8px;
    margin-bottom: 18px;
}

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 22px;
}

.stat-card {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 22px;
    min-height: 120px;
}

.stat-label {
    color: var(--muted);
    font-weight: 700;
    margin-bottom: 8px;
}

.stat-value {
    color: var(--navy);
    font-size: 2.25rem;
    font-weight: 950;
}

/* Adult cards */
.adult-card {
    background: #fffaf0;
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 24px;
    margin: 18px 0 26px;
}

.adult-title {
    font-size: 1.35rem;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 14px;
}

.quota-card,
.quota-card-selected {
    border-radius: 24px;
    padding: 22px;
    min-height: 210px;
    box-shadow: 0 8px 22px rgba(90, 60, 20, 0.06);
    margin-bottom: 12px;
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
    font-size: 1.35rem;
    font-weight: 950;
    color: var(--navy);
    margin-bottom: 8px;
}

.quota-price {
    font-size: 2.2rem;
    font-weight: 950;
    color: #b85f00;
    margin-bottom: 10px;
}

.quota-card-selected .quota-price {
    color: #3f7d07;
}

.quota-desc {
    font-size: 0.98rem;
    color: #475569;
    line-height: 1.5;
}

/* Payment */
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
    font-weight: 900;
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
    font-weight: 900;
    letter-spacing: 0.3px;
    margin-top: 8px;
}

.total-value {
    color: #b85f00;
    font-size: 1.55rem;
    font-weight: 950;
}

/* Footer */
.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 0.95rem;
    padding: 34px 20px;
    line-height: 1.7;
}

.footer-note strong {
    color: var(--navy);
}

/* Widgets */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stRadio label,
.stTextArea label,
.stFileUploader label {
    color: var(--navy) !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    background: #ffffff !important;
    border: 1px solid #d8c6a4 !important;
    border-radius: 14px !important;
    min-height: 44px !important;
    color: #1f2937 !important;
}

input, textarea {
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
    font-weight: 900 !important;
    border-radius: 999px !important;
    border: none !important;
}

section[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}

.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    border-radius: 999px !important;
    font-weight: 900 !important;
    border: none !important;
    background: var(--orange) !important;
    color: #ffffff !important;
    padding: 0.76rem 1.25rem !important;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    color: #ffffff !important;
    font-weight: 900 !important;
}

.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover {
    background: var(--orange-2) !important;
    color: #ffffff !important;
    border: none !important;
}

.admin-lock button {
    background: transparent !important;
    color: #111827 !important;
    box-shadow: none !important;
    padding: 0 !important;
    border: none !important;
}

@media (max-width: 900px) {
    .intro-grid,
    .note-grid {
        grid-template-columns: 1fr;
    }

    .included-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .stat-grid {
        grid-template-columns: 1fr;
    }

    .form-shell {
        padding: 24px;
    }
}

@media (max-width: 560px) {
    .included-grid {
        grid-template-columns: 1fr;
    }

    .content-wrap,
    .hero-image-card {
        width: min(100% - 24px, 1120px);
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
    st.markdown("".join(line.strip() for line in content.strip().splitlines()), unsafe_allow_html=True)


def money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def get_item_meta(nome_item):
    mapa = {
        "3 refrigerantes de 2 litros": {
            "emoji": "🥤",
            "titulo": "Refrigerantes",
            "subtitulo": "3 refrigerantes de 2 litros",
        },
        "Arroz doce": {"emoji": "🍚", "titulo": "Arroz doce", "subtitulo": ""},
        "Bolo doce": {"emoji": "🎂", "titulo": "Bolo doce", "subtitulo": ""},
        "Bolo salgado": {"emoji": "🥧", "titulo": "Bolo salgado", "subtitulo": ""},
        "Doces diversos: abóbora, batata doce, cocada etc.": {
            "emoji": "🍬",
            "titulo": "Doces diversos",
            "subtitulo": "abóbora, batata doce, cocada etc.",
        },
        "Milho verde": {"emoji": "🌽", "titulo": "Milho verde", "subtitulo": ""},
        "Paçoca": {"emoji": "🥜", "titulo": "Paçoca", "subtitulo": ""},
        "Pipoca": {"emoji": "🍿", "titulo": "Pipoca", "subtitulo": ""},
        "Sagu": {"emoji": "🍮", "titulo": "Sagu", "subtitulo": ""},
    }
    return mapa.get(nome_item, {"emoji": "🧺", "titulo": nome_item, "subtitulo": ""})


def quota_meta(tipo):
    metas = {
        "completa_50": {
            "emoji": "🎟️",
            "titulo": "Cota R$50",
            "preco": 50.0,
            "descricao": "Para quem não tem tempo. Você não precisa levar nenhum prato.",
        },
        "reduzida_25": {
            "emoji": "🧺",
            "titulo": "Cota R$25",
            "preco": 25.0,
            "descricao": "Você ajuda na organização e leva um prato dentre as opções.",
        },
        "minima_5": {
            "emoji": "🤝",
            "titulo": "Cota R$5",
            "preco": 5.0,
            "descricao": "Cota solidária para quem está apertado. Você ajuda de forma simbólica e leva um prato.",
        },
    }
    return metas[tipo]


# =========================
# FUNÇÕES DE BANCO
# =========================

def buscar_configuracao():
    response = (
        supabase.table("configuracoes_evento")
        .select("*")
        .eq("id", 1)
        .single()
        .execute()
    )
    return response.data


def contar_participantes_por_cota(tipo_cota):
    response = (
        supabase.table("participantes")
        .select("id", count="exact")
        .eq("tipo_cota", tipo_cota)
        .in_("status_pagamento", ["aguardando_conferencia", "confirmado"])
        .execute()
    )
    return response.count or 0


def buscar_itens_disponiveis():
    itens_response = (
        supabase.table("itens_levar")
        .select("*")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )

    participantes_response = (
        supabase.table("participantes")
        .select("item_levar")
        .in_("tipo_cota", ["reduzida_25", "minima_5"])
        .in_("status_pagamento", ["aguardando_conferencia", "confirmado"])
        .execute()
    )

    ocupados = Counter()
    for participante in participantes_response.data:
        item = participante.get("item_levar")
        if item:
            ocupados[item] += 1

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
    nome_arquivo = (
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
        f"{nome_seguro}_{uuid4()}.{extensao}"
    )

    supabase.storage.from_("comprovantes").upload(
        path=nome_arquivo,
        file=arquivo.getvalue(),
        file_options={"content-type": arquivo.type},
    )

    return nome_arquivo


def cadastrar_participantes_grupo(
    responsavel_nome,
    email,
    whatsapp,
    adultos,
    qtd_criancas,
    familiares,
    comprovante_url,
):
    total = sum(quota_meta(adulto["tipo_cota"])["preco"] for adulto in adultos)
    payload = []

    for idx, adulto in enumerate(adultos, start=1):
        meta = quota_meta(adulto["tipo_cota"])
        nome_adulto = adulto.get("nome") or f"Adulto {idx}"

        payload.append({
            "nome": f"{responsavel_nome.strip()} | {nome_adulto.strip()}",
            "email": email.strip().lower(),
            "whatsapp": whatsapp.strip(),
            "tipo_cota": adulto["tipo_cota"],
            "valor_cota": meta["preco"],
            "item_levar": adulto.get("item_levar"),
            "status_pagamento": "aguardando_conferencia",
            "comprovante_url": comprovante_url,
            "qtd_adultos_pagantes": len(adultos),
            "qtd_criancas_ate_10": qtd_criancas,
            "familiares": familiares.strip(),
            "valor_total": total,
        })

    response = supabase.table("participantes").insert(payload).execute()
    return response.data


def buscar_participantes():
    response = (
        supabase.table("participantes")
        .select("*")
        .order("criado_em", desc=True)
        .execute()
    )
    return response.data


def atualizar_status(participante_id, novo_status):
    (
        supabase.table("participantes")
        .update({"status_pagamento": novo_status})
        .eq("id", participante_id)
        .execute()
    )


def gerar_link_comprovante(caminho):
    if not caminho:
        return None

    try:
        response = supabase.storage.from_("comprovantes").create_signed_url(
            path=caminho,
            expires_in=3600,
        )
        return response.get("signedURL") or response.get("signedUrl")
    except Exception:
        return None


# =========================
# SESSION STATE
# =========================

if "mostrar_inscricao" not in st.session_state:
    st.session_state.mostrar_inscricao = False

if "tipo_cota_adulto" not in st.session_state:
    st.session_state.tipo_cota_adulto = {}

if "item_adulto" not in st.session_state:
    st.session_state.item_adulto = {}


def iniciar_inscricao():
    st.session_state.mostrar_inscricao = True


def selecionar_cota(adulto_idx, tipo):
    st.session_state.tipo_cota_adulto[adulto_idx] = tipo
    if tipo == "completa_50":
        st.session_state.item_adulto[adulto_idx] = None


def selecionar_item(adulto_idx, item_nome):
    st.session_state.item_adulto[adulto_idx] = item_nome


# =========================
# DADOS PRINCIPAIS
# =========================

config = buscar_configuracao()

LIMITES_COTA = {
    "completa_50": int(config["limite_cota_50"]),
    "reduzida_25": int(config["limite_cota_25"]),
    "minima_5": 5,
}

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

admin_col_1, admin_col_2 = st.columns([14, 1])
with admin_col_2:
    if st.button("🔒", key="admin_lock", help="Acesso administrativo"):
        st.session_state["modo_admin"] = not st.session_state.get("modo_admin", False)


# =========================
# HERO
# =========================

html('<div class="page-shell"><section class="hero-section"><div class="hero-image-card">')

banner_path = Path(__file__).parent / "banner_festa_julina.png"

if banner_path.exists():
    try:
        st.image(str(banner_path), use_container_width=True)
    except Exception:
        st.error("O banner foi encontrado, mas não pôde ser carregado como imagem.")
else:
    st.error("Banner não encontrado. Confirme se banner_festa_julina.png está na raiz do projeto.")

html('</div></section></div>')


# =========================
# ADMIN
# =========================

if st.session_state.get("modo_admin", False):
    html('<section class="full-section cream-section"><div class="content-wrap"><div class="form-shell"><div class="form-title">Painel administrativo</div><div class="form-subtitle">Acesso restrito à organização.</div>')

    senha_col, btn_col, voltar_col = st.columns([2, 0.8, 0.8])
    with senha_col:
        senha = st.text_input("Senha do admin", type="password")
    with btn_col:
        st.write("")
        acessar = st.button("Acessar", use_container_width=True)
    with voltar_col:
        st.write("")
        voltar = st.button("Voltar", use_container_width=True)

    if voltar:
        st.session_state["modo_admin"] = False
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

                    comprovante_path = participante.get("comprovante_url")
                    link_comprovante = gerar_link_comprovante(comprovante_path)

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
            st.download_button(
                "Baixar lista em CSV",
                data=csv,
                file_name="participantes_festa_julina_mary.csv",
                mime="text/csv",
            )

    html('</div></div></section><div class="footer-note">Festa Julina da Mary • Organização das inscrições e contribuições<br><strong>Desenvolvimento by Levz</strong></div>')
    st.stop()


# =========================
# LANDING
# =========================

html("""
<section class="full-section white-section">
<div class="content-wrap">
<div class="intro-grid">
<div>
<div class="intro-title">A Festa Julina da Mary está chegando. Vem participar com a gente!</div>
<div class="intro-text">Uma noite gostosa, divertida e bem organizada para reunir todo mundo. Quem participar já terá acesso às comidas principais, às brincadeiras, à estrutura preparada e a uma programação cheia de clima julino.</div>
<div class="cta-wrap"><a class="cta-button" href="#inscricao">Quero me inscrever</a></div>
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
<div class="included-pill"><span class="included-emoji">🥟</span>Bolinho caipira</div>
<div class="included-pill"><span class="included-emoji">🍲</span>Caldinhos</div>
<div class="included-pill"><span class="included-emoji">🌭</span>Cachorro-quente</div>
<div class="included-pill"><span class="included-emoji">🥤</span>Refrigerante</div>
<div class="included-pill"><span class="included-emoji">🎤</span>Karaokê</div>
<div class="included-pill"><span class="included-emoji">📺</span>Telão interativo</div>
<div class="included-pill"><span class="included-emoji">🎯</span>Bingo</div>
<div class="included-pill"><span class="included-emoji">🔥</span>Fogueira</div>
<div class="included-pill"><span class="included-emoji">💋</span>Barraca do beijo</div>
<div class="included-pill"><span class="included-emoji">🎣</span>Pescaria infantil</div>
<div class="included-pill"><span class="included-emoji">💃</span>Quadrilha</div>
<div class="included-pill"><span class="included-emoji">🎊</span>Decoração temática</div>
</div>
<div class="note-grid">
<div class="note-card">🍻 <strong>Bebidas alcoólicas:</strong> cada pessoa leva a sua, caso queira consumir.</div>
<div class="note-card">🎁 <strong>Prendas para o bingo:</strong> quem quiser colaborar pode levar prendas extras à vontade.</div>
</div>
</div>
</section>
""")


# =========================
# INSCRIÇÃO
# =========================

html('<section id="inscricao" class="full-section cream-section"><div class="content-wrap"><div class="form-shell"><div class="form-title">Inscreva sua família</div><div class="form-subtitle">Preencha os dados do responsável, informe quantos adultos participarão e escolha a cota de cada adulto. Crianças até 10 anos não pagam.</div>')

with st.form("form_inscricao_familia", clear_on_submit=False):
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

    familiares = st.text_area(
        "Nomes dos familiares/acompanhantes",
        placeholder="Ex.: João, Ana, Pedro (criança), Mariana...",
        height=90,
    )

    st.markdown('<div class="step-title">Cotas disponíveis</div>', unsafe_allow_html=True)
    html(f"""
    <div class="stat-grid">
    <div class="stat-card"><div class="stat-label">Cotas R$50 disponíveis</div><div class="stat-value">{vagas_cotas["completa_50"]}</div></div>
    <div class="stat-card"><div class="stat-label">Cotas R$25 + item disponíveis</div><div class="stat-value">{vagas_cotas["reduzida_25"]}</div></div>
    <div class="stat-card"><div class="stat-label">Cotas solidárias R$5 disponíveis</div><div class="stat-value">{vagas_cotas["minima_5"]}</div></div>
    </div>
    """)

    adultos = []
    escolhas_cotas = []

    for adulto_idx in range(1, int(qtd_adultos) + 1):
        html(f'<div class="adult-card"><div class="adult-title">Adulto {adulto_idx}</div></div>')

        nome_adulto = st.text_input(
            f"Nome do adulto {adulto_idx}",
            key=f"nome_adulto_{adulto_idx}",
            placeholder="Pode repetir o nome do responsável, se for o caso",
        )

        tipo_cota = st.radio(
            f"Escolha a cota do adulto {adulto_idx}",
            options=["completa_50", "reduzida_25", "minima_5"],
            format_func=lambda tipo: quota_meta(tipo)["titulo"],
            horizontal=True,
            key=f"tipo_cota_{adulto_idx}",
        )

        escolhas_cotas.append(tipo_cota)

        meta_cota = quota_meta(tipo_cota)

        st.markdown(
            f"""
            <div class="quota-card-selected">
                <div class="quota-title">{meta_cota['emoji']} {meta_cota['titulo']}</div>
                <div class="quota-price">{money(meta_cota['preco'])}</div>
                <div class="quota-desc">{meta_cota['descricao']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        item_levar = None

        if tipo_cota in ["reduzida_25", "minima_5"]:
            # Calcula disponibilidade do item considerando escolhas anteriores na mesma inscrição
            itens_ja_escolhidos = [
                adulto.get("item_levar")
                for adulto in adultos
                if adulto.get("item_levar")
            ]
            contagem_local = Counter(itens_ja_escolhidos)

            opcoes_itens = []
            for item in itens_disponiveis_base:
                restantes = item["vagas_restantes"] - contagem_local.get(item["nome"], 0)
                if restantes > 0:
                    meta_item = get_item_meta(item["nome"])
                    opcoes_itens.append((item["nome"], f"{meta_item['emoji']} {meta_item['titulo']} — {restantes} vaga(s)"))

            if opcoes_itens:
                item_levar = st.selectbox(
                    f"Item que o adulto {adulto_idx} vai levar",
                    options=[item[0] for item in opcoes_itens],
                    format_func=lambda nome: next(label for value, label in opcoes_itens if value == nome),
                    key=f"item_adulto_{adulto_idx}",
                )
            else:
                st.warning("Não há mais itens disponíveis para esta cota.")

        adultos.append({
            "nome": nome_adulto,
            "tipo_cota": tipo_cota,
            "item_levar": item_levar,
        })

    total = sum(quota_meta(adulto["tipo_cota"])["preco"] for adulto in adultos)

    # Validação visual de disponibilidade de cotas
    contagem_cotas_form = Counter(escolhas_cotas)
    erros_disponibilidade = []
    for tipo, qtd in contagem_cotas_form.items():
        if qtd > vagas_cotas[tipo]:
            erros_disponibilidade.append(
                f"{quota_meta(tipo)['titulo']}: selecionadas {qtd}, disponíveis {vagas_cotas[tipo]}."
            )

    st.markdown('<div class="step-title">Resumo e pagamento</div>', unsafe_allow_html=True)

    resumo_linhas = "".join(
        f"<div class='payment-line'><strong>Adulto {idx}:</strong> {adulto.get('nome') or '-'} • {quota_meta(adulto['tipo_cota'])['titulo']} • Item: {adulto.get('item_levar') or '-'}</div>"
        for idx, adulto in enumerate(adultos, start=1)
    )

    st.markdown(
        f"""
        <div class="payment-grid">
            <div class="payment-block">
                <div class="payment-block-title">Resumo da inscrição</div>
                {resumo_linhas}
                <div class="payment-line"><strong>Crianças até 10 anos:</strong> {int(qtd_criancas)}</div>
                <div class="payment-line total-value">Total do Pix: {money(total)}</div>
            </div>
            <div class="payment-block">
                <div class="payment-block-title">Dados do Recebedor</div>
                <div class="payment-line">Copie o código Pix abaixo:</div>
                <div class="pix-key">{config["chave_pix"]}</div>
            </div>
            <div class="payment-block">
                <div class="payment-block-title">Anexo do Comprovante</div>
        """,
        unsafe_allow_html=True,
    )

    comprovante = st.file_uploader(
        "Anexe o comprovante do Pix",
        type=["png", "jpg", "jpeg", "pdf"],
        label_visibility="collapsed",
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    enviar = st.form_submit_button("Confirmar minha inscrição", use_container_width=True)

    if enviar:
        if not responsavel_nome or not email or not whatsapp:
            st.error("Preencha nome do responsável, e-mail e WhatsApp.")
        elif erros_disponibilidade:
            st.error("Não há vagas suficientes para as cotas escolhidas: " + " ".join(erros_disponibilidade))
        elif any(adulto["tipo_cota"] in ["reduzida_25", "minima_5"] and not adulto.get("item_levar") for adulto in adultos):
            st.error("Todos os adultos com cota R$25 ou R$5 precisam escolher um item para levar.")
        elif not comprovante:
            st.error("Anexe o comprovante do Pix.")
        else:
            try:
                comprovante_url = salvar_comprovante(comprovante, email)

                cadastrar_participantes_grupo(
                    responsavel_nome=responsavel_nome,
                    email=email,
                    whatsapp=whatsapp,
                    adultos=adultos,
                    qtd_criancas=int(qtd_criancas),
                    familiares=familiares,
                    comprovante_url=comprovante_url,
                )

                st.success("Inscrição enviada com sucesso! O pagamento ficará aguardando conferência da organização.")
                st.balloons()

            except Exception as erro:
                st.error("Não foi possível salvar sua inscrição.")
                st.exception(erro)

html('</div></div></section>')


# =========================
# FOOTER
# =========================

html("""
<div class="footer-note">
Festa Julina da Mary • Organização das inscrições e contribuições<br>
<strong>Desenvolvimento by Levz</strong>
</div>
""")
