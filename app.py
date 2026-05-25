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


@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_KEY"]
    return create_client(url, key)


supabase = get_supabase_client()


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


config = buscar_configuracao()

st.title("🌽 Festa Junina da Mary")
st.write("Organização das cotas e dos itens para levar.")

st.info(
    "Escolha sua forma de participação. "
    "A confirmação do pagamento será feita manualmente após conferência do comprovante."
)

aba_publica, aba_admin = st.tabs(["Participar", "Admin"])


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
    col1.metric("Vagas cota R$50", vagas_50)
    col2.metric("Vagas cota R$25 + item", vagas_25)

    itens_disponiveis = buscar_itens_disponiveis()

    opcoes_cota = []

    if vagas_50 > 0:
        opcoes_cota.append("R$50 - Não preciso levar nada")

    if vagas_25 > 0 and len(itens_disponiveis) > 0:
        opcoes_cota.append("R$25 - Vou levar um item")

    if not opcoes_cota:
        st.warning("As vagas foram preenchidas.")
    else:
        with st.form("form_participacao"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")

            escolha_cota = st.radio("Escolha sua participação", opcoes_cota)

            item_escolhido = None
            tipo_cota = None
            valor_cota = None

            if escolha_cota.startswith("R$50"):
                tipo_cota = "completa_50"
                valor_cota = valor_50
                st.success("Você escolheu a cota de R$50 e não precisa levar item.")

            if escolha_cota.startswith("R$25"):
                tipo_cota = "reduzida_25"
                valor_cota = valor_25

                nomes_itens = [
                    f"{item['nome']} — {item['vagas_restantes']} vaga(s)"
                    for item in itens_disponiveis
                ]

                item_label = st.selectbox(
                    "Escolha o item que você vai levar",
                    nomes_itens,
                )

                item_escolhido = item_label.split(" — ")[0]

            st.markdown("### Dados para Pix")
            st.write(f"**Valor:** R$ {valor_cota:.2f}")
            st.write(f"**Recebedor:** {config['nome_recebedor_pix']}")
            st.code(config["chave_pix"])

            comprovante = st.file_uploader(
                "Anexe o comprovante do Pix",
                type=["png", "jpg", "jpeg", "pdf"],
            )

            enviar = st.form_submit_button("Enviar participação")

            if enviar:
                if not nome or not email or not whatsapp:
                    st.error("Preencha nome, e-mail e WhatsApp.")
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
                    st.write(f"**Comprovante:** {participante.get('comprovante_url') or '-'}")

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
