from datetime import datetime
from pathlib import Path
from textwrap import dedent
from urllib.parse import quote, unquote
from uuid import uuid4

import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Festa Julina da Mary",
    page_icon="🌽",
    layout="centered",
)


# =========================
# ESTILO VISUAL
# =========================

st.markdown(
    """
<style>
:root {
    --bg: #fff7ed;
    --paper: #ffffff;
    --paper-soft: #fffaf0;
    --navy: #12355b;
    --blue: #1d4f80;
    --orange: #df7f00;
    --orange-dark: #bf6900;
    --line: #ead9bc;
    --line-strong: #e7bd76;
    --text: #26384d;
    --muted: #64748b;
    --green: #5f9f1f;
    --green-bg: #eef8d8;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.main .block-container {
    max-width: 1080px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: var(--navy) !important;
}

p, li, label, span, div {
    color: var(--text);
}

img {
    border-radius: 24px;
    box-shadow: 0 16px 36px rgba(90, 60, 20, 0.13);
    border: 1px solid var(--line);
}

/* top admin */
.top-lock {
    text-align: right;
    margin-bottom: 10px;
}
.top-lock a {
    color: #111827;
    text-decoration: none;
    font-size: 1rem;
    font-weight: 800;
}

/* landing */
.hero-section,
.clean-section,
.payment-section,
.admin-section {
    background: var(--paper);
    border-radius: 28px;
    padding: 34px;
    box-shadow: 0 14px 32px rgba(90, 60, 20, 0.08);
    border: 1px solid var(--line);
    margin: 28px 0;
}

.hero-title {
    font-size: 2.35rem;
    font-weight: 900;
    line-height: 1.15;
    color: var(--navy);
    margin-bottom: 16px;
}

.hero-text {
    font-size: 1.08rem;
    line-height: 1.75;
    color: #41516a;
    margin-bottom: 22px;
}

.attractions-title,
.how-title {
    font-size: 1.45rem;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 14px;
}

.attractions-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px 12px;
    margin: 18px 0 22px 0;
}

.attraction-pill {
    background: #fff7df;
    border: 1px solid #f0c987;
    border-radius: 999px;
    padding: 10px 14px;
    font-weight: 800;
    color: var(--navy);
}

.how-card {
    background: #fff5df;
    border: 1px solid #f0c987;
    border-left: 8px solid var(--orange);
    border-radius: 22px;
    padding: 24px;
    margin-top: 18px;
}

.how-card p {
    line-height: 1.7;
    margin-bottom: 14px;
}

.quota-line {
    margin: 9px 0;
    line-height: 1.55;
}

.note-box {
    background: #f8fbff;
    border: 1px solid #dbeafe;
    border-radius: 18px;
    padding: 16px 18px;
    margin-top: 16px;
    line-height: 1.6;
}

.cta-wrap {
    text-align: center;
    margin-top: 26px;
}
.cta-button {
    display: inline-block;
    background: var(--orange);
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 900;
    padding: 15px 34px;
    border-radius: 999px;
    box-shadow: 0 10px 20px rgba(90,60,20,0.14);
}
.cta-button:hover {
    background: var(--orange-dark);
    color: #ffffff !important;
}

.section-title {
    font-size: 2rem;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 8px;
}
.section-subtitle {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.55;
}

/* inputs */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stFileUploader label {
    color: var(--navy) !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border: 1px solid #d8c6a4 !important;
    border-radius: 14px !important;
    min-height: 44px !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
input,
textarea {
    color: #1f2937 !important;
    background: #ffffff !important;
}

/* stats */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 18px 0 22px 0;
}
.stat-card {
    background: #fffdf8;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    min-height: 108px;
    box-shadow: 0 6px 18px rgba(90,60,20,0.05);
}
.stat-label {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 10px;
    font-weight: 700;
}
.stat-value {
    color: var(--navy);
    font-size: 2.05rem;
    font-weight: 900;
    line-height: 1;
}

/* clickable cota cards */
.cota-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 18px 0;
}
.cota-card {
    display: block;
    text-decoration: none !important;
    background: #fffdf8;
    border: 2px solid var(--line);
    border-radius: 24px;
    padding: 24px;
    min-height: 245px;
    box-shadow: 0 8px 22px rgba(90,60,20,0.06);
}
.cota-card:hover {
    border-color: var(--orange);
    transform: translateY(-1px);
}
.cota-card.selected {
    background: var(--green-bg);
    border: 3px solid var(--green);
}
.cota-title {
    font-size: 1.35rem;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 8px;
}
.cota-price {
    font-size: 2.25rem;
    font-weight: 950;
    color: #b85f00;
    margin-bottom: 12px;
}
.cota-desc {
    color: #475569;
    line-height: 1.48;
    font-size: 0.98rem;
    margin-bottom: 16px;
}
.cota-note {
    color: var(--muted);
    font-weight: 800;
    font-size: 0.93rem;
}

/* item cards */
.item-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 18px 0;
}
.item-card {
    display: block;
    text-decoration: none !important;
    border-radius: 22px;
    padding: 18px;
    height: 168px;
    background: #fffdf8;
    border: 2px solid var(--line);
    box-shadow: 0 6px 18px rgba(90,60,20,0.05);
}
.item-card.selected {
    background: var(--green-bg);
    border: 3px solid var(--green);
}
.item-title {
    font-size: 1.12rem;
    font-weight: 900;
    color: var(--navy);
    line-height: 1.25;
    margin-bottom: 8px;
}
.item-subtitle {
    font-size: 0.88rem;
    color: var(--muted);
    min-height: 42px;
    line-height: 1.35;
}
.item-vagas {
    margin-top: 12px;
    font-size: 0.9rem;
    color: var(--muted);
    font-weight: 800;
}

/* payment */
.payment-section {
    padding: 34px;
}
.payment-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 18px;
}
.payment-box {
    background: #fffdf8;
    border: 2px dashed #d9be91;
    border-radius: 22px;
    padding: 22px;
}
.payment-box-title {
    font-size: 1.25rem;
    font-weight: 900;
    color: var(--navy);
    margin-bottom: 14px;
}
.payment-box strong {
    color: var(--navy);
}
.pix-key {
    display: inline-block;
    background: var(--navy);
    color: #fff8e8;
    padding: 13px 16px;
    border-radius: 14px;
    font-size: 1.16rem;
    font-weight: 900;
    letter-spacing: 0.3px;
    margin-top: 8px;
}
.pix-copy-text {
    color: var(--navy);
    font-weight: 900;
    margin-bottom: 8px;
}

/* upload */
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

/* buttons */
.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    border-radius: 999px !important;
    font-weight: 900 !important;
    border: none !important;
    background: var(--orange) !important;
    color: #ffffff !important;
    padding: 0.72rem 1.2rem !important;
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
    background: var(--orange-dark) !important;
    color: #ffffff !important;
    border: none !important;
}

.footer-note {
    text-align: center;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 34px;
    line-height: 1.7;
}
.footer-note strong {
    color: var(--navy);
}

@media (max-width: 760px) {
    .hero-title { font-size: 1.8rem; }
    .hero-section, .clean-section, .payment-section, .admin-section { padding: 22px; }
    .attractions-grid, .stats-row, .cota-grid, .item-grid { grid-template-columns: 1fr; }
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

def html(content):
    cleaned = "".join(line.strip() for line in dedent(content).strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def section_header(title, subtitle=None):
    subtitle_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    html(f"""
    <div class="clean-section">
        <div class="section-title">{title}</div>
        {subtitle_html}
    </div>
    """)


def get_item_meta(nome_item):
    mapa = {
        "3 refrigerantes de 2 litros": {
            "emoji": "🥤",
            "titulo": "Refrigerantes",
            "subtitulo": "3 refrigerantes de 2 litros",
        },
        "Arroz doce": {
            "emoji": "🍚",
            "titulo": "Arroz doce",
            "subtitulo": "&nbsp;",
        },
        "Bolo doce": {
            "emoji": "🎂",
            "titulo": "Bolo doce",
            "subtitulo": "&nbsp;",
        },
        "Bolo salgado": {
            "emoji": "🥧",
            "titulo": "Bolo salgado",
            "subtitulo": "&nbsp;",
        },
        "Doces diversos: abóbora, batata doce, cocada etc.": {
            "emoji": "🍬",
            "titulo": "Doces diversos",
            "subtitulo": "abóbora, batata doce, cocada etc.",
        },
        "Milho verde": {
            "emoji": "🌽",
            "titulo": "Milho verde",
            "subtitulo": "&nbsp;",
        },
        "Paçoca": {
            "emoji": "🥜",
            "titulo": "Paçoca",
            "subtitulo": "&nbsp;",
        },
        "Pipoca": {
            "emoji": "🍿",
            "titulo": "Pipoca",
            "subtitulo": "&nbsp;",
        },
        "Sagu": {
            "emoji": "🍮",
            "titulo": "Sagu",
            "subtitulo": "&nbsp;",
        },
    }

    return mapa.get(
        nome_item,
        {"emoji": "🧺", "titulo": nome_item, "subtitulo": "&nbsp;"}
    )


def link_query(**params):
    base = []
    for key, value in params.items():
        if value is not None:
            base.append(f"{key}={quote(str(value))}")
    return "?" + "&".join(base)


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


def buscar_participantes_validos():
    response = (
        supabase
        .table("participantes")
        .select("*")
        .in_("status_pagamento", ["aguardando_conferencia", "confirmado"])
        .execute()
    )
    return response.data or []


def contar_cotas(tipo_cota):
    total = 0
    for participante in buscar_participantes_validos():
        if participante.get("tipo_cota") == tipo_cota:
            total += int(participante.get("qtd_adultos_pagantes") or 1)
    return total


def buscar_itens_disponiveis():
    itens_response = (
        supabase
        .table("itens_levar")
        .select("*")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )

    participantes = buscar_participantes_validos()

    ocupados = {}
    for participante in participantes:
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
    nome_arquivo = (
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
        f"{nome_seguro}_{uuid4()}.{extensao}"
    )

    conteudo = arquivo.getvalue()

    supabase.storage.from_("comprovantes").upload(
        path=nome_arquivo,
        file=conteudo,
        file_options={"content-type": arquivo.type}
    )

    return nome_arquivo


def cadastrar_participante(
    nome,
    email,
    whatsapp,
    tipo_cota,
    valor_cota,
    valor_total,
    item_levar,
    comprovante_url,
    qtd_adultos_pagantes,
    qtd_criancas_ate_10,
    familiares,
):
    dados = {
        "nome": nome.strip(),
        "email": email.strip().lower(),
        "whatsapp": whatsapp.strip(),
        "tipo_cota": tipo_cota,
        "valor_cota": valor_cota,
        "valor_total": valor_total,
        "item_levar": item_levar,
        "qtd_adultos_pagantes": qtd_adultos_pagantes,
        "qtd_criancas_ate_10": qtd_criancas_ate_10,
        "familiares": familiares.strip() if familiares else None,
        "status_pagamento": "aguardando_conferencia",
        "comprovante_url": comprovante_url,
    }

    response = (
        supabase
        .table("participantes")
        .insert(dados)
        .execute()
    )

    return response.data


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
        response = supabase.storage.from_("comprovantes").create_signed_url(
            path=caminho,
            expires_in=3600,
        )
        return response.get("signedURL") or response.get("signedUrl")
    except Exception:
        return None


# =========================
# SESSION STATE / QUERY PARAMS
# =========================

if "tipo_cota" not in st.session_state:
    st.session_state.tipo_cota = None

if "item_levar" not in st.session_state:
    st.session_state.item_levar = None

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False

query_admin = st.query_params.get("admin")
query_cota = st.query_params.get("cota")
query_item = st.query_params.get("item")

if query_cota in ["completa_50", "reduzida_25", "minima_5"]:
    st.session_state.tipo_cota = query_cota
    if query_cota == "completa_50":
        st.session_state.item_levar = None

if query_item:
    st.session_state.item_levar = unquote(query_item)


# =========================
# DADOS PRINCIPAIS
# =========================

config = buscar_configuracao()

limite_50 = int(config["limite_cota_50"])
limite_25 = int(config["limite_cota_25"])
limite_5 = 5

valor_50 = float(config["valor_cota_50"])
valor_25 = float(config["valor_cota_25"])
valor_5 = 5.00

total_50 = contar_cotas("completa_50")
total_25 = contar_cotas("reduzida_25")
total_5 = contar_cotas("minima_5")

vagas_50 = max(limite_50 - total_50, 0)
vagas_25 = max(limite_25 - total_25, 0)
vagas_5 = max(limite_5 - total_5, 0)

itens_disponiveis = buscar_itens_disponiveis()


# =========================
# TOPO DISCRETO + HERO
# =========================

st.markdown('<div class="top-lock"><a href="?admin=1">🔒</a></div>', unsafe_allow_html=True)

banner_path = Path(__file__).parent / "banner_festa_julina.png"

if banner_path.exists():
    try:
        st.image(str(banner_path), use_container_width=True)
    except Exception:
        st.error(
            "O banner foi encontrado, mas não pôde ser carregado como imagem. "
            "Verifique se o arquivo enviado no GitHub é realmente um PNG válido."
        )
else:
    st.error(
        "Banner não encontrado. Confirme se o arquivo banner_festa_julina.png "
        "está na raiz do repositório, junto com app.py."
    )


# =========================
# ADMIN
# =========================

if query_admin == "1":
    html("""
    <div class="admin-section">
        <div class="section-title">Painel administrativo</div>
        <div class="section-subtitle">Acesso restrito à organização.</div>
    </div>
    """)

    if not st.session_state.admin_autenticado:
        col_senha, col_acessar, col_voltar = st.columns([2.2, 0.8, 0.8])
        with col_senha:
            senha = st.text_input("Senha do admin", type="password")
        with col_acessar:
            st.write("")
            st.write("")
            if st.button("Acessar", use_container_width=True):
                senha_admin = st.secrets.get("ADMIN_PASSWORD", "admin123")
                if senha == senha_admin:
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
        with col_voltar:
            st.write("")
            st.write("")
            st.link_button("Voltar", "./", use_container_width=True)
    else:
        participantes = buscar_participantes()

        if not participantes:
            st.info("Ainda não há participantes cadastrados.")
        else:
            df = pd.DataFrame(participantes)
            if "valor_total" not in df.columns:
                df["valor_total"] = df["valor_cota"]

            total_previsto = df["valor_total"].fillna(df["valor_cota"]).sum()
            total_confirmado = df[df["status_pagamento"] == "confirmado"]["valor_total"].fillna(
                df[df["status_pagamento"] == "confirmado"]["valor_cota"]
            ).sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Inscrições", len(df))
            col2.metric("Total previsto", f"R$ {total_previsto:.2f}")
            col3.metric("Total confirmado", f"R$ {total_confirmado:.2f}")

            st.markdown("### Participantes")

            for participante in participantes:
                valor_total_participante = participante.get("valor_total") or participante.get("valor_cota")
                with st.expander(
                    f"{participante['nome']} - R$ {float(valor_total_participante):.2f}"
                ):
                    st.write(f"**E-mail:** {participante['email']}")
                    st.write(f"**WhatsApp:** {participante.get('whatsapp', '')}")
                    st.write(f"**Tipo de cota:** {participante['tipo_cota']}")
                    st.write(f"**Adultos pagantes:** {participante.get('qtd_adultos_pagantes') or 1}")
                    st.write(f"**Crianças até 10 anos:** {participante.get('qtd_criancas_ate_10') or 0}")
                    st.write(f"**Familiares/acompanhantes:** {participante.get('familiares') or '-'}")
                    st.write(f"**Item para levar:** {participante.get('item_levar') or '-'}")
                    st.write(f"**Status:** {participante['status_pagamento']}")

                    comprovante_path = participante.get("comprovante_url")
                    st.write(f"**Arquivo do comprovante:** {comprovante_path or '-'}")

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

        st.link_button("Voltar", "./")

    html("""
    <div class="footer-note">
        Festa Julina da Mary • Organização das inscrições e contribuições<br>
        <strong>Desenvolvimento by Levz</strong>
    </div>
    """)
    st.stop()


# =========================
# LANDING PAGE
# =========================

html("""
<div class="hero-section">
    <div class="hero-title">A Festa Julina da Mary está chegando. Vem participar com a gente!</div>
    <div class="hero-text">
        A festa está sendo preparada para reunir todo mundo em uma noite gostosa, divertida e bem organizada.
        Quem participar já terá acesso às comidas principais, atrações e estrutura preparada para o evento.
    </div>
    <div class="attractions-title">O que já está incluso para quem participar?</div>
    <div class="attractions-grid">
        <div class="attraction-pill">🌭 Cachorro-quente</div>
        <div class="attraction-pill">🥣 Caldinhos</div>
        <div class="attraction-pill">🍡 Bolinho caipira</div>
        <div class="attraction-pill">🍿 Pipoca, paçoca e doces</div>
        <div class="attraction-pill">🎤 Karaoke</div>
        <div class="attraction-pill">📺 Telão interativo</div>
        <div class="attraction-pill">🎱 Bingo</div>
        <div class="attraction-pill">🔥 Fogueira</div>
        <div class="attraction-pill">💋 Barraca do beijo</div>
        <div class="attraction-pill">🎣 Pescaria</div>
        <div class="attraction-pill">💃 Quadrilha</div>
        <div class="attraction-pill">🎊 Decoração temática</div>
    </div>
    <div class="note-box">
        🍻 Bebidas alcoólicas são por conta de cada pessoa, caso queira consumir.<br>
        🎁 Quem quiser também pode levar prendas extras para o bingo.
    </div>
    <div class="how-card">
        <div class="how-title">Como funciona?</div>
        <p>
            Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente.
            Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.
        </p>
        <div class="quota-line">🎟️ <strong>Cota R$50:</strong> esta cota é para quem não tem tempo. Com ela você não precisa levar nenhum prato.</div>
        <div class="quota-line">🧺 <strong>Cota R$25:</strong> com esta cota, você ajuda na organização e leva um prato dentre as opções.</div>
        <div class="quota-line">🤝 <strong>Cota R$5:</strong> cota solidária para quem está apertado. Você ajuda de forma simbólica e leva um prato dentre as opções.</div>
        <p style="margin-top:18px; margin-bottom:0;">
            A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.
        </p>
    </div>
    <div class="cta-wrap">
        <a class="cta-button" href="#inscricao">Quero me inscrever</a>
    </div>
</div>
""")

st.markdown('<div id="inscricao"></div>', unsafe_allow_html=True)

# =========================
# INSCRIÇÃO
# =========================

section_header("Preencha seus dados", "Informe seus dados e, se vier com família, adicione os acompanhantes na mesma inscrição. Crianças até 10 anos não pagam.")

nome = st.text_input("Nome completo")

col_email, col_whatsapp = st.columns(2)
with col_email:
    email = st.text_input("E-mail")
with col_whatsapp:
    whatsapp = st.text_input("WhatsApp")

col_adultos, col_criancas = st.columns(2)
with col_adultos:
    qtd_adultos_pagantes = st.number_input(
        "Adultos pagantes, incluindo você",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )
with col_criancas:
    qtd_criancas_ate_10 = st.number_input(
        "Crianças até 10 anos",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
    )

familiares = st.text_area(
    "Nomes dos familiares/acompanhantes, se houver",
    placeholder="Ex.: João, Maria, Pedro (criança 8 anos)...",
)

section_header("Escolha sua participação")

html(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Cotas R$50 disponíveis</div>
        <div class="stat-value">{vagas_50}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Cotas R$25 + item disponíveis</div>
        <div class="stat-value">{vagas_25}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Cotas R$5 solidárias disponíveis</div>
        <div class="stat-value">{vagas_5}</div>
    </div>
</div>
""")

