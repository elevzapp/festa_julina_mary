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
.stApp {
    background: #fff4df;
    color: #19324f;
}

.main .block-container {
    max-width: 980px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: #12355b !important;
}

p, li, label, span, div {
    color: #334155;
}

img {
    border-radius: 24px;
    box-shadow: 0 14px 34px rgba(90, 60, 20, 0.13);
    border: 1px solid #ead9bc;
}

.intro-card,
.section-card,
.ready-card {
    background: #ffffff;
    border-radius: 26px;
    padding: 30px;
    box-shadow: 0 12px 30px rgba(90, 60, 20, 0.08);
    border: 1px solid #ead9bc;
    margin: 24px 0;
}

.intro-title {
    font-size: 2.1rem;
    font-weight: 850;
    color: #12355b;
    line-height: 1.2;
    margin-bottom: 16px;
}

.intro-text {
    font-size: 1.08rem;
    line-height: 1.75;
    color: #475569;
    margin-bottom: 20px;
}

.attractions-list {
    background: #fffaf0;
    border: 1px solid #ead9bc;
    border-radius: 18px;
    padding: 18px 20px;
    margin: 18px 0;
    line-height: 1.75;
}

.attractions-list strong {
    color: #12355b;
}

.how-card {
    background: #fff5df;
    border: 1px solid #f0c987;
    border-left: 8px solid #df7f00;
    border-radius: 20px;
    padding: 22px;
    margin: 20px 0;
}

.how-card-title {
    font-size: 1.35rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 12px;
}

.section-title {
    font-size: 1.75rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #64748b;
    font-size: 1rem;
}

.ready-card {
    text-align: center;
    padding: 26px;
}

.stat-card {
    background: #fffdf8;
    border: 1px solid #ead9bc;
    border-radius: 20px;
    padding: 18px;
    min-height: 108px;
    box-shadow: 0 6px 18px rgba(90, 60, 20, 0.05);
    margin-bottom: 16px;
}

.stat-label {
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 10px;
}

.stat-value {
    color: #12355b;
    font-size: 2.1rem;
    font-weight: 850;
    line-height: 1;
}

.option-link {
    text-decoration: none !important;
}

.option-card,
.option-card-selected {
    border-radius: 24px;
    padding: 24px;
    min-height: 260px;
    box-shadow: 0 8px 22px rgba(90, 60, 20, 0.06);
    margin-bottom: 12px;
    cursor: pointer;
    transition: 0.18s ease;
}

.option-card:hover {
    transform: translateY(-2px);
    border-color: #df7f00;
}

.option-card {
    background: #fffdf8;
    border: 2px solid #e8d3ae;
}

.option-card-selected {
    background: #ecfbd3;
    border: 3px solid #65a30d;
}

.option-title {
    font-size: 1.55rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 8px;
}

.option-price {
    font-size: 2.25rem;
    font-weight: 900;
    color: #b85f00;
    margin-bottom: 12px;
}

.option-text {
    font-size: 1rem;
    line-height: 1.55;
    color: #475569;
    margin-bottom: 18px;
}

.option-note {
    color: #64748b;
    font-size: 0.95rem;
    font-weight: 650;
}

.item-card,
.item-card-selected {
    border-radius: 22px;
    padding: 18px;
    height: 168px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 6px 18px rgba(90, 60, 20, 0.05);
    margin-bottom: 10px;
    cursor: pointer;
    transition: 0.18s ease;
}

.item-card:hover {
    transform: translateY(-2px);
    border-color: #df7f00;
}

.item-card {
    background: #fffdf8;
    border: 2px solid #e8d3ae;
}

.item-card-selected {
    background: #ecfbd3;
    border: 3px solid #65a30d;
}

.item-title {
    font-size: 1.18rem;
    font-weight: 850;
    color: #12355b;
    line-height: 1.25;
}

.item-subtitle {
    font-size: 0.9rem;
    color: #64748b;
    margin-top: 8px;
    line-height: 1.35;
    min-height: 38px;
}

.item-vagas {
    font-size: 0.92rem;
    color: #64748b;
    font-weight: 650;
}

.payment-shell {
    background: #ffffff;
    border-radius: 26px;
    padding: 30px;
    box-shadow: 0 12px 30px rgba(90, 60, 20, 0.08);
    border: 1px solid #ead9bc;
    margin: 24px 0 12px 0;
}

