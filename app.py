from datetime import datetime
from pathlib import Path
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
        background: #f9f2e6;
        color: #1f2937;
    }

    .main .block-container {
        max-width: 980px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #12355b;
    }

    p, li, label, span, div {
        color: #334155;
    }

    /* ===== Hero / intro ===== */
    .intro-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(90, 60, 20, 0.08);
        border: 1px solid #ead9bc;
        margin-top: 24px;
        margin-bottom: 24px;
    }

    .intro-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #12355b;
        margin-bottom: 12px;
        line-height: 1.2;
    }

    .intro-text {
        font-size: 1.15rem;
        line-height: 1.7;
        color: #475569;
        margin-bottom: 18px;
    }

    .how-card {
        background: #fff5df;
        border: 1px solid #f0c987;
        border-left: 8px solid #dd8a07;
        border-radius: 18px;
        padding: 20px;
        margin-top: 16px;
        margin-bottom: 16px;
        color: #334155;
    }

    .how-card h3 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #12355b;
    }

    .notice {
        background: linear-gradient(90deg, #12355b 0%, #1e4d80 100%);
        color: #fffaf0;
        padding: 16px 20px;
        border-radius: 16px;
        font-weight: 700;
        margin-top: 18px;
        text-align: center;
    }

    /* ===== Section header ===== */
    .section-header {
        background: #ffffff;
        border: 1px solid #ead9bc;
        border-radius: 22px;
        padding: 22px 24px;
        margin-top: 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px rgba(90, 60, 20, 0.06);
    }

    .section-header h3 {
        margin: 0;
        color: #12355b;
        font-size: 1.9rem;
        line-height: 1.2;
    }

    .section-subtitle {
        margin-top: 8px;
        color: #64748b;
        font-size: 1rem;
    }

    /* ===== Availability stat cards ===== */
    .stat-card {
        background: #fffdf8;
        border: 1px solid #ead9bc;
        border-radius: 20px;
        padding: 18px;
        min-height: 120px;
        box-shadow: 0 6px 18px rgba(90, 60, 20, 0.05);
    }

    .stat-label {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }

    .stat-value {
        color: #12355b;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
    }

    /* ===== Cota cards ===== */
    .option-card,
    .option-card-selected {
        border-radius: 22px;
        padding: 24px;
        min-height: 220px;
        box-shadow: 0 8px 22px rgba(90, 60, 20, 0.06);
    }

    .option-card {
        background: #fffdf8;
        border: 2px solid #e8d3ae;
    }

    .option-card-selected {
        background: #fff6e4;
        border: 3px solid #dd8a07;
    }

    .option-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #12355b;
        margin-bottom: 6px;
    }

    .option-price {
        font-size: 2.3rem;
        font-weight: 900;
        color: #b86800;
        margin-bottom: 12px;
    }

    .option-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #475569;
        margin-bottom: 18px;
    }

    .option-note {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* ===== Item cards ===== */
    .item-card,
    .item-card-selected {
        border-radius: 20px;
        padding: 18px;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 18px rgba(90, 60, 20, 0.05);
        margin-bottom: 10px;
    }

    .item-card {
        background: #fffdf8;
        border: 2px solid #e8d3ae;
    }

    .item-card-selected {
        background: #eef8d8;
        border: 3px solid #65a30d;
    }

    .item-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #12355b;
        line-height: 1.3;
    }

    .item-subtitle {
        font-size: 0.92rem;
        color: #64748b;
        margin-top: 6px;
        line-height: 1.35;
        min-height: 38px;
    }

    .item-vagas {
        font-size: 0.92rem;
        color: #64748b;
        font-weight: 600;
    }

    /* ===== Summary / Pix ===== */
    .summary-box {
        background: #fff7df;
        border: 1px solid #f0c987;
        border-radius: 20px;
        padding: 20px;
        margin-top: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(90, 60, 20, 0.04);
    }

    .summary-box strong {
        color: #12355b;
    }

    .pix-box {
        background: linear-gradient(180deg, #12355b 0%, #1f4d7c 100%);
        border: 2px dashed #f4c14f;
        color: #fffdf8;
        border-radius: 24px;
        padding: 28px;
        margin-top: 18px;
        margin-bottom: 22px;
        box-shadow: 0 10px 26px rgba(18, 53, 91, 0.20);
    }

    .pix-box h3 {
        color: #fffdf8;
        margin-top: 0;
        margin-bottom: 14px;
        font-size: 1.9rem;
    }

    .pix-box p,
    .pix-box strong {
        color: #fffdf8;
        font-size: 1.05rem;
    }

    .pix-key {
        display: inline-block;
        margin-top: 10px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        color: #ffffff;
        padding: 14px 16px;
        border-radius: 14px;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    .payment-note {
        font-size: 0.95rem;
        color: #dbeafe !important;
        margin-top: 12px;
    }

    /* ===== Footer ===== */
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

    /* ===== Banner image ===== */
    img {
        border-radius: 22px;
        box-shadow: 0 14px 34px rgba(90, 60, 20, 0.12);
        border: 1px solid #ead9bc;
    }

    /* ===== Streamlit widgets ===== */
    div[data-baseweb="input"] > div {
        background: #ffffff !important;
        border: 1px solid #d8c6a4 !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="input"] input {
        color: #1f2937 !important;
        background: #ffffff !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput label,
    .stFileUploader label {
        color: #12355b !important;
        font-weight: 700 !important;
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;
        border: 2px dashed #d8c6a4 !important;
        border-radius: 16px !important;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: #475569 !important;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: none;
        background: #dd8200;
        color: #ffffff;
        padding: 0.72rem 1.2rem;
    }

    .stButton > button:hover {
        background: #c36f00;
        color: #ffffff;
        border: none;
    }

    button[kind="secondary"] {
        background: #ffffff !important;
        color: #dd8200 !important;
        border: 1px solid #dd8200 !important;
    }

    div[data-testid="stTabs"] button {
        font-weight: 700;
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

def section_header(title, subtitle=None):
    html = f"""
<div class="section-header">
    <h3>{title}</h3>
    {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


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
            "subtitulo": "",
        },
        "Bolo doce": {
            "emoji": "🎂",
            "titulo": "Bolo doce",
            "subtitulo": "",
        },
        "Bolo salgado": {
            "emoji": "🥧",
            "titulo": "Bolo salgado",
            "subtitulo": "",
        },
        "Doces diversos: abóbora, batata doce, cocada etc.": {
            "emoji": "🍬",
            "titulo": "Doces diversos",
            "subtitulo": "abóbora, batata doce, cocada etc.",
        },
        "Milho verde": {
            "emoji": "🌽",
            "titulo": "Milho verde",
            "subtitulo": "",
        },
        "Paçoca": {
            "emoji": "🥜",
            "titulo": "Paçoca",
            "subtitulo": "",
        },
        "Pipoca": {
            "emoji": "🍿",
            "titulo": "Pipoca",
            "subtitulo": "",
        },
        "Sagu": {
            "emoji": "🍮",
            "titulo": "Sagu",
            "subtitulo": "",
        },
    }

    return mapa.get(
        nome_item,
        {"emoji": "🧺", "titulo": nome_item, "subtitulo": ""}
    )


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
        .eq("tipo_cota", "reduzida_25")
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
limite_25 = int(config["limite_cota_25"])
valor_50 = float(config["valor_cota_50"])
valor_25 = float(config["valor_cota_25"])

total_50 = contar_participantes_por_cota("completa_50")
total_25 = contar_participantes_por_cota("reduzida_25")

vagas_50 = max(limite_50 - total_50, 0)
vagas_25 = max(limite_25 - total_25, 0)

itens_disponiveis = buscar_itens_disponiveis()


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
# INTRODUÇÃO
# =========================

st.markdown(
    """
<div class="intro-card">
    <div class="intro-title">Que bom termos sua participação esse ano!</div>
    <div class="intro-text">
        Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente.
        Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.
    </div>

    <div class="how-card">
        <h3>Como funciona?</h3>
        🎟️ <strong>Cota R$50:</strong> você participa e não precisa levar nada.<br>
        🧺 <strong>Cota R$25:</strong> você participa e também escolhe um item para levar.<br><br>
        A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.
    </div>

    <div class="notice">
        Garanta sua inscrição. As vagas são limitadas!
    </div>
</div>
""",
    unsafe_allow_html=True,
)


col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if st.button("Quero me inscrever", use_container_width=True):
        st.session_state.mostrar_inscricao = True


aba_publica, aba_admin = st.tabs(["🎉 Inscrição", "🔐 Admin"])


# =========================
# ABA INSCRIÇÃO
# =========================

with aba_publica:
    if not st.session_state.mostrar_inscricao:
        section_header(
            "Pronto para participar?",
            "Clique no botão Quero me inscrever acima para abrir o formulário."
        )
    else:
        section_header("1. Seus dados")

        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")

        section_header("2. Escolha sua participação")

        col_stat1, col_stat2 = st.columns(2)

        with col_stat1:
            st.markdown(
                f"""
<div class="stat-card">
    <div class="stat-label">Cotas R$50 disponíveis</div>
    <div class="stat-value">{vagas_50}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with col_stat2:
            st.markdown(
                f"""
<div class="stat-card">
    <div class="stat-label">Cotas R$25 + item disponíveis</div>
    <div class="stat-value">{vagas_25}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        col_cota_50, col_cota_25 = st.columns(2)

        with col_cota_50:
            classe = (
                "option-card-selected"
                if st.session_state.tipo_cota == "completa_50"
                else "option-card"
            )

            st.markdown(
                f"""
<div class="{classe}">
    <div class="option-title">🎟️ Cota completa</div>
    <div class="option-price">R$50</div>
    <div class="option-text">
        Você participa da festa e não precisa levar nenhum item.
    </div>
    <div class="option-note">Vagas disponíveis: {vagas_50}</div>
</div>
""",
                unsafe_allow_html=True,
            )

            if vagas_50 > 0:
                if st.button("Escolher R$50", key="btn_r50", use_container_width=True):
                    escolher_cota("completa_50")
                    st.rerun()
            else:
                st.warning("Cota esgotada.")

        with col_cota_25:
            classe = (
                "option-card-selected"
                if st.session_state.tipo_cota == "reduzida_25"
                else "option-card"
            )

            st.markdown(
                f"""
<div class="{classe}">
    <div class="option-title">🧺 Cota com item</div>
    <div class="option-price">R$25</div>
    <div class="option-text">
        Você participa da festa e escolhe um item para levar no dia.
    </div>
    <div class="option-note">Vagas disponíveis: {vagas_25}</div>
</div>
""",
                unsafe_allow_html=True,
            )

            if vagas_25 > 0 and len(itens_disponiveis) > 0:
                if st.button("Escolher R$25", key="btn_r25", use_container_width=True):
                    escolher_cota("reduzida_25")
                    st.rerun()
            else:
                st.warning("Cota esgotada.")

        if st.session_state.tipo_cota == "reduzida_25":
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

                        st.markdown(
                            f"""
<div class="{classe}">
    <div>
        <div class="item-title">{meta['emoji']} {meta['titulo']}</div>
        <div class="item-subtitle">{meta['subtitulo'] or '&nbsp;'}</div>
    </div>
    <div class="item-vagas">{item["vagas_restantes"]} vaga(s) disponível(is)</div>
</div>
""",
                            unsafe_allow_html=True,
                        )

                        label_botao = "Selecionado" if selecionado else "Selecionar"

                        if st.button(
                            label_botao,
                            key=f"item_{item['nome']}",
                            use_container_width=True,
                        ):
                            escolher_item(item["nome"])
                            st.rerun()

        if st.session_state.tipo_cota:
            valor_cota = (
                valor_50
                if st.session_state.tipo_cota == "completa_50"
                else valor_25
            )

            tipo_texto = (
                "Cota R$50 - Não preciso levar nada"
                if st.session_state.tipo_cota == "completa_50"
                else "Cota R$25 - Vou levar um item"
            )

            section_header("4. Resumo e pagamento")

            item_resumo = st.session_state.item_levar or "-"

            st.markdown(
                f"""
<div class="summary-box">
    <strong>Participação escolhida:</strong> {tipo_texto}<br>
    <strong>Item para levar:</strong> {item_resumo}<br>
    <strong>Valor do Pix:</strong> R$ {valor_cota:.2f}
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
<div class="pix-box">
    <h3>Dados para Pix</h3>
    <p><strong>Recebedor:</strong> {config['nome_recebedor_pix']}</p>
    <p><strong>Chave Pix:</strong></p>
    <div class="pix-key">{config["chave_pix"]}</div>
    <div class="payment-note">
        Depois de realizar o pagamento, anexe o comprovante logo abaixo para concluir sua inscrição.
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            comprovante = st.file_uploader(
                "Anexe o comprovante do Pix",
                type=["png", "jpg", "jpeg", "pdf"],
            )

            if st.button("Confirmar minha inscrição", key="confirmar_inscricao", use_container_width=True):
                if not nome or not email or not whatsapp:
                    st.error("Preencha nome, e-mail e WhatsApp antes de confirmar.")
                elif (
                    st.session_state.tipo_cota == "reduzida_25"
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


# =========================
# ABA ADMIN
# =========================

with aba_admin:
    st.subheader("Painel administrativo")

    senha = st.text_input("Senha do admin", type="password")
    senha_admin = st.secrets.get("ADMIN_PASSWORD", "admin123")

    if senha != senha_admin:
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


# =========================
# FOOTER
# =========================

st.markdown(
    """
<div class="footer-note">
    Festa Julina da Mary • Organização das inscrições e contribuições<br>
    <strong>Desenvolvimento by Levz</strong>
</div>
""",
    unsafe_allow_html=True,
)