selected_cota = st.session_state.tipo_cota

cota_cards = []
if vagas_50 > 0:
    cota_cards.append(("completa_50", "🎟️ Cota R$50", "R$50", "Para quem não tem tempo. Você participa e não precisa levar nenhum prato.", vagas_50))
if vagas_25 > 0:
    cota_cards.append(("reduzida_25", "🧺 Cota R$25", "R$25", "Você ajuda na organização e leva um prato dentre as opções disponíveis.", vagas_25))
if vagas_5 > 0:
    cota_cards.append(("minima_5", "🤝 Cota R$5", "R$5", "Cota solidária para quem está apertado. Ajuda simbólica e leva um prato.", vagas_5))

cards_html = '<div class="cota-grid">'
for tipo, titulo, preco, desc, vagas in cota_cards:
    selected_class = " selected" if selected_cota == tipo else ""
    href = link_query(cota=tipo) + "#inscricao"
    cards_html += (
        f'<a class="cota-card{selected_class}" href="{href}">'
        f'<div class="cota-title">{titulo}</div>'
        f'<div class="cota-price">{preco}</div>'
        f'<div class="cota-desc">{desc}</div>'
        f'<div class="cota-note">Vagas disponíveis: {vagas}</div>'
        '</a>'
    )
cards_html += '</div>'
html(cards_html)

