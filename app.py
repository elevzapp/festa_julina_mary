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
        background: #fff7e8;
        color: #1f2933;
    }

    .main .block-container {
        max-width: 980px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #12355b;
    }

    .intro-card {
        background: #ffffff;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(80, 45, 20, 0.10);
        border: 1px solid rgba(168, 91, 31, 0.16);
        margin: 22px 0;
    }

    .intro-card p {
        font-size: 18px;
        line-height: 1.6;
        color: #334155;
    }

    .how-card {
        background: #fff0cf;
        border-left: 8px solid #d97706;
        border-radius: 18px;
        padding: 22px;
        margin: 18px 0;
        color: #1f2933;
    }

    .notice {
        background: #12355b;
        color: #fff7e8;
        padding: 18px 22px;
        border-radius: 18px;
        margin: 18px 0;
        font-weight: 600;
    }

    .section-card {
        background: #ffffff;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(80, 45, 20, 0.10);
        border: 1px solid rgba(168, 91, 31, 0.16);
        margin: 24px 0;
    }

    .option-card {
        background: #fffaf0;
        border: 2px solid #efd3a1;
        border-radius: 20px;
        padding: 22px;
        min-height: 180px;
        margin-bottom: 14px;
    }

    .option-card-selected {
        background: #fff0cf;
        border: 3px solid #d97706;
        border-radius: 20px;
        padding: 22px;
        min-height: 180px;
        margin-bottom: 14px;
    }

    .option-title {
        font-size: 24px;
        font-weight: 800;
        color: #12355b;
        margin-bottom: 8px;
    }

    .option-price {
        font-size: 32px;
        font-weight: 900;
        color: #b45309;
        margin: 8px 0;
    }

    .option-text {
        font-size: 16px;
        color: #475569;
        line-height: 1.45;
    }

    .item-card {
        background: #fffaf0;
        border: 2px solid #efd3a1;
        border-radius: 18px;
        padding: 18px;
        min-height: 130px;
        margin-bottom: 10px;
    }

    .item-card-selected {
        background: #ecfccb;
        border: 3px solid #65a30d;
        border-radius: 18px;
        padding: 18px;
        min-height: 130px;
        margin-bottom: 10px;
    }

    .item-title {
        font-size: 18px;
        font-weight: 800;
        color: #12355b;
    }

    .item-vagas {
        font-size: 14px;
        color: #64748b;
        margin-top: 8px;
    }

    .pix-box {
        background: #12355b;
        color: #fff7e8;
        border-radius: 20px;
        padding: 24px;
        margin: 18px 0;
        border: 2px dashed #f6c453;
    }

    .pix-box code {
        background: rgba(255,255,255,0.14);
        color: #ffffff;
        padding: 10px 12px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 8px;
        font-size: 18px;
    }

    .summary-box {
        background: #fef3c7;
        border-radius: 18px;
        padding: 20px;
        margin: 18px 0;
        border: 1px solid #f59e0b;
        color: #1f2933;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(168, 91, 31, 0.18);
        box-shadow: 0 8px 22px rgba(80, 45, 20, 0.08);
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: none;
        background: #d97706;
        color: #ffffff;
        padding: 0.65rem 1.2rem;
    }

    .stButton > button:hover {
        background: #b45309;
        color: #ffffff;
        border: none;
    }

    .secondary-note {
        color: #64748b;
        font-size: 14px;
    }

    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 28px;
    }

    img {
        border-radius: 22px;
        box-shadow: 0 14px 40px rgba(80, 45, 20, 0.16);
        border: 1px solid rgba(168, 91, 31, 0.18);
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
        st.write("Arquivo encontrado:")
        st.code(str(banner_path))
        st.write("Tamanho do arquivo em bytes:")
        st.code(str(banner_path.stat().st_size))
else:
    st.error(
        "Banner não encontrado. Confirme se o arquivo banner_festa_julina.png "
        "está na raiz do repositório, junto com app.py."
    )
    st.write("Arquivos encontrados no projeto:")
    st.write([p.name for p in Path(__file__).parent.iterdir()])


# =========================
# INTRODUÇÃO
# =========================

st.markdown(
"""
<div class="intro-card">
<h2>Que bom termos sua participação esse ano!</h2>
<p>
Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente.
Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.
</p>

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
# ABA DE INSCRIÇÃO
# =========================

with aba_publica:
    if not st.session_state.mostrar_inscricao:
        st.markdown(
"""
<div class="section-card">
<h3>Pronto para participar?</h3>
<p>
Clique no botão <strong>Quero me inscrever</strong> acima para abrir o formulário.
</p>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="section-card"><h3>1. Seus dados</h3>',
            unsafe_allow_html=True,
        )

        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-card"><h3>2. Escolha sua participação</h3>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        col1.metric("Cotas R$50 disponíveis", vagas_50)
        col2.metric("Cotas R$25 + item disponíveis", vagas_25)

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
<br>
<div class="secondary-note">
Vagas disponíveis: {vagas_50}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            if vagas_50 > 0:
                if st.button("Escolher R$50", use_container_width=True):
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
<br>
<div class="secondary-note">
Vagas disponíveis: {vagas_25}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            if vagas_25 > 0 and len(itens_disponiveis) > 0:
                if st.button("Escolher R$25", use_container_width=True):
                    escolher_cota("reduzida_25")
                    st.rerun()
            else:
                st.warning("Cota esgotada.")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.tipo_cota == "reduzida_25":
            st.markdown(
                '<div class="section-card"><h3>3. Escolha o item que você vai levar</h3>',
                unsafe_allow_html=True,
            )

            st.write("Selecione uma das opções disponíveis abaixo.")

            itens_por_linha = 3

            for i in range(0, len(itens_disponiveis), itens_por_linha):
                cols = st.columns(itens_por_linha)
                grupo = itens_disponiveis[i:i + itens_por_linha]

                for col, item in zip(cols, grupo):
                    with col:
                        selecionado = st.session_state.item_levar == item["nome"]
                        classe = "item-card-selected" if selecionado else "item-card"

                        st.markdown(
                            f"""
<div class="{classe}">
<div class="item-title">🧺 {item["nome"]}</div>
<div class="item-vagas">
{item["vagas_restantes"]} vaga(s) disponível(is)
</div>
</div>
""",
                            unsafe_allow_html=True,
                        )

                        if st.button(
                            "Selecionar",
                            key=f"item_{item['nome']}",
                            use_container_width=True,
                        ):
                            escolher_item(item["nome"])
                            st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

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

            st.markdown(
                '<div class="section-card"><h3>4. Resumo e pagamento</h3>',
                unsafe_allow_html=True,
            )

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
<h3 style="color:#fff7e8; margin-top:0;">Dados para Pix</h3>
<strong>Recebedor:</strong> {config['nome_recebedor_pix']}<br>
<strong>Chave Pix:</strong><br>
<code>{config["chave_pix"]}</code>
</div>
""",
                unsafe_allow_html=True,
            )

            comprovante = st.file_uploader(
                "Anexe o comprovante do Pix",
                type=["png", "jpg", "jpeg", "pdf"],
            )

            if st.button("Confirmar minha inscrição", use_container_width=True):
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

            st.markdown("</div>", unsafe_allow_html=True)


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


st.markdown(
"""
<div class="footer-note">
Festa Julina da Mary • Organização das inscrições e contribuições
</div>
""",
    unsafe_allow_html=True,
)
