
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
    color: var(--text) !important;
}

.admin-card, .login-box, .kpi-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 24px;
    box-shadow: 0 10px 28px rgba(90, 60, 20, 0.08);
}

.admin-card {
    padding: 28px;
    margin-bottom: 24px;
}

.admin-title {
    font-size: 2.1rem;
    font-weight: 900;
    margin-bottom: 8px;
}

.admin-subtitle, .small-note, .kpi-sub {
    color: var(--muted) !important;
}

.login-box {
    max-width: 420px;
    margin: 30px auto;
    padding: 26px;
}

.section-title {
    font-size: 1.65rem;
    font-weight: 900;
    margin-top: 28px;
    margin-bottom: 12px;
}

.kpi-card {
    padding: 18px;
    min-height: 112px;
    margin-bottom: 12px;
}

.kpi-label {
    font-size: 0.92rem;
    color: var(--muted) !important;
    margin-bottom: 8px;
    font-weight: 700;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 900;
}

.status-pill {
    display: inline-block;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 0.82rem;
    font-weight: 800;
}

.status-confirmado { background: #dcfce7; color: #166534 !important; }
.status-aguardando { background: #fef3c7; color: #92400e !important; }
.status-recusado { background: #fee2e2; color: #991b1b !important; }

/* Botões Streamlit e links com aparência de botão */
.stButton > button,
button[kind="primary"],
button[kind="secondary"],
div[data-testid="stLinkButton"] a,
a.admin-link-button {
    border-radius: 999px !important;
    background: var(--orange) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    text-align: center !important;
    padding: 0.65rem 1.1rem !important;
}

.stButton > button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover,
div[data-testid="stLinkButton"] a:hover,
a.admin-link-button:hover {
    background: var(--orange-dark) !important;
    color: #ffffff !important;
    border: none !important;
}

.stButton > button p,
button[kind="primary"] p,
button[kind="secondary"] p,
div[data-testid="stLinkButton"] a p,
a.admin-link-button {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Inputs e selects claros */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #e2c792 !important;
    border-radius: 14px !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #111111 !important;
}


/* Dropdown do select claro */
div[data-baseweb="popover"] {
    background: #ffffff !important;
    color: #111111 !important;
}

div[data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}

ul[role="listbox"],
div[role="listbox"] {
    background: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #e2c792 !important;
}

li[role="option"],
div[role="option"] {
    background: #ffffff !important;
    color: #111111 !important;
}

li[role="option"]:hover,
div[role="option"]:hover {
    background: #fff1d6 !important;
    color: #111111 !important;
}

.login-title-block {
    max-width: 420px;
    margin: 26px auto 8px auto;
}

.login-title-block h3 {
    margin-bottom: 8px;
}

/* Expander claro */
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #ebc98f !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
}

div[data-testid="stExpander"] details summary {
    background: #fffaf0 !important;
    color: #111111 !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
}

div[data-testid="stExpander"] details summary * {
    color: #111111 !important;
}

/* Tabelas HTML claras */
.admin-table-wrap {
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #ebc98f;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(90, 60, 20, 0.04);
    margin: 8px 0 22px 0;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
    background: #ffffff;
    color: #111111;
}

.admin-table th {
    background: #fff1d6;
    color: #111111 !important;
    font-weight: 900;
    text-align: left;
    padding: 12px 14px;
    border-bottom: 1px solid #ebc98f;
    white-space: nowrap;
}

.admin-table td {
    background: #ffffff;
    color: #111111 !important;
    padding: 11px 14px;
    border-bottom: 1px solid #f1e1c4;
    vertical-align: top;
}

.admin-table tr:nth-child(even) td {
    background: #fffaf0;
}

.admin-table tr:last-child td {
    border-bottom: none;
}

.table-empty {
    background: #ffffff;
    border: 1px solid #ebc98f;
    border-radius: 14px;
    padding: 14px;
    color: #5f6673 !important;
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
        "completa_35": "Cota R$35",
        "reduzida_10": "Cota R$10",
    }.get(tipo, tipo or "-")


def status_label(status):
    return {
        "aguardando_conferencia": "Aguardando conferência",
        "confirmado": "Confirmado",
        "recusado": "Recusado",
    }.get(status, status or "-")




def safe_html(value):
    if value is None:
        return ""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_table(dataframe, columns=None):
    if dataframe is None or dataframe.empty:
        st.markdown('<div class="table-empty">Nenhum registro encontrado.</div>', unsafe_allow_html=True)
        return

    base = dataframe.copy()
    if columns:
        base = base[[c for c in columns if c in base.columns]]

    header = "".join(f"<th>{safe_html(col)}</th>" for col in base.columns)
    rows = []
    for _, row in base.iterrows():
        cells = "".join(f"<td>{safe_html(row[col])}</td>" for col in base.columns)
        rows.append(f"<tr>{cells}</tr>")

    html_table = (
        '<div class="admin-table-wrap">'
        '<table class="admin-table">'
        f'<thead><tr>{header}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '</div>'
    )
    st.markdown(html_table, unsafe_allow_html=True)

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
            "Cota R$35": "completa_35",
            "Cota R$10": "reduzida_10",
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

    render_table(
        base[colunas_existentes].rename(
            columns={
                "nome": "Participante",
                "email": "E-mail",
                "whatsapp": "WhatsApp",
            }
        )
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
    st.markdown(
        '''<div class="login-title-block">
            <h3>Entrar no painel</h3>
            <div class="admin-subtitle">Digite a senha para acessar a conferência.</div>
        </div>''',
        unsafe_allow_html=True,
    )

    col_left, col_center, col_right = st.columns([1.4, 1, 1.4])

    with col_center:
        senha = st.text_input("Senha", type="password", key="senha_admin_input")

        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.button("Acessar", use_container_width=True):
                if senha == senha_admin:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")

        with btn_col2:
            st.markdown(
                '<a class="admin-link-button" href="/" style="display:block;">Voltar</a>',
                unsafe_allow_html=True,
            )

    st.stop()


# =========================
# ADMIN LOGADO
# =========================

col_top1, col_top2, col_top3 = st.columns([1, 1, 1])

with col_top1:
    st.markdown('<a class="admin-link-button" href="/" style="display:block;">Voltar para inscrição</a>', unsafe_allow_html=True)

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

LIMITE_COTA_35 = 52
LIMITE_COTA_10 = 54

total_previsto = ativos["valor_cota"].sum()
total_confirmado = confirmados["valor_cota"].sum()
total_pendente = pendentes["valor_cota"].sum()

qtd_35 = len(ativos[ativos["tipo_cota"] == "completa_35"])
qtd_10 = len(ativos[ativos["tipo_cota"] == "reduzida_10"])

# Estimativa de referência: 52 adultos pagando a cota cheia de R$35.
meta_estimativa = LIMITE_COTA_35 * 35
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

k5, k6, k7 = st.columns(3)
with k5:
    render_kpi("Participantes ativos", len(ativos), "Aguardando + confirmado")
with k6:
    render_kpi("Cota R$35", f"{qtd_35}/{LIMITE_COTA_35}", f"Disponível: {max(LIMITE_COTA_35 - qtd_35, 0)}")
with k7:
    render_kpi("Cota R$10", f"{qtd_10}/{LIMITE_COTA_10}", f"Disponível: {max(LIMITE_COTA_10 - qtd_10, 0)}")


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
    render_table(itens_df)

    faltantes = itens_df[itens_df["Faltam"] > 0].copy()
    if not faltantes.empty:
        st.markdown("#### Itens que ainda faltam")
        render_table(faltantes[["Item", "Faltam"]])


# =========================
# TABELAS POR COTA
# =========================

st.markdown('<div class="section-title">Participantes por cota</div>', unsafe_allow_html=True)

tab35, tab10, tabtodos = st.tabs(["Cota R$35", "Cota R$10", "Todos"])

with tab35:
    tabela_participantes(df, filtro_cota="Cota R$35", filtro_status="Todos")

with tab10:
    tabela_participantes(df, filtro_cota="Cota R$10", filtro_status="Todos")

with tabtodos:
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        filtro_cota = st.selectbox(
            "Filtrar por cota",
            ["Todas", "Cota R$35", "Cota R$10"],
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