if selected_cota in ["reduzida_25", "minima_5"]:
    section_header("Escolha o item que você vai levar", "Selecione uma das opções disponíveis abaixo.")

    item_html = '<div class="item-grid">'
    for item in itens_disponiveis:
        meta = get_item_meta(item["nome"])
        selected_class = " selected" if st.session_state.item_levar == item["nome"] else ""
        href = link_query(cota=selected_cota, item=item["nome"]) + "#inscricao"
        item_html += (
            f'<a class="item-card{selected_class}" href="{href}">'
            f'<div class="item-title">{meta["emoji"]} {meta["titulo"]}</div>'
            f'<div class="item-subtitle">{meta["subtitulo"]}</div>'
            f'<div class="item-vagas">{item["vagas_restantes"]} vaga(s) disponível(is)</div>'
            '</a>'
        )
    item_html += '</div>'
    html(item_html)

if selected_cota:
    if selected_cota == "completa_50":
        valor_cota = valor_50
        tipo_texto = "Cota R$50 - não preciso levar prato"
        item_resumo = "-"
    elif selected_cota == "reduzida_25":
        valor_cota = valor_25
        tipo_texto = "Cota R$25 - vou levar um prato"
        item_resumo = st.session_state.item_levar or "-"
    else:
        valor_cota = valor_5
        tipo_texto = "Cota R$5 - solidária + prato"
        item_resumo = st.session_state.item_levar or "-"

    valor_total = float(valor_cota) * int(qtd_adultos_pagantes)

    html(f"""
    <div class="payment-section">
        <div class="section-title">Resumo e pagamento</div>
        <div class="payment-grid">
            <div class="payment-box">
                <div class="payment-box-title">Resumo da inscrição</div>
                <strong>Participação escolhida:</strong> {tipo_texto}<br>
                <strong>Adultos pagantes:</strong> {int(qtd_adultos_pagantes)}<br>
                <strong>Crianças até 10 anos:</strong> {int(qtd_criancas_ate_10)}<br>
                <strong>Item para levar:</strong> {item_resumo}<br>
                <strong>Valor total do Pix:</strong> R$ {valor_total:.2f}
            </div>
            <div class="payment-box">
                <div class="payment-box-title">Dados do Recebedor</div>
                <div class="pix-copy-text">Copie o código Pix abaixo:</div>
                <div class="pix-key">{config["chave_pix"]}</div>
            </div>
            <div class="payment-box">
                <div class="payment-box-title">Anexo do Comprovante</div>
            </div>
        </div>
    </div>
    """)

    comprovante = st.file_uploader(
        "Anexe o comprovante do Pix",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    if st.button("Confirmar minha inscrição", key="confirmar_inscricao", use_container_width=True):
        if not nome or not email or not whatsapp:
            st.error("Preencha nome, e-mail e WhatsApp antes de confirmar.")
        elif selected_cota in ["reduzida_25", "minima_5"] and not st.session_state.item_levar:
            st.error("Escolha o item que você vai levar.")
        elif not comprovante:
            st.error("Anexe o comprovante do Pix.")
        elif selected_cota == "completa_50" and int(qtd_adultos_pagantes) > vagas_50:
            st.error("Não há vagas suficientes nesta cota para a quantidade de adultos pagantes informada.")
        elif selected_cota == "reduzida_25" and int(qtd_adultos_pagantes) > vagas_25:
            st.error("Não há vagas suficientes nesta cota para a quantidade de adultos pagantes informada.")
        elif selected_cota == "minima_5" and int(qtd_adultos_pagantes) > vagas_5:
            st.error("Não há vagas suficientes nesta cota para a quantidade de adultos pagantes informada.")
        else:
            try:
                comprovante_url = salvar_comprovante(comprovante, email)

                cadastrar_participante(
                    nome=nome,
                    email=email,
                    whatsapp=whatsapp,
                    tipo_cota=selected_cota,
                    valor_cota=valor_cota,
                    valor_total=valor_total,
                    item_levar=st.session_state.item_levar if selected_cota in ["reduzida_25", "minima_5"] else None,
                    comprovante_url=comprovante_url,
                    qtd_adultos_pagantes=int(qtd_adultos_pagantes),
                    qtd_criancas_ate_10=int(qtd_criancas_ate_10),
                    familiares=familiares,
                )

                st.session_state.tipo_cota = None
                st.session_state.item_levar = None

                st.success(
                    "Inscrição enviada com sucesso! "
                    "O pagamento ficará aguardando conferência da organização."
                )

            except Exception as erro:
                st.error("Não foi possível salvar sua inscrição.")
                st.exception(erro)


# =========================
# FOOTER
# =========================

html("""
<div class="footer-note">
    Festa Julina da Mary • Organização das inscrições e contribuições<br>
    <strong>Desenvolvimento by Levz</strong>
</div>
""")
