from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Festa Junina da Mary",
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
            background: linear-gradient(180deg, #07182f 0%, #101010 45%, #15100b 100%);
            color: #fff;
        }

        .main .block-container {
            max-width: 920px;
            padding-top: 2rem;
        }

        .hero {
            background: linear-gradient(135deg, #102b4d 0%, #7a2518 55%, #d98722 100%);
            padding: 28px;
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 18px 50px rgba(0,0,0,0.35);
            margin-bottom: 24px;
        }

        .hero h1 {
            margin: 0;
            font-size: 42px;
            line-height: 1.05;
            color: #fff7df;
        }

        .hero p {
            font-size: 18px;
            color: #fff3cf;
            margin-top: 12px;
        }

        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.14);
            padding: 7px 12px;
            border-radius: 999px;
            margin-bottom: 14px;
            color: #fff7df;
            font-weight: 700;
        }

        .card-info {
            background: rgba(255, 247, 223, 0.08);
            border: 1px solid rgba(255, 247, 223, 0.18);
            padding: 18px;
            border-radius: 18px;
            margin: 14px 0;
        }

        .card-option {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            padding: 18px;
            border-radius: 18px;
            margin-bottom: 12px;
        }

        .pix-box {
            background: #1f2937;
            border: 1px dashed #f5b94c;
            border-radius: 18px;
            padding: 18px;
            margin-top: 18px;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.08);
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.14);
        }

        .small-note {
            font-size: 14px;
            color: #f8d996;
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
    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome_seguro}_{uuid4()}.{extensao}"

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


# =========================
# INTERFACE
# =========================

config = buscar_configuracao()

st.markdown(
    """
    <div class="hero">
        <div class="badge">🔥 Save the date • 18 de Julho</div>
        <h1>🌽 Festa Junina da Mary</h1>
        <p>
            Escolha sua forma de participação, envie o comprovante do Pix
            e ajude a organizar os comes, bebidas e itens da festa.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card-info">
        <strong>Como funciona?</strong><br><br>
        <strong>🎟️ Cota R$50:</strong> você participa e não precisa levar nada.<br>
        <strong>🧺 Cota R$25:</strong> você participa e também escolhe um item para levar.<br><br>
        A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.
    </div>
    """,
    unsafe_allow_html=True,
)

aba_publica, aba_admin = st.tabs(["🎉 Participar", "🔐 Admin"])


with aba_publica:
    st.subheader("Quero participar")

    limite_50 = int(config["limite_cota_50"])
    limite_25 = int(config["limite_cota_25"])
    valor_50 = float(config["valor_cota_50"])
    valor_25 = float(config["valor_cota_25"])

    total_50 = contar_participantes_por_cota("completa_50")
    total_25 = contar_participantes_por_cota("reduzida_25")

    vagas_50 = max(limite_50 - total_50, 0)
    vagas_25 = max(limite_25 - total_25, 0)

    col1, col2 = st.columns(2)
    col1.metric("Cota R$50 disponíveis", vagas_50)
    col2.metric("Cota R$25 + item disponíveis", vagas_25)

    itens_disponiveis = buscar_itens_disponiveis()

    opcoes_cota = []

    if vagas_50 > 0:
        opcoes_cota.append("R$50 - Não preciso levar nada")

    if vagas_25 > 0 and len(itens_disponiveis) > 0:
        opcoes_cota.append("R$25 - Vou levar um item")

    if not opcoes_cota:
        st.warning("As vagas foram preenchidas.")
    else:
        st.markdown("### 1. Escolha sua forma de participação")

        escolha_cota = st.radio(
            "Selecione uma opção:",
            opcoes_cota,
            key="escolha_cota",
        )

        item_escolhido = None
        tipo_cota = None
        valor_cota = None

        if escolha_cota.startswith("R$50"):
            tipo_cota = "completa_50"
            valor_cota = valor_50

            st.markdown(
                """
                <div class="card-option">
                    <strong>🎟️ Você escolheu a cota de R$50.</strong><br>
                    Você não precisa levar nenhum item. Sua contribuição ajuda a cobrir
                    os itens principais da festa.
                </div>
                """,
                unsafe_allow_html=True,
            )

        if escolha_cota.startswith("R$25"):
            tipo_cota = "reduzida_25"
            valor_cota = valor_25

            st.markdown(
                """
                <div class="card-option">
                    <strong>🧺 Você escolheu a cota de R$25.</strong><br>
                    Agora selecione abaixo qual item você vai levar no dia da festa.
                </div>
                """,
                unsafe_allow_html=True,
            )

            nomes_itens = [
                f"{item['nome']} — {item['vagas_restantes']} vaga(s) disponível(is)"
                for item in itens_disponiveis
            ]

            item_label = st.selectbox(
                "Item que você vai levar:",
                nomes_itens,
                key="item_escolhido",
            )

            item_escolhido = item_label.split(" — ")[0]

        st.markdown("### 2. Preencha seus dados")

        with st.form("form_participacao"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")

            st.markdown("### 3. Faça o Pix")

            st.markdown(
                f"""
                <div class="pix-box">
                    <strong>Valor:</strong> R$ {valor_cota:.2f}<br>
                    <strong>Recebedor:</strong> {config['nome_recebedor_pix']}<br>
                    <strong>Chave Pix:</strong><br>
                    <code>{config["chave_pix"]}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                '<p class="small-note">Depois de pagar, anexe o comprovante abaixo.</p>',
                unsafe_allow_html=True,
            )

            comprovante = st.file_uploader(
                "Anexe o comprovante do Pix",
                type=["png", "jpg", "jpeg", "pdf"],
            )

            enviar = st.form_submit_button("Enviar participação")

            if enviar:
                if not nome or not email or not whatsapp:
                    st.error("Preencha nome, e-mail e WhatsApp.")
                elif tipo_cota == "reduzida_25" and not item_escolhido:
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
                            tipo_cota=tipo_cota,
                            valor_cota=valor_cota,
                            item_levar=item_escolhido,
                            comprovante_url=comprovante_url,
                        )

                        st.success(
                            "Participação enviada com sucesso! "
                            "O pagamento ficará aguardando conferência."
                        )
                        st.rerun()

                    except Exception as erro:
                        st.error("Não foi possível salvar sua participação.")
                        st.exception(erro)


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
                    f"{participante['nome']} - R$ {participante['valor_cota']}"
                ):
                    st.write(f"**E-mail:** {participante['email']}")
                    st.write(f"**WhatsApp:** {participante.get('whatsapp', '')}")
                    st.write(f"**Tipo de cota:** {participante['tipo_cota']}")
                    st.write(f"**Item para levar:** {participante.get('item_levar') or '-'}")
                    st.write(f"**Status:** {participante['status_pagamento']}")
                    st.write(f"**Comprovante salvo como:** {participante.get('comprovante_url') or '-'}")

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
