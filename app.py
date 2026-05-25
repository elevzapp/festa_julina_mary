from datetime import datetime
from pathlib import Path
from textwrap import dedent
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

/* Banner */
img {
    border-radius: 24px;
    box-shadow: 0 14px 34px rgba(90, 60, 20, 0.13);
    border: 1px solid #ead9bc;
}

/* Cards principais */
.intro-card,
.section-card,
.ready-card,
.payment-card {
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

.notice {
    background: #12355b;
    color: #fff8e8;
    padding: 18px 22px;
    border-radius: 18px;
    font-weight: 750;
    text-align: center;
    margin-top: 18px;
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

.ready-card .section-title {
    margin-bottom: 8px;
}

/* Estatísticas */
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

/* Cards de cota */
.option-card,
.option-card-selected {
    border-radius: 24px;
    padding: 24px;
    min-height: 220px;
    box-shadow: 0 8px 22px rgba(90, 60, 20, 0.06);
    margin-bottom: 12px;
}

.option-card {
    background: #fffdf8;
    border: 2px solid #e8d3ae;
}

.option-card-selected {
    background: #fff1cf;
    border: 3px solid #df7f00;
}

.option-title {
    font-size: 1.65rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 8px;
}

.option-price {
    font-size: 2.35rem;
    font-weight: 900;
    color: #b85f00;
    margin-bottom: 12px;
}

.option-text {
    font-size: 1.02rem;
    line-height: 1.55;
    color: #475569;
    margin-bottom: 18px;
}

.option-note {
    color: #64748b;
    font-size: 0.95rem;
    font-weight: 650;
}

/* Cards de itens */
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

/* Pagamento */
.payment-card {
    padding: 30px;
}

.payment-title {
    font-size: 1.75rem;
    font-weight: 850;
    color: #12355b;
    margin-bottom: 16px;
}

.payment-summary {
    background: #fff5df;
    border: 1px solid #f0c987;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
}

.payment-summary strong {
    color: #12355b;
}

.pix-area {
    background: #fffaf0;
    border: 2px dashed #df9b23;
    border-radius: 20px;
    padding: 20px;
    margin-top: 16px;
}

.pix-label {
    color: #64748b;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.pix-value {
    color: #12355b;
    font-size: 1.12rem;
    font-weight: 850;
    margin-bottom: 12px;
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

.payment-note {
    color: #64748b;
    font-size: 0.96rem;
    margin-top: 14px;
}

/* Footer */
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

/* Inputs */
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

/* Upload */
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

/* Botões laranja */
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

/* Admin toggle discreto */
div[data-testid="stCheckbox"] label {
    color: #111827 !important;
    font-size: 1.1rem !important;
}

div[data-testid="stCheckbox"] label p {
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
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


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
# ADMIN DISCRETO
# =========================

col_admin_1, col_admin_2 = st.columns([12, 1])
with col_admin_2:
    modo_admin = st.checkbox("🔒", key="modo_admin_toggle")


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

if modo_admin:
    section_header("Painel administrativo", "Acesso restrito à organização.")

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
<div class="intro-card">
    <div class="intro-title">Que bom termos sua participação esse ano!</div>
    <div class="intro-text">
        Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente.
        Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.
    </div>

    <div class="how-card">
        <div class="how-card-title">Como funciona?</div>
        🎟️ <strong>Cota R$50:</strong> você participa e não precisa levar nada.<br>
        🧺 <strong>Cota R$25:</strong> você participa e também escolhe um item para levar.<br><br>
        A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.
    </div>

    <div class="notice">
        Garanta sua inscrição. As vagas são limitadas!
    </div>
</div>
""")


if not st.session_state.mostrar_inscricao:
    html("""
    <div class="ready-card">
        <div class="section-title">Pronto para participar?</div>
    </div>
    """)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("Quero me inscrever", use_container_width=True):
            st.session_state.mostrar_inscricao = True
            st.rerun()


# =========================
# INSCRIÇÃO
# =========================

if st.session_state.mostrar_inscricao:
    section_header("1. Seus dados")

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
            <div class="stat-label">Cotas R$25 + item disponíveis</div>
            <div class="stat-value">{vagas_25}</div>
        </div>
        """)

    col_cota_50, col_cota_25 = st.columns(2)

    with col_cota_50:
        classe = (
            "option-card-selected"
            if st.session_state.tipo_cota == "completa_50"
            else "option-card"
        )

        html(f"""
        <div class="{classe}">
            <div class="option-title">🎟️ Cota completa</div>
            <div class="option-price">R$50</div>
            <div class="option-text">
                Você participa da festa e não precisa levar nenhum item.
            </div>
            <div class="option-note">Vagas disponíveis: {vagas_50}</div>
        </div>
        """)

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

        html(f"""
        <div class="{classe}">
            <div class="option-title">🧺 Cota com item</div>
            <div class="option-price">R$25</div>
            <div class="option-text">
                Você participa da festa e escolhe um item para levar no dia.
            </div>
            <div class="option-note">Vagas disponíveis: {vagas_25}</div>
        </div>
        """)

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

                    html(f"""
                    <div class="{classe}">
                        <div>
                            <div class="item-title">{meta['emoji']} {meta['titulo']}</div>
                            <div class="item-subtitle">{meta['subtitulo']}</div>
                        </div>
                        <div class="item-vagas">{item["vagas_restantes"]} vaga(s) disponível(is)</div>
                    </div>
                    """)

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

        item_resumo = st.session_state.item_levar or "-"

        html(f"""
        <div class="payment-card">
            <div class="payment-title">4. Resumo e pagamento</div>

            <div class="payment-summary">
                <strong>Participação escolhida:</strong> {tipo_texto}<br>
                <strong>Item para levar:</strong> {item_resumo}<br>
                <strong>Valor do Pix:</strong> R$ {valor_cota:.2f}
            </div>

            <div class="pix-area">
                <div class="pix-label">Recebedor</div>
                <div class="pix-value">{config['nome_recebedor_pix']}</div>

                <div class="pix-label">Chave Pix</div>
                <div class="pix-key">{config["chave_pix"]}</div>

                <div class="payment-note">
                    Depois de realizar o pagamento, anexe o comprovante abaixo para concluir sua inscrição.
                </div>
            </div>
        </div>
        """)

        comprovante = st.file_uploader(
            "Anexe o comprovante do Pix",
            type=["png", "jpg", "jpeg", "pdf"],
        )

        if st.button(
            "Confirmar minha inscrição",
            key="confirmar_inscricao",
            use_container_width=True,
        ):
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
# FOOTER
# =========================

html("""
<div class="footer-note">
    Festa Julina da Mary • Organização das inscrições e contribuições<br>
    <strong>Desenvolvimento by Levz</strong>
</div>
""")