.payment-title {
    font-size: 1.75rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 16px;
}

.payment-box {
    background: #fffdf8;
    border: 2px dashed #e8d3ae;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
}

.payment-box-title {
    color: #12355b;
    font-weight: 850;
    font-size: 1.15rem;
    margin-bottom: 12px;
}

.payment-box strong {
    color: #12355b;
}

.pix-instruction {
    color: #64748b;
    font-size: 0.98rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.pix-key {
    display: inline-block;
    background: #12355b;
    color: #fff8e8;
    padding: 13px 16px;
    border-radius: 14px;
    font-size: 1.16rem;
    font-weight: 850;
    letter-spacing: 0.3px;
    margin-top: 6px;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 0.95rem;
    margin-top: 34px;
    line-height: 1.7;
}

.footer-note strong {
    color: #12355b;
}

.stTextInput label,
.stFileUploader label {
    color: #12355b !important;
    font-weight: 750 !important;
    font-size: 0.95rem !important;
}

div[data-baseweb="input"] > div {
    background: #ffffff !important;
    border: 1px solid #d8c6a4 !important;
    border-radius: 14px !important;
    min-height: 44px !important;
}

div[data-baseweb="input"] input {
    color: #1f2937 !important;
    background: #ffffff !important;
    min-height: 42px !important;
}

input {
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
    background: #df7f00 !important;
    color: #ffffff !important;
    font-weight: 850 !important;
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
    font-weight: 850 !important;
    border: none !important;
    background: #df7f00 !important;
    color: #ffffff !important;
    padding: 0.72rem 1.2rem !important;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    color: #ffffff !important;
    font-weight: 850 !important;
}

.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover {
    background: #bf6900 !important;
    color: #ffffff !important;
    border: none !important;
}

.admin-lock button {
    background: transparent !important;
    color: #111827 !important;
    border: none !important;
    padding: 0.1rem !important;
    box-shadow: none !important;
    font-size: 1.2rem !important;
}

.admin-lock button p {
    color: #111827 !important;
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
    <div class="section-card">
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


def escolher_cota_link(tipo):
    return f"?inscrever=1&cota={tipo}#inscricao"


def escolher_item_link(nome_item):
    return f"?inscrever=1&cota={st.session_state.tipo_cota}&item={quote(nome_item)}#itens"


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


def contar_participantes_com_item():
    response = (
        supabase
        .table("participantes")
        .select("id", count="exact")
        .in_("tipo_cota", ["reduzida_25", "minima_10"])
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
        .in_("tipo_cota", ["reduzida_25", "minima_10"])
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
    item_levar,
    comprovante_url,
):
    dados = {
        "nome": nome.strip(),
        "email": email.strip().lower(),
        "whatsapp": whatsapp.strip(),
        "tipo_cota": tipo_cota,
        "valor_cota": valor_cota,
        "item_levar": item_levar,
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
# SESSION STATE
# =========================

if "mostrar_inscricao" not in st.session_state:
    st.session_state.mostrar_inscricao = False

if "tipo_cota" not in st.session_state:
    st.session_state.tipo_cota = None

if "item_levar" not in st.session_state:
    st.session_state.item_levar = None

if "modo_admin" not in st.session_state:
    st.session_state.modo_admin = False

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False

if st.query_params.get("inscrever") == "1":
    st.session_state.mostrar_inscricao = True

query_cota = st.query_params.get("cota")
if query_cota in ["completa_50", "reduzida_25", "minima_10"]:
    st.session_state.tipo_cota = query_cota
    if query_cota == "completa_50":
        st.session_state.item_levar = None

query_item = st.query_params.get("item")
if query_item:
    st.session_state.item_levar = unquote(query_item)


def escolher_cota(tipo):
    st.session_state.tipo_cota = tipo

    if tipo == "completa_50":
        st.session_state.item_levar = None


def escolher_item(nome_item):
    st.session_state.item_levar = nome_item


# =========================
# DADOS PRINCIPAIS
# =========================

config = buscar_configuracao()

limite_50 = int(config["limite_cota_50"])
limite_itens = int(config["limite_cota_25"])
valor_50 = float(config["valor_cota_50"])
valor_25 = float(config["valor_cota_25"])
valor_10 = 10.00

total_50 = contar_participantes_por_cota("completa_50")
total_com_item = contar_participantes_com_item()

vagas_50 = max(limite_50 - total_50, 0)
vagas_com_item = max(limite_itens - total_com_item, 0)

itens_disponiveis = buscar_itens_disponiveis()


# =========================
# ADMIN DISCRETO
# =========================

col_admin_1, col_admin_2 = st.columns([15, 1])
with col_admin_2:
    st.markdown('<div class="admin-lock">', unsafe_allow_html=True)
    if st.button("🔒", key="btn_admin_lock", help="Área administrativa"):
        st.session_state.modo_admin = True
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# HERO COM IMAGEM
# =========================

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

if st.session_state.modo_admin:
    section_header("Painel administrativo", "Acesso restrito à organização.")

    col_senha, col_acessar, col_voltar = st.columns([3, 1, 1])

    with col_senha:
        senha = st.text_input("Senha do admin", type="password")

    with col_acessar:
        st.write("")
        if st.button("Acessar", key="btn_acessar_admin", use_container_width=True):
            senha_admin = st.secrets.get("ADMIN_PASSWORD", "admin123")
            if senha == senha_admin:
                st.session_state.admin_autenticado = True
                st.rerun()
            else:
                st.session_state.admin_autenticado = False
                st.error("Senha incorreta.")

    with col_voltar:
        st.write("")
        if st.button("Voltar", key="btn_voltar_admin", use_container_width=True):
            st.session_state.modo_admin = False
            st.session_state.admin_autenticado = False
            st.rerun()

    if not st.session_state.admin_autenticado:
        st.warning("Digite a senha para acessar o painel.")
    else:
        participantes = buscar_participantes()

        if not participantes:
            st.info("Ainda não há participantes cadastrados.")
        else:
            df = pd.DataFrame(participantes)

            total_previsto = df["valor_cota"].sum()
            total_confirmado = df[df["status_pagamento"] == "confirmado"]["valor_cota"].sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Participantes", len(df))
            col2.metric("Total previsto", f"R$ {total_previsto:.2f}")
            col3.metric("Total confirmado", f"R$ {total_confirmado:.2f}")

            st.markdown("### Participantes")

            for participante in participantes:
                with st.expander(
                    f"{participante['nome']} - R$ {float(participante['valor_cota']):.2f}"
                ):
                    st.write(f"**E-mail:** {participante['email']}")
                    st.write(f"**WhatsApp:** {participante.get('whatsapp', '')}")
                    st.write(f"**Tipo de cota:** {participante['tipo_cota']}")
                    st.write(f"**Item para levar:** {participante.get('item_levar') or '-'}")
                    st.write(f"**Status:** {participante['status_pagamento']}")

                    comprovante_path = participante.get("comprovante_url")
                    st.write(f"**Arquivo do comprovante:** {comprovante_path or '-'}")

                    link_comprovante = gerar_link_comprovante(comprovante_path)

                    if link_comprovante:
                        st.link_button("Abrir comprovante", link_comprovante)

                    status_opcoes = [
                        "aguardando_conferencia",
                        "confirmado",
                        "recusado",
                    ]

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

st.markdown(
    '<div class="intro-card">'
    '<div class="intro-title">A Festa Julina da Mary está chegando. Vem participar com a gente!</div>'
    '<div class="intro-text">'
    'Este ano a festa está sendo preparada para reunir todo mundo em uma noite gostosa, divertida e bem organizada. '
    'Teremos comidas típicas, bolinho caipira, cachorro-quente, caldinhos, vinho quente, quentão, doces, bolos, pipoca, paçoca, milho verde, sagu, arroz doce e refrigerantes. '
    'Além disso, a programação contará com telão interativo, karaokê, bingo, fogueira, barraca do beijo, pescaria, quadrilha, decoração temática e muito mais.'
    '</div>'
    '<div class="how-card">'
    '<div class="how-card-title">Como funciona?</div>'
    'Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente. '
    'Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.<br><br>'
    '🎟️ <strong>Cota R$50:</strong> você participa e não precisa levar nada.<br>'
    '🧺 <strong>Cota R$25:</strong> você participa e também escolhe um item para levar.<br>'
    '🤝 <strong>Cota mínima R$10:</strong> opção para quem não consegue colaborar com um valor maior, mas ainda precisa escolher um item para levar.<br><br>'
    'A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

if not st.session_state.mostrar_inscricao:
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("Quero me inscrever", key="btn_inscrever", use_container_width=True):
            st.session_state.mostrar_inscricao = True
            st.rerun()


# =========================
# INSCRIÇÃO
# =========================

if st.session_state.mostrar_inscricao:
    st.markdown('<div id="inscricao"></div>', unsafe_allow_html=True)
    section_header("1. Preencha seus dados")

    nome = st.text_input("Nome completo")

    col_email, col_whatsapp = st.columns(2)

    with col_email:
        email = st.text_input("E-mail")

    with col_whatsapp:
        whatsapp = st.text_input("WhatsApp")

    section_header("2. Escolha sua participação")

    col_stat1, col_stat2 = st.columns(2)

    with col_stat1:
        html(f"""
        <div class="stat-card">
            <div class="stat-label">Cotas R$50 disponíveis</div>
            <div class="stat-value">{vagas_50}</div>
        </div>
        """)

    with col_stat2:
        html(f"""
        <div class="stat-card">
            <div class="stat-label">Cotas com item disponíveis</div>
            <div class="stat-value">{vagas_com_item}</div>
        </div>
        """)

    col_cota_50, col_cota_25, col_cota_10 = st.columns(3)

    with col_cota_50:
        classe = (
            "option-card-selected"
            if st.session_state.tipo_cota == "completa_50"
            else "option-card"
        )

        if vagas_50 > 0:
            html(f"""
            <a class="option-link" href="{escolher_cota_link('completa_50')}">
                <div class="{classe}">
                    <div class="option-title">🎟️ Cota completa</div>
                    <div class="option-price">R$50</div>
                    <div class="option-text">Você participa da festa e não precisa levar nenhum item.</div>
                    <div class="option-note">Vagas disponíveis: {vagas_50}</div>
                </div>
            </a>
            """)
        else:
            html(f"""
            <div class="{classe}">
                <div class="option-title">🎟️ Cota completa</div>
                <div class="option-price">R$50</div>
                <div class="option-text">Cota esgotada.</div>
                <div class="option-note">Vagas disponíveis: 0</div>
            </div>
            """)

    with col_cota_25:
        classe = (
            "option-card-selected"
            if st.session_state.tipo_cota == "reduzida_25"
            else "option-card"
        )

        if vagas_com_item > 0 and len(itens_disponiveis) > 0:
            html(f"""
            <a class="option-link" href="{escolher_cota_link('reduzida_25')}">
                <div class="{classe}">
                    <div class="option-title">🧺 Cota com item</div>
                    <div class="option-price">R$25</div>
                    <div class="option-text">Você participa da festa e escolhe um item para levar no dia.</div>
                    <div class="option-note">Vagas disponíveis: {vagas_com_item}</div>
                </div>
            </a>
            """)
        else:
            html(f"""
            <div class="{classe}">
                <div class="option-title">🧺 Cota com item</div>
                <div class="option-price">R$25</div>
                <div class="option-text">Cota esgotada.</div>
                <div class="option-note">Vagas disponíveis: 0</div>
            </div>
            """)

    with col_cota_10:
        classe = (
            "option-card-selected"
            if st.session_state.tipo_cota == "minima_10"
            else "option-card"
        )

        if vagas_com_item > 0 and len(itens_disponiveis) > 0:
            html(f"""
            <a class="option-link" href="{escolher_cota_link('minima_10')}">
                <div class="{classe}">
                    <div class="option-title">🤝 Cota mínima</div>
                    <div class="option-price">R$10</div>
                    <div class="option-text">Para quem não consegue colaborar com mais. Precisa escolher um item para levar.</div>
                    <div class="option-note">Vagas disponíveis: {vagas_com_item}</div>
                </div>
            </a>
            """)
        else:
            html(f"""
            <div class="{classe}">
                <div class="option-title">🤝 Cota mínima</div>
                <div class="option-price">R$10</div>
                <div class="option-text">Cota esgotada.</div>
                <div class="option-note">Vagas disponíveis: 0</div>
            </div>
            """)

    if st.session_state.tipo_cota in ["reduzida_25", "minima_10"]:
        st.markdown('<div id="itens"></div>', unsafe_allow_html=True)
        section_header(
            "3. Escolha o item que você vai levar",
            "Selecione uma das opções disponíveis abaixo."
        )

        itens_por_linha = 3

        for i in range(0, len(itens_disponiveis), itens_por_linha):
            cols = st.columns(itens_por_linha)
            grupo = itens_disponiveis[i:i + itens_por_linha]

            for col, item in zip(cols, grupo):
                meta = get_item_meta(item["nome"])

                with col:
                    selecionado = st.session_state.item_levar == item["nome"]
                    classe = "item-card-selected" if selecionado else "item-card"

                    html(f"""
                    <a class="option-link" href="{escolher_item_link(item['nome'])}">
                        <div class="{classe}">
                            <div>
                                <div class="item-title">{meta['emoji']} {meta['titulo']}</div>
                                <div class="item-subtitle">{meta['subtitulo']}</div>
                            </div>
                            <div class="item-vagas">{item["vagas_restantes"]} vaga(s) disponível(is)</div>
                        </div>
                    </a>
                    """)

    if st.session_state.tipo_cota:
        if st.session_state.tipo_cota == "completa_50":
            valor_cota = valor_50
            tipo_texto = "Cota R$50 - Não preciso levar nada"
        elif st.session_state.tipo_cota == "reduzida_25":
            valor_cota = valor_25
            tipo_texto = "Cota R$25 - Vou levar um item"
        else:
            valor_cota = valor_10
            tipo_texto = "Cota mínima R$10 - Vou levar um item"

        item_resumo = st.session_state.item_levar or "-"

        html('<div class="payment-shell"><div class="payment-title">4. Resumo e pagamento</div>')

        html(f"""
        <div class="payment-box">
            <div class="payment-box-title">Resumo da inscrição</div>
            <strong>Participação escolhida:</strong> {tipo_texto}<br>
            <strong>Item para levar:</strong> {item_resumo}<br>
            <strong>Valor do Pix:</strong> R$ {valor_cota:.2f}
        </div>
        """)

        html(f"""
        <div class="payment-box">
            <div class="payment-box-title">Dados do Recebedor</div>
            <div class="pix-instruction">Copie o código Pix abaixo:</div>
            <div class="pix-key">{config["chave_pix"]}</div>
        </div>
        """)

        html("""
        <div class="payment-box">
            <div class="payment-box-title">Anexo do Comprovante</div>
        """)

        comprovante = st.file_uploader(
            "Anexe o comprovante do Pix",
            type=["png", "jpg", "jpeg", "pdf"],
            label_visibility="collapsed",
        )

        if st.button(
            "Confirmar minha inscrição",
            key="confirmar_inscricao",
            use_container_width=True,
        ):
            if not nome or not email or not whatsapp:
                st.error("Preencha nome, e-mail e WhatsApp antes de confirmar.")
            elif (
                st.session_state.tipo_cota in ["reduzida_25", "minima_10"]
                and not st.session_state.item_levar
            ):
                st.error("Escolha o item que você vai levar.")
            elif not comprovante:
                st.error("Anexe o comprovante do Pix.")
            else:
                try:
                    comprovante_url = salvar_comprovante(comprovante, email)

                    cadastrar_participante(
                        nome=nome,
                        email=email,
                        whatsapp=whatsapp,
                        tipo_cota=st.session_state.tipo_cota,
                        valor_cota=valor_cota,
                        item_levar=st.session_state.item_levar,
                        comprovante_url=comprovante_url,
                    )

                    st.session_state.tipo_cota = None
                    st.session_state.item_levar = None
                    st.session_state.mostrar_inscricao = False

                    st.success(
                        "Inscrição enviada com sucesso! "
                        "O pagamento ficará aguardando conferência da organização."
                    )
                    st.rerun()

                except Exception as erro:
                    st.error("Não foi possível salvar sua inscrição.")
                    st.exception(erro)

        html('</div></div>')


# =========================
# FOOTER
# =========================

html("""
<div class="footer-note">
    Festa Julina da Mary • Organização das inscrições e contribuições<br>
    <strong>Desenvolvimento by Levz</strong>
</div>
""")
