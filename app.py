
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import base64
import json

import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Festa Julina da Mary",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================
# CONFIGURAÇÃO VISUAL
# =========================

st.markdown(
    """
<style>
:root {
    --azul: #12355b;
    --azul-2: #17456f;
    --laranja: #df7f00;
    --laranja-2: #bf6900;
    --amarelo: #f8c94a;
    --fundo: #fff5e6;
    --creme: #fffaf0;
    --borda: #efd3a1;
    --texto: #24364b;
    --muted: #64748b;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

.stApp {
    background: var(--fundo);
    color: var(--texto);
}

.main .block-container {
    max-width: 100%;
    padding: 0 0 3rem 0;
}

h1, h2, h3 {
    color: var(--azul) !important;
}

p, div, span, label {
    color: var(--texto);
}

section[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #d8b981 !important;
    border-radius: 18px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: var(--texto) !important;
}

section[data-testid="stFileUploaderDropzone"] button,
.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    border-radius: 999px !important;
    background: var(--laranja) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 850 !important;
    padding: 0.72rem 1.25rem !important;
}

section[data-testid="stFileUploaderDropzone"] button *,
.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    color: #ffffff !important;
    font-weight: 850 !important;
}

.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover {
    background: var(--laranja-2) !important;
    color: #ffffff !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border: 1px solid #d9c29b !important;
    border-radius: 14px !important;
}

div[data-baseweb="input"] input,
textarea {
    color: #1f2937 !important;
    background: #ffffff !important;
}

.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stFileUploader label {
    color: var(--azul) !important;
    font-weight: 750 !important;
}

.hero-img {
    width: 100vw;
    max-width: 100vw;
    display: block;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    object-fit: cover;
}

.section {
    width: 100%;
    padding: 52px 18px;
}

.section-white {
    background: #ffffff;
}

.section-yellow {
    background: #f7c64a;
}

.section-cream {
    background: var(--fundo);
}

.section-inner {
    max-width: 980px;
    margin: 0 auto;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 44px;
    align-items: center;
}

.hero-title {
    font-size: clamp(2.6rem, 7vw, 5.5rem);
    line-height: 0.98;
    color: var(--azul);
    font-weight: 950;
    letter-spacing: -0.045em;
    margin-bottom: 22px;
}

.hero-text {
    font-size: clamp(1.05rem, 2.5vw, 1.35rem);
    line-height: 1.65;
    color: var(--texto);
    margin-bottom: 28px;
}

.info-card {
    background: var(--creme);
    border: 1px solid var(--borda);
    border-left: 8px solid var(--laranja);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 12px 28px rgba(90, 60, 20, 0.07);
}

.info-card h2 {
    margin: 0 0 16px 0;
    font-size: clamp(1.7rem, 4vw, 2.25rem);
}

.info-line {
    line-height: 1.65;
    margin: 13px 0;
    font-size: 1.06rem;
}

.cta-link {
    display: inline-block;
    background: var(--laranja);
    color: #ffffff !important;
    font-weight: 900;
    text-decoration: none !important;
    padding: 15px 32px;
    border-radius: 999px;
    box-shadow: 0 10px 22px rgba(90,60,20,0.16);
}

.section-title {
    text-align: center;
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 950;
    color: var(--azul);
    letter-spacing: -0.035em;
    line-height: 1.05;
    margin-bottom: 12px;
}

.section-subtitle {
    text-align: center;
    font-size: 1.15rem;
    color: var(--azul);
    line-height: 1.55;
    margin-bottom: 34px;
}

.included-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
}

.included-card {
    background: #fffdf8;
    border-radius: 22px;
    min-height: 132px;
    padding: 22px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(90, 60, 20, 0.08);
}

.included-emoji {
    font-size: 2rem;
    line-height: 1;
}

.included-text {
    font-weight: 900;
    color: var(--azul);
    font-size: 1.02rem;
    line-height: 1.25;
}

.note-card {
    margin-top: 22px;
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(18, 53, 91, 0.12);
    border-radius: 20px;
    padding: 20px;
    color: var(--azul);
    line-height: 1.55;
}

.how-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.how-card {
    background: #ffffff;
    border: 1px solid var(--borda);
    border-radius: 24px;
    padding: 24px;
    min-height: 210px;
    box-shadow: 0 10px 24px rgba(90, 60, 20, 0.07);
}

.how-emoji {
    font-size: 2rem;
    margin-bottom: 10px;
}

.how-title {
    font-size: 1.25rem;
    font-weight: 900;
    color: var(--azul);
    margin-bottom: 8px;
}

.how-text {
    line-height: 1.55;
    color: var(--texto);
}

.form-shell {
    max-width: 780px;
    margin: 0 auto;
    background: #ffffff;
    border: 1px solid var(--borda);
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 12px 30px rgba(90, 60, 20, 0.08);
}

.step-title {
    font-size: clamp(1.8rem, 4vw, 2.4rem);
    font-weight: 950;
    color: var(--azul);
    margin-bottom: 8px;
}

.step-subtitle {
    color: var(--muted);
    line-height: 1.55;
    margin-bottom: 22px;
}

.person-card {
    background: #fffaf0;
    border: 1px solid var(--borda);
    border-radius: 22px;
    padding: 22px;
    margin: 16px 0;
}

.person-title {
    font-size: 1.25rem;
    color: var(--azul);
    font-weight: 900;
    margin-bottom: 12px;
}

.payment-box {
    background: #fffdf8;
    border: 2px dashed #d8b981;
    border-radius: 22px;
    padding: 22px;
    margin: 18px 0;
}

.payment-box h3 {
    margin-top: 0;
    font-size: 1.35rem;
}

.pix-key {
    display: inline-block;
    background: var(--azul);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 14px;
    font-weight: 900;
    margin-top: 8px;
    word-break: break-all;
}

.center-btn {
    text-align: center;
    margin-top: 18px;
}

.footer-note {
    text-align: center;
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.7;
    padding: 28px 16px;
}

.footer-note strong {
    color: var(--azul);
}

@media (max-width: 800px) {
    .hero-grid {
        grid-template-columns: 1fr;
        gap: 26px;
    }

    .section {
        padding: 34px 16px;
    }

    .included-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .included-card {
        min-height: 118px;
        padding: 18px 10px;
    }

    .how-grid {
        grid-template-columns: 1fr;
    }

    .form-shell {
        border-radius: 24px;
        padding: 22px 16px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# SUPABASE
# =========================

@st.cache_resource
def get_supabase_client():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_KEY"])


supabase = get_supabase_client()


# =========================
# HELPERS
# =========================

def html(content: str):
    st.markdown(content.strip(), unsafe_allow_html=True)


def money(value: float) -> str:
    return f"R$ {value:.2f}".replace(".", ",")


def render_banner():
    banner_path = Path(__file__).parent / "banner_festa_julina.png"
    if not banner_path.exists():
        st.error("Banner não encontrado: banner_festa_julina.png")
        return

    encoded = base64.b64encode(banner_path.read_bytes()).decode("utf-8")
    html(f'<img class="hero-img" src="data:image/png;base64,{encoded}" alt="Festa Julina da Mary">')


def buscar_configuracao():
    return (
        supabase.table("configuracoes_evento")
        .select("*")
        .eq("id", 1)
        .single()
        .execute()
        .data
    )


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
        vagas_restantes = int(item["vagas_total"]) - ocupados.get(nome, 0)
        if vagas_restantes > 0:
            disponiveis.append({
                "nome": nome,
                "vagas_total": int(item["vagas_total"]),
                "vagas_restantes": vagas_restantes,
            })

    return disponiveis


def salvar_comprovante(arquivo, email):
    extensao = arquivo.name.split(".")[-1].lower()
    nome_seguro = email.replace("@", "_").replace(".", "_")
    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome_seguro}_{uuid4()}.{extensao}"

    supabase.storage.from_("comprovantes").upload(
        path=nome_arquivo,
        file=arquivo.getvalue(),
        file_options={"content-type": arquivo.type},
    )

    return nome_arquivo


def cadastrar_participantes_familia(
    responsavel_nome,
    email,
    whatsapp,
    adultos,
    criancas,
    cotas_por_adulto,
    itens_por_adulto,
    valor_total,
    comprovante_url,
):
    grupo_id = str(uuid4())

    familiares_payload = {
        "grupo_id": grupo_id,
        "responsavel": responsavel_nome,
        "adultos": adultos,
        "criancas": criancas,
        "cotas_por_adulto": cotas_por_adulto,
        "itens_por_adulto": itens_por_adulto,
    }

    registros = []
    for idx, adulto in enumerate(adultos):
        tipo_cota = cotas_por_adulto[idx]
        valor_cota = {"completa_50": 50.0, "reduzida_25": 25.0, "minima_5": 5.0}[tipo_cota]
        item = itens_por_adulto[idx] if tipo_cota in ["reduzida_25", "minima_5"] else None

        registros.append({
            "nome": adulto,
            "email": email.strip().lower(),
            "whatsapp": whatsapp.strip(),
            "tipo_cota": tipo_cota,
            "valor_cota": valor_cota,
            "item_levar": item,
            "status_pagamento": "aguardando_conferencia",
            "comprovante_url": comprovante_url,
            "qtd_adultos_pagantes": len(adultos),
            "qtd_criancas_ate_10": len(criancas),
            "familiares": json.dumps(familiares_payload, ensure_ascii=False),
            "valor_total": valor_total,
        })

    return supabase.table("participantes").insert(registros).execute().data


def get_item_meta(nome_item):
    mapa = {
        "3 refrigerantes de 2 litros": ("🥤", "Refrigerantes", "3 refrigerantes de 2 litros"),
        "Arroz doce": ("🍚", "Arroz doce", ""),
        "Bolo doce": ("🎂", "Bolo doce", ""),
        "Bolo salgado": ("🥧", "Bolo salgado", ""),
        "Doces diversos: abóbora, batata doce, cocada etc.": ("🍬", "Doces diversos", "abóbora, batata doce, cocada etc."),
        "Milho verde": ("🌽", "Milho verde", ""),
        "Paçoca": ("🥜", "Paçoca", ""),
        "Pipoca": ("🍿", "Pipoca", ""),
        "Sagu": ("🍮", "Sagu", ""),
    }
    return mapa.get(nome_item, ("🧺", nome_item, ""))


# =========================
# STATE
# =========================

if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = False

if "familia_confirmada" not in st.session_state:
    st.session_state.familia_confirmada = False

if "adultos_nomes" not in st.session_state:
    st.session_state.adultos_nomes = []

if "criancas_nomes" not in st.session_state:
    st.session_state.criancas_nomes = []


# =========================
# DADOS
# =========================

config = buscar_configuracao()
itens_disponiveis = buscar_itens_disponiveis()

total_50 = contar_participantes_por_cota("completa_50")
total_25 = contar_participantes_por_cota("reduzida_25")
total_5 = contar_participantes_por_cota("minima_5")

vagas_50 = max(int(config["limite_cota_50"]) - total_50, 0)
vagas_25 = max(int(config["limite_cota_25"]) - total_25, 0)
vagas_5 = max(5 - total_5, 0)


# =========================
# PAGE
# =========================

render_banner()

html("""
<section class="section section-white" id="inicio">
    <div class="section-inner hero-grid">
        <div>
            <div class="hero-title">A Festa Julina da Mary está chegando.</div>
            <div class="hero-text">
                Uma noite gostosa, divertida e bem organizada para reunir todo mundo.
                Quem participar já terá acesso às comidas principais, às brincadeiras,
                à estrutura preparada e a uma programação cheia de clima julino.
            </div>
            <a class="cta-link" href="#inscricao">Quero me inscrever</a>
        </div>
        <div class="info-card">
            <h2>Como funciona?</h2>
            <div class="info-line">
                Para facilitar a organização da festa, este ano a inscrição será feita antecipadamente.
                Assim conseguimos controlar melhor as comidas, bebidas, estrutura e os itens que cada pessoa vai levar.
            </div>
            <div class="info-line">🎟️ <strong>Cota R$50:</strong> esta cota é para quem não tem tempo. Com ela você não precisa levar nenhum prato.</div>
            <div class="info-line">🧺 <strong>Cota R$25:</strong> com esta cota, você ajuda na organização e leva um prato dentre as opções.</div>
            <div class="info-line">🤝 <strong>Cota R$5:</strong> cota solidária para quem está apertado. Você ajuda de forma simbólica e leva um prato dentre as opções.</div>
            <div class="info-line">A confirmação do pagamento será feita manualmente pela organização após a conferência do comprovante.</div>
        </div>
    </div>
</section>
""")

included = [
    ("🥟", "Bolinho caipira"),
    ("🥣", "Caldinhos"),
    ("🌭", "Cachorro-quente"),
    ("🥤", "Refrigerante"),
    ("🎤", "Karaokê"),
    ("📺", "Telão interativo"),
    ("🎯", "Bingo"),
    ("🔥", "Fogueira"),
    ("💋", "Barraca do beijo"),
    ("🎣", "Pescaria infantil"),
    ("💃", "Quadrilha"),
    ("🎊", "Decoração temática"),
]

cards = ""
for emoji, text in included:
    cards += f'<div class="included-card"><div class="included-emoji">{emoji}</div><div class="included-text">{text}</div></div>'

html(f"""
<section class="section section-yellow">
    <div class="section-inner">
        <div class="section-title">O que já está incluso para quem participar?</div>
        <div class="section-subtitle">
            A festa já está sendo preparada com comidas, estrutura e atrações para todo mundo aproveitar.
        </div>
        <div class="included-grid">{cards}</div>
        <div class="note-card">
            🍻 <strong>Bebidas alcoólicas:</strong> cada pessoa leva a sua, caso queira consumir.
            &nbsp;&nbsp;|&nbsp;&nbsp;
            🎁 <strong>Prendas para o bingo:</strong> quem quiser colaborar pode levar prendas extras à vontade.
        </div>
    </div>
</section>
""")

html("""
<section class="section section-white">
    <div class="section-inner">
        <div class="section-title">Como funciona?</div>
        <div class="section-subtitle">
            Escolha a forma de participação de cada adulto da família.
        </div>
        <div class="how-grid">
            <div class="how-card">
                <div class="how-emoji">🎟️</div>
                <div class="how-title">Cota R$50</div>
                <div class="how-text">Para quem quer participar sem precisar levar nenhum prato.</div>
            </div>
            <div class="how-card">
                <div class="how-emoji">🧺</div>
                <div class="how-title">Cota R$25</div>
                <div class="how-text">Você contribui com R$25 e escolhe um item para levar.</div>
            </div>
            <div class="how-card">
                <div class="how-emoji">🤝</div>
                <div class="how-title">Cota R$5</div>
                <div class="how-text">Cota solidária para quem está apertado. Também escolhe um item para levar.</div>
            </div>
        </div>
    </div>
</section>
""")


# =========================
# FORMULÁRIO
# =========================

html('<section class="section section-cream" id="inscricao"><div class="section-inner"><div class="form-shell">')
st.markdown('<div class="step-title">Inscreva sua família</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="step-subtitle">Primeiro preencha os dados do responsável e informe quem vai participar. Crianças até 10 anos não pagam.</div>',
    unsafe_allow_html=True,
)

responsavel_nome = st.text_input("Nome completo do responsável", key="responsavel_nome")

col1, col2 = st.columns(2)
with col1:
    email = st.text_input("E-mail", key="email")
with col2:
    whatsapp = st.text_input("WhatsApp", key="whatsapp")

col3, col4 = st.columns(2)
with col3:
    qtd_adultos = st.number_input("Adultos pagantes", min_value=1, max_value=12, value=1, step=1)
with col4:
    qtd_criancas = st.number_input("Crianças até 10 anos", min_value=0, max_value=12, value=0, step=1)

st.markdown("#### Nomes dos adultos")
adultos_nomes = []
for i in range(int(qtd_adultos)):
    default = responsavel_nome if i == 0 else ""
    adultos_nomes.append(st.text_input(f"Adulto {i + 1}", value=default, key=f"adulto_nome_{i}"))

criancas_nomes = []
if int(qtd_criancas) > 0:
    st.markdown("#### Nomes das crianças")
    for i in range(int(qtd_criancas)):
        criancas_nomes.append(st.text_input(f"Criança {i + 1}", key=f"crianca_nome_{i}"))

if st.button("Confirmar participantes", use_container_width=True):
    adultos_ok = all(nome.strip() for nome in adultos_nomes)
    criancas_ok = all(nome.strip() for nome in criancas_nomes)

    if not responsavel_nome or not email or not whatsapp:
        st.error("Preencha nome, e-mail e WhatsApp do responsável.")
    elif not adultos_ok:
        st.error("Preencha o nome de todos os adultos pagantes.")
    elif not criancas_ok:
        st.error("Preencha o nome de todas as crianças informadas.")
    else:
        st.session_state.familia_confirmada = True
        st.session_state.adultos_nomes = [nome.strip() for nome in adultos_nomes]
        st.session_state.criancas_nomes = [nome.strip() for nome in criancas_nomes]
        st.rerun()

if st.session_state.familia_confirmada:
    adultos = st.session_state.adultos_nomes
    criancas = st.session_state.criancas_nomes

    st.divider()
    st.markdown('<div class="step-title">Escolha as cotas dos adultos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="step-subtitle">Cada adulto deve escolher uma cota. Quem escolher R$25 ou R$5 também escolhe um item para levar.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="payment-box">
            <strong>Cotas disponíveis:</strong><br>
            🎟️ R$50: {vagas_50} vaga(s) &nbsp; | &nbsp;
            🧺 R$25: {vagas_25} vaga(s) &nbsp; | &nbsp;
            🤝 R$5: {vagas_5} vaga(s) simbólica(s)
        </div>
        """,
        unsafe_allow_html=True,
    )

    cotas_por_adulto = []
    itens_por_adulto = []
    valor_total = 0.0
    formulario_cotas_ok = True

    item_options = [""] + [item["nome"] for item in itens_disponiveis]

    for idx, adulto in enumerate(adultos):
        st.markdown(f'<div class="person-card"><div class="person-title">{adulto}</div>', unsafe_allow_html=True)

        cota_label = st.radio(
            "Escolha a cota",
            ["🎟️ Cota R$50", "🧺 Cota R$25", "🤝 Cota R$5"],
            horizontal=True,
            key=f"cota_adulto_{idx}",
        )

        if "R$50" in cota_label:
            tipo = "completa_50"
            valor_total += 50.0
            item = None
        elif "R$25" in cota_label:
            tipo = "reduzida_25"
            valor_total += 25.0
            item = st.selectbox("Item que vai levar", item_options, key=f"item_adulto_{idx}")
            if not item:
                formulario_cotas_ok = False
        else:
            tipo = "minima_5"
            valor_total += 5.0
            item = st.selectbox("Item que vai levar", item_options, key=f"item_adulto_{idx}")
            if not item:
                formulario_cotas_ok = False

        cotas_por_adulto.append(tipo)
        itens_por_adulto.append(item)

        st.markdown("</div>", unsafe_allow_html=True)

    resumo_itens = "".join(
        f"<li>{adultos[i]}: {itens_por_adulto[i] or 'não precisa levar item'}</li>"
        for i in range(len(adultos))
    )

    st.markdown(
        f"""
        <div class="payment-box">
            <h3>Resumo da inscrição</h3>
            <strong>Responsável:</strong> {responsavel_nome}<br>
            <strong>Adultos pagantes:</strong> {len(adultos)}<br>
            <strong>Crianças até 10 anos:</strong> {len(criancas)}<br>
            <strong>Total do Pix:</strong> {money(valor_total)}<br>
            <br>
            <strong>Itens:</strong>
            <ul>{resumo_itens}</ul>
        </div>
        <div class="payment-box">
            <h3>Dados do Recebedor</h3>
            <strong>Copie o código Pix abaixo:</strong><br>
            <div class="pix-key">{config["chave_pix"]}</div>
        </div>
        <div class="payment-box">
            <h3>Anexo do Comprovante</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    comprovante = st.file_uploader(
        "Anexe o comprovante do Pix",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    col_confirm_1, col_confirm_2, col_confirm_3 = st.columns([1, 1, 1])
    with col_confirm_2:
        if st.button("Confirmar inscrição", use_container_width=True):
            if not formulario_cotas_ok:
                st.error("Escolha o item de todos os adultos que selecionaram cota R$25 ou R$5.")
            elif not comprovante:
                st.error("Anexe o comprovante do Pix.")
            else:
                try:
                    comprovante_url = salvar_comprovante(comprovante, email)

                    cadastrar_participantes_familia(
                        responsavel_nome=responsavel_nome,
                        email=email,
                        whatsapp=whatsapp,
                        adultos=adultos,
                        criancas=criancas,
                        cotas_por_adulto=cotas_por_adulto,
                        itens_por_adulto=itens_por_adulto,
                        valor_total=valor_total,
                        comprovante_url=comprovante_url,
                    )

                    st.success("Inscrição enviada com sucesso! O pagamento ficará aguardando conferência da organização.")

                    st.session_state.familia_confirmada = False
                    st.session_state.mostrar_formulario = False
                    st.session_state.adultos_nomes = []
                    st.session_state.criancas_nomes = []
                    st.rerun()

                except Exception as erro:
                    st.error("Não foi possível salvar sua inscrição.")
                    st.exception(erro)

html("</div></div></section>")


# =========================
# FOOTER
# =========================

html("""
<div class="footer-note">
    Festa Julina da Mary • Organização das inscrições e contribuições<br>
    <strong>Desenvolvimento by Levz</strong>
</div>
""")
