
from datetime import datetime
import pandas as pd
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Admin | Festa Julina da Mary",
    page_icon="🔐",
    layout="wide",
)

# =========================
# ESTILO
# =========================

st.markdown(
    """
<style>
:root {
    --bg: #fff4df;
    --card: #ffffff;
    --text: #111111;
    --muted: #5f6673;
    --line: #ebc98f;
    --orange: #e88700;
    --orange-dark: #bf6b00;
    --soft-orange: #fff4df;
    --green: #15803d;
    --red: #b91c1c;
    --yellow: #a16207;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.main .block-container {
    max-width: 1240px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, p, div, span, label {
    color: var(--text);
}

.admin-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 10px 28px rgba(90, 60, 20, 0.08);
    margin-bottom: 24px;
}

.admin-title {
    font-size: 2.1rem;
    font-weight: 900;
    margin-bottom: 8px;
    color: #111111;
}

.admin-subtitle {
    font-size: 1rem;
    color: var(--muted);
    line-height: 1.5;
}

.login-box {
    max-width: 420px;
    margin: 30px auto;
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 10px 28px rgba(90, 60, 20, 0.08);
}

.section-title {
    font-size: 1.65rem;
    font-weight: 900;
    margin-top: 28px;
    margin-bottom: 12px;
    color: #111111;
}

.small-note {
    font-size: 0.92rem;
    color: var(--muted);
}

.kpi-card {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    min-height: 112px;
    box-shadow: 0 6px 18px rgba(90, 60, 20, 0.05);
}

.kpi-label {
    font-size: 0.92rem;
    color: var(--muted);
    margin-bottom: 8px;
    font-weight: 700;
}

.kpi-value {
    font-size: 1.9rem;
    color: #111111;
    font-weight: 900;
}

.kpi-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 6px;
}

.status-pill {
    display: inline-block;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 0.82rem;
    font-weight: 800;
}

.status-confirmado {
    background: #dcfce7;
    color: #166534;
}

.status-aguardando {
    background: #fef3c7;
    color: #92400e;
}

.status-recusado {
    background: #fee2e2;
    color: #991b1b;
}

.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    border-radius: 999px !important;
    background: var(--orange) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 800 !important;
}

.stButton > button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
    background: var(--orange-dark) !important;
    color: #ffffff !important;
}

.stButton > button p,
button[kind="primary"] p,
button[kind="secondary"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #e2c792 !important;
    border-radius: 14px !important;
}

div[data-baseweb="input"] input {
    color: #111111 !important;
}

[data-testid="stDataFrame"] {
    background: #ffffff;
}

hr {
    border: none;
    border-top: 1px solid #ead7b5;
    margin: 20px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# CONEXÃO
# =========================

@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_KEY"]
    return create_client(url, key)


supabase = get_supabase_client()


# =========================
# FUNÇÕES
# =========================

def br_money(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def cota_label(tipo):
    return {
        "completa_50": "Cota R$50",
        "reduzida_25": "Cota R$25",
        "minima_5": "Cota R$5",
    }.get(tipo, tipo or "-")


def status_label(status):
    return {
        "aguardando_conferencia": "Aguardando conferência",
        "confirmado": "Confirmado",
        "recusado": "Recusado",
    }.get(status, status or "-")


def buscar_participantes():
    response = (
        supabase
        .table("participantes")
        .select("*")
        .order("criado_em", desc=False)
        .execute()
    )
    return response.data or []


def buscar_itens():
    response = (
        supabase
        .table("itens_levar")
        .select("*")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )
    return response.data or []


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


def preparar_df(participantes):
    df = pd.DataFrame(participantes)

    if df.empty:
        return df

    for col in [
        "nome", "email", "whatsapp", "tipo_cota", "item_levar",
        "status_pagamento", "comprovante_url", "familiares"
    ]:
        if col not in df.columns:
            df[col] = ""

    if "valor_cota" not in df.columns:
        df["valor_cota"] = 0

    if "valor_total" not in df.columns:
        df["valor_total"] = df["valor_cota"]

    if "qtd_adultos_pagantes" not in df.columns:
        df["qtd_adultos_pagantes"] = 1

    if "qtd_criancas_ate_10" not in df.columns:
        df["qtd_criancas_ate_10"] = 0

    if "criado_em" not in df.columns:
        df["criado_em"] = None

    df["valor_cota"] = pd.to_numeric(df["valor_cota"], errors="coerce").fillna(0)
    df["valor_total"] = pd.to_numeric(df["valor_total"], errors="coerce").fillna(df["valor_cota"])
    df["Cota"] = df["tipo_cota"].apply(cota_label)
    df["Status"] = df["status_pagamento"].apply(status_label)
    df["Item"] = df["item_levar"].fillna("").replace("", "-")
    df["Valor"] = df["valor_cota"].apply(br_money)

    try:
        df["Data"] = pd.to_datetime(df["criado_em"], errors="coerce").dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        df["Data"] = ""

    return df


def tabela_participantes(df, filtro_cota=None, filtro_status=None):
    if df.empty:
        st.info("Ainda não há participantes cadastrados.")
        return

    base = df.copy()

    if filtro_cota and filtro_cota != "Todas":
        mapa_cota = {
            "Cota R$50": "completa_50",
            "Cota R$25": "reduzida_25",
            "Cota R$5": "minima_5",
        }
        base = base[base["tipo_cota"] == mapa_cota.get(filtro_cota)]

    if filtro_status and filtro_status != "Todos":
        mapa_status = {
            "Aguardando conferência": "aguardando_conferencia",
            "Confirmado": "confirmado",
            "Recusado": "recusado",
        }
        base = base[base["status_pagamento"] == mapa_status.get(filtro_status)]

    colunas = ["nome", "Cota", "Valor", "Item", "Status", "email", "whatsapp", "Data"]
    colunas_existentes = [c for c in colunas if c in base.columns]

    st.dataframe(
        base[colunas_existentes].rename(
            columns={
                "nome": "Participante",
                "email": "E-mail",
                "whatsapp": "WhatsApp",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_kpi(label, value, sub=""):
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-sub">{sub}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# =========================
# LOGIN
# =========================

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

st.markdown(
    """
<div class="admin-card">
    <div class="admin-title">Painel administrativo</div>
    <div class="admin-subtitle">Acesso restrito à organização da Festa Julina da Mary.</div>
</div>
""",
    unsafe_allow_html=True,
)

senha_admin = st.secrets.get("ADMIN_PASSWORD", "admin123")

if not st.session_state.admin_logado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### Entrar no painel")
    senha = st.text_input("Senha", type="password", key="senha_admin_input")

    col_login, col_voltar = st.columns(2)

    with col_login:
        if st.button("Acessar", use_container_width=True):
            if senha == senha_admin:
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("Senha incorreta.")

    with col_voltar:
        st.link_button("Voltar para inscrição", "/", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================
# ADMIN LOGADO
# =========================

col_top1, col_top2, col_top3 = st.columns([1, 1, 1])

with col_top1:
    st.link_button("Voltar para inscrição", "/", use_container_width=True)

with col_top2:
    if st.button("Atualizar dados", use_container_width=True):
        st.rerun()

with col_top3:
    if st.button("Sair do admin", use_container_width=True):
        st.session_state.admin_logado = False
        st.rerun()


participantes = buscar_participantes()
itens = buscar_itens()
df = preparar_df(participantes)

if df.empty:
    st.info("Ainda não há inscrições cadastradas.")
    st.stop()

ativos = df[df["status_pagamento"].isin(["aguardando_conferencia", "confirmado"])].copy()
confirmados = df[df["status_pagamento"] == "confirmado"].copy()
pendentes = df[df["status_pagamento"] == "aguardando_conferencia"].copy()
recusados = df[df["status_pagamento"] == "recusado"].copy()

total_previsto = ativos["valor_cota"].sum()
total_confirmado = confirmados["valor_cota"].sum()
total_pendente = pendentes["valor_cota"].sum()

qtd_50 = len(ativos[ativos["tipo_cota"] == "completa_50"])
qtd_25 = len(ativos[ativos["tipo_cota"] == "reduzida_25"])
qtd_5 = len(ativos[ativos["tipo_cota"] == "minima_5"])

limite_50 = 30
limite_25 = 20
limite_5 = 5

meta_estimativa = (limite_50 * 50) + (limite_25 * 25) + (limite_5 * 5)
falta_estimativa = max(meta_estimativa - total_confirmado, 0)

st.markdown('<div class="section-title">Resumo financeiro e de cotas</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi("Total previsto", br_money(total_previsto), "Aguardando + confirmado")
with k2:
    render_kpi("Total confirmado", br_money(total_confirmado), "Pagamentos conferidos")
with k3:
    render_kpi("Pendente de conferência", br_money(total_pendente), "Comprovantes enviados")
with k4:
    render_kpi("Falta para estimativa", br_money(falta_estimativa), f"Estimativa base: {br_money(meta_estimativa)}")

k5, k6, k7, k8 = st.columns(4)
with k5:
    render_kpi("Participantes ativos", len(ativos), "Aguardando + confirmado")
with k6:
    render_kpi("Cota R$50", f"{qtd_50}/{limite_50}", f"Disponível: {max(limite_50 - qtd_50, 0)}")
with k7:
    render_kpi("Cota R$25", f"{qtd_25}/{limite_25}", f"Disponível: {max(limite_25 - qtd_25, 0)}")
with k8:
    render_kpi("Cota R$5", f"{qtd_5}/{limite_5}", "Simbólica: pode passar")


# =========================
# ITENS
# =========================

st.markdown('<div class="section-title">Controle dos itens para levar</div>', unsafe_allow_html=True)

itens_df_rows = []

for item in itens:
    nome_item = item.get("nome")
    vagas_total = int(item.get("vagas_total") or 0)

    escolhidos = ativos[ativos["item_levar"] == nome_item]
    qtd_escolhida = len(escolhidos)
    restante = max(vagas_total - qtd_escolhida, 0)

    pessoas = ", ".join(escolhidos["nome"].tolist()) if qtd_escolhida else "-"

    itens_df_rows.append(
        {
            "Item": nome_item,
            "Vagas totais": vagas_total,
            "Já escolhido": qtd_escolhida,
            "Faltam": restante,
            "Quem escolheu": pessoas,
        }
    )

itens_df = pd.DataFrame(itens_df_rows)

if itens_df.empty:
    st.info("Nenhum item cadastrado em itens_levar.")
else:
    st.dataframe(itens_df, use_container_width=True, hide_index=True)

    faltantes = itens_df[itens_df["Faltam"] > 0].copy()
    if not faltantes.empty:
        st.markdown("#### Itens que ainda faltam")
        st.dataframe(
            faltantes[["Item", "Faltam"]],
            use_container_width=True,
            hide_index=True,
        )


# =========================
# TABELAS POR COTA
# =========================

st.markdown('<div class="section-title">Participantes por cota</div>', unsafe_allow_html=True)

tab50, tab25, tab5, tabtodos = st.tabs(["Cota R$50", "Cota R$25", "Cota R$5", "Todos"])

with tab50:
    tabela_participantes(df, filtro_cota="Cota R$50", filtro_status="Todos")

with tab25:
    tabela_participantes(df, filtro_cota="Cota R$25", filtro_status="Todos")

with tab5:
    tabela_participantes(df, filtro_cota="Cota R$5", filtro_status="Todos")

with tabtodos:
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        filtro_cota = st.selectbox(
            "Filtrar por cota",
            ["Todas", "Cota R$50", "Cota R$25", "Cota R$5"],
        )
    with col_filtro2:
        filtro_status = st.selectbox(
            "Filtrar por status",
            ["Todos", "Aguardando conferência", "Confirmado", "Recusado"],
        )

    tabela_participantes(df, filtro_cota=filtro_cota, filtro_status=filtro_status)


# =========================
# CONFERÊNCIA DE PAGAMENTO
# =========================

st.markdown('<div class="section-title">Conferência de pagamentos</div>', unsafe_allow_html=True)

for participante in df.sort_values("criado_em", ascending=False).to_dict("records"):
    nome = participante.get("nome", "-")
    valor = br_money(participante.get("valor_cota", 0))
    status = participante.get("status_pagamento", "")
    item = participante.get("item_levar") or "-"
    cota = cota_label(participante.get("tipo_cota"))

    with st.expander(f"{nome} • {cota} • {valor} • {status_label(status)}"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write(f"**Nome:** {nome}")
            st.write(f"**Cota:** {cota}")
            st.write(f"**Valor:** {valor}")
            st.write(f"**Item:** {item}")

        with c2:
            st.write(f"**E-mail:** {participante.get('email', '-')}")
            st.write(f"**WhatsApp:** {participante.get('whatsapp', '-')}")
            st.write(f"**Status atual:** {status_label(status)}")

        with c3:
            comprovante_path = participante.get("comprovante_url")
            link_comprovante = gerar_link_comprovante(comprovante_path)

            if link_comprovante:
                st.link_button("Abrir comprovante", link_comprovante, use_container_width=True)
            else:
                st.caption("Sem comprovante anexado.")

            status_opcoes = {
                "Aguardando conferência": "aguardando_conferencia",
                "Confirmado": "confirmado",
                "Recusado": "recusado",
            }

            status_atual_label = status_label(status)
            if status_atual_label not in status_opcoes:
                status_atual_label = "Aguardando conferência"

            novo_status_label = st.selectbox(
                "Novo status",
                list(status_opcoes.keys()),
                index=list(status_opcoes.keys()).index(status_atual_label),
                key=f"status_{participante.get('id')}",
            )

            if st.button("Salvar status", key=f"salvar_{participante.get('id')}", use_container_width=True):
                atualizar_status(participante.get("id"), status_opcoes[novo_status_label])
                st.success("Status atualizado.")
                st.rerun()


# =========================
# EXPORTAÇÃO
# =========================

st.markdown('<div class="section-title">Exportar dados</div>', unsafe_allow_html=True)

export_cols = [
    "nome", "email", "whatsapp", "Cota", "valor_cota", "Item",
    "Status", "qtd_adultos_pagantes", "qtd_criancas_ate_10",
    "familiares", "comprovante_url", "Data"
]
export_cols = [c for c in export_cols if c in df.columns]

csv = df[export_cols].to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "Baixar planilha CSV",
    data=csv,
    file_name="participantes_festa_julina_mary.csv",
    mime="text/csv",
)
