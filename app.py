
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo
import base64
import json
import re
import unicodedata

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
    --azul: #111111;
    --azul-2: #222222;
    --laranja: #df7f00;
    --laranja-2: #bf6900;
    --amarelo: #f8c94a;
    --fundo: #fff5e6;
    --creme: #fffaf0;
    --borda: #efd3a1;
    --texto: #111827;
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

/* Selectbox claro e legível */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #d9c29b !important;
    border-radius: 14px !important;
    min-height: 44px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #1f2937 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    background: #ffffff !important;
    color: #1f2937 !important;
}

ul[role="listbox"] {
    background: #ffffff !important;
    color: #1f2937 !important;
}

li[role="option"] {
    background: #ffffff !important;
    color: #1f2937 !important;
}

li[role="option"]:hover,
li[aria-selected="true"] {
    background: #fff0d4 !important;
    color: #12355b !important;
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

.banner-wrap {
    width: calc(100% - 72px);
    max-width: 1760px;
    margin: 0 auto;
    padding: 0;
}

.hero-img {
    width: 100%;
    display: block;
    object-fit: cover;
    border-radius: 0 0 18px 18px;
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
    max-width: 1120px;
    margin: 0 auto;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 44px;
    align-items: center;
}

.hero-single {
    max-width: 900px;
    text-align: left;
}

.hero-single .hero-title {
    max-width: 820px;
}

.hero-single .hero-text {
    max-width: 760px;
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

.form-intro {
    max-width: 760px;
    margin: 0 auto 30px auto;
}

.form-heading {
    max-width: 780px;
    margin: 0 auto 28px auto;
    text-align: center;
}

.form-heading .step-title {
    font-size: clamp(2.1rem, 6vw, 3.4rem);
}

.form-heading .step-subtitle {
    font-size: clamp(1rem, 3vw, 1.18rem);
}

div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p {
    font-size: 1.06rem !important;
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


/* Formulário mais confortável */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stFileUploader label {
    font-size: 1.05rem !important;
}

div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p {
    font-size: 1.12rem !important;
}

button[data-testid="stBaseButton-secondary"],
.stButton > button {
    font-size: 1rem !important;
}

.success-card {
    max-width: 720px;
    margin: 42px auto;
    background: #ffffff;
    border: 1px solid #efd3a1;
    border-radius: 26px;
    padding: 32px;
    text-align: center;
    box-shadow: 0 12px 28px rgba(90, 60, 20, 0.08);
}

.success-card h2 {
    font-size: clamp(2rem, 5vw, 3rem);
    margin: 0 0 12px 0;
}

.success-card p {
    font-size: 1.15rem;
    line-height: 1.6;
}



/* Ajustes finais de formulário e componentes */
.form-compact {
    max-width: 560px;
    margin: 0 auto;
}
.form-compact .step-title {
    text-align: center;
}
.form-compact .step-subtitle {
    text-align: center;
    margin-bottom: 14px;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border: 0 !important;
    box-shadow: 0 0 0 1px rgba(17,24,39,0.18) !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    box-shadow: 0 0 0 2px var(--laranja) !important;
    border: 0 !important;
}

input:focus,
textarea:focus {
    outline: none !important;
    box-shadow: none !important;
    background: #ffffff !important;
}

input::selection,
textarea::selection {
    background: #ffe4b8 !important;
    color: #111827 !important;
}

/* Number input: menos preto, mais laranja */
button[aria-label="Decrement"],
button[aria-label="Increment"] {
    background: #111827 !important;
    color: #ffffff !important;
    border: 0 !important;
}
button[aria-label="Increment"] {
    background: var(--laranja) !important;
}

/* Radio: bolinhas não selecionadas brancas */
div[data-testid="stRadio"] [role="radio"] > div:first-child {
    background: #ffffff !important;
    border: 2px solid #111827 !important;
}
div[data-testid="stRadio"] [aria-checked="true"] > div:first-child {
    background: #ff4b4b !important;
    border: 2px solid #ff4b4b !important;
}

.success-card {
    background: #ffffff !important;
    border: 1px solid var(--borda) !important;
}

.upload-note {
    font-size: 0.95rem;
    color: var(--muted);
    margin-bottom: 10px;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    white-space: nowrap !important;
}



/* Correções finais de formulário */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border: 0 !important;
    box-shadow: none !important;
    background: #ffffff !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    border: 0 !important;
    box-shadow: 0 0 0 1px #df7f00 !important;
    background: #ffffff !important;
}

div[data-baseweb="input"] input,
textarea,
input {
    color: #111111 !important;
    background: #ffffff !important;
    caret-color: #df7f00 !important;
    box-shadow: none !important;
    outline: none !important;
    -webkit-text-fill-color: #111111 !important;
}

input::selection,
textarea::selection {
    background: #ffe4b8 !important;
    color: #111111 !important;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill,
textarea:-webkit-autofill:hover,
textarea:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px #ffffff inset !important;
    -webkit-text-fill-color: #111111 !important;
    transition: background-color 9999s ease-in-out 0s !important;
}

/* Number input: preto e laranja, sem vermelho */
button[data-testid="stNumberInputStepDown"],
button[aria-label="Decrement"],
button[title="Decrease value"] {
    background: #111111 !important;
    color: #ffffff !important;
    border: 0 !important;
}
button[data-testid="stNumberInputStepUp"],
button[aria-label="Increment"],
button[title="Increase value"] {
    background: #df7f00 !important;
    color: #ffffff !important;
    border: 0 !important;
}
button[data-testid="stNumberInputStepDown"] *,
button[data-testid="stNumberInputStepUp"] *,
button[aria-label="Decrement"] *,
button[aria-label="Increment"] * {
    color: #ffffff !important;
}

/* Radio: branco quando não selecionado, laranja quando selecionado */
div[data-testid="stRadio"] [role="radio"] > div:first-child {
    background: #ffffff !important;
    border: 2px solid #111111 !important;
    box-shadow: none !important;
}
div[data-testid="stRadio"] [role="radio"][aria-checked="true"] > div:first-child,
div[data-testid="stRadio"] [aria-checked="true"] > div:first-child {
    background: #df7f00 !important;
    border: 2px solid #df7f00 !important;
    box-shadow: inset 0 0 0 3px #ffffff !important;
}
div[data-testid="stRadio"] svg {
    color: #df7f00 !important;
    fill: #df7f00 !important;
}

/* Upload: esconder texto interno padrão do Streamlit */
[data-testid="stFileUploaderDropzoneInstructions"],
section[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploaderDropzone"] [data-testid="stMarkdownContainer"]:has(small) {
    display: none !important;
}
section[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #d8b981 !important;
    border-radius: 18px !important;
    padding: 14px !important;
}

.upload-card {
    background: #ffffff;
    border: 2px dashed #d8b981;
    border-radius: 22px;
    padding: 22px;
    margin: 18px 0;
}
.upload-title {
    color: #111111;
    font-size: 1.35rem;
    font-weight: 900;
    margin-bottom: 8px;
}

.payment-box h3,
.payment-box strong,
.person-title,
.step-title,
.section-title,
.included-text,
.how-title {
    color: #111111 !important;
}

.btn-center-narrow {
    max-width: 260px;
    margin: 18px auto 0 auto;
}

.open-notes {
    margin-top: 26px;
    text-align: center;
    color: #ffffff !important;
    font-size: clamp(1.05rem, 2.8vw, 1.35rem);
    line-height: 1.55;
    font-weight: 900;
    text-shadow: 0 2px 10px rgba(0,0,0,0.18);
}
.open-notes strong { color: #ffffff !important; }
.closed-card {
    max-width: 760px;
    margin: 42px auto;
    background: #ffffff;
    border: 1px solid #efd3a1;
    border-radius: 26px;
    padding: 34px;
    text-align: center;
    box-shadow: 0 12px 28px rgba(90, 60, 20, 0.08);
}
.closed-card h2 {
    color: #111111 !important;
    font-size: clamp(2rem, 5vw, 3.2rem);
    margin: 0 0 14px 0;
}
.closed-card p {
    font-size: 1.15rem;
    line-height: 1.65;
    color: #111111 !important;
}

@media (max-width: 800px) {
    .banner-wrap {
        width: 100%;
        max-width: 100%;
    }
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

    .form-shell,
    .form-intro {
        border-radius: 24px;
        padding: 22px 16px;
    }

    .hero-single {
        text-align: left;
    }
}


/* Ajustes v12: menos briga com componentes nativos */
.form-compact { max-width: 720px; margin: 0 auto; }
.form-compact .step-title, .step-title { font-size: 2.15rem !important; }
.form-compact .step-subtitle, .step-subtitle { font-size: 1.05rem !important; }

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    border: 0 !important;
    box-shadow: 0 0 0 2px rgba(223, 127, 0, 0.28) !important;
    outline: none !important;
}

input:focus, textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Selectbox claro: substitui radios e evita bolinhas azul/vermelho */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111111 !important;
    border-radius: 14px !important;
    min-height: 48px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #111111 !important;
}

div[data-baseweb="select"] svg {
    color: var(--laranja) !important;
    fill: var(--laranja) !important;
}

div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    background: #ffffff !important;
    color: #111111 !important;
}

/* Esconde texto padrão do uploader quando possível */
section[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"],
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] * {
    display: none !important;
}

/* Quadrante nativo para anexo */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px dashed #d8b981 !important;
    border-radius: 18px !important;
    background: #ffffff !important;
    padding: 1.2rem !important;
}

/* Botões sem quebra de texto */
.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    white-space: nowrap !important;
    min-width: 180px !important;
}

.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    white-space: nowrap !important;
}

/* Upload dentro do bloco */
.upload-inline-title {
    font-size: 1.35rem;
    font-weight: 850;
    color: #111111;
    margin-bottom: 0.35rem;
}
.upload-inline-note {
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 0.9rem;
}


/* Ajustes v13 - alinhamento e componentes mais estáveis */
.form-compact {
    max-width: 760px !important;
}

/* Campos do formulário com altura consistente */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border: 1px solid #d8b981 !important;
    background: #ffffff !important;
    min-height: 48px !important;
}

/* Selectboxes: fundo claro, texto preto, seta laranja */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}
div[data-baseweb="select"] svg {
    fill: var(--laranja) !important;
    color: var(--laranja) !important;
}

/* Evita que os rótulos dos selects quebrem desnecessariamente */
.stSelectbox label p {
    white-space: nowrap !important;
    font-size: 0.98rem !important;
}

/* Botões centralizados e sem quebra de texto */
.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    min-width: 190px !important;
    width: 100% !important;
    line-height: 1 !important;
}
.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    white-space: nowrap !important;
    margin: 0 !important;
    line-height: 1 !important;
}

/* Um único quadrante para o comprovante */
.upload-box {
    background: #ffffff;
    border: 1px dashed #d8b981;
    border-radius: 22px;
    padding: 24px;
    margin: 20px 0 18px 0;
}
.upload-box-title {
    font-size: 1.45rem;
    font-weight: 900;
    color: #111111;
    margin-bottom: 6px;
}
.upload-box-note {
    font-size: 0.98rem;
    color: #64748b;
    margin-bottom: 14px;
}

/* Dentro do quadrante, o uploader não cria outro quadrante */
section[data-testid="stFileUploaderDropzone"] {
    border: 0 !important;
    background: transparent !important;
    padding: 0 !important;
    min-height: auto !important;
}
section[data-testid="stFileUploaderDropzone"] > div {
    padding: 0 !important;
}

/* Esconde textos padrão do uploader que conflitam com a instrução personalizada */
section[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"],
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] *,
section[data-testid="stFileUploaderDropzone"] div:has(> small) {
    display: none !important;
}

/* Arquivo anexado: claro e legível */
div[data-testid="stFileUploaderFile"],
div[data-testid="stFileUploaderFile"] * {
    background: #fffaf0 !important;
    color: #111111 !important;
}
div[data-testid="stFileUploaderFile"] {
    border: 1px solid #efd3a1 !important;
    border-radius: 12px !important;
}



/* v14: layout mobile-first mais estável */
.form-compact {
    max-width: 720px !important;
    margin: 0 auto !important;
    text-align: center !important;
}
.form-compact .step-title {
    font-size: clamp(2rem, 5vw, 4rem) !important;
    font-weight: 950 !important;
    letter-spacing: -0.035em !important;
    line-height: 1.05 !important;
    margin-bottom: 12px !important;
}
.form-compact .step-subtitle {
    font-size: 1.15rem !important;
    line-height: 1.55 !important;
    margin-bottom: 0 !important;
}
.form-area-spacer { height: 8px; }

.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    width: 100% !important;
    min-width: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
}
.stButton > button p,
button[kind="secondary"] p,
button[kind="primary"] p {
    white-space: nowrap !important;
    color: #ffffff !important;
}

.upload-native-block {
    background: transparent;
    margin-top: 20px;
    margin-bottom: 10px;
}
.upload-native-title {
    font-size: 1.75rem;
    font-weight: 950;
    color: #111111;
    margin-bottom: 6px;
}
.upload-native-note {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 10px;
}
section[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #d8b981 !important;
    border-radius: 18px !important;
    padding: 16px !important;
}
section[data-testid="stFileUploaderDropzone"] > div {
    padding: 0 !important;
}
section[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"],
section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] * {
    display: none !important;
}
div[data-testid="stFileUploaderFile"],
div[data-testid="stFileUploaderFile"] * {
    background: #fffaf0 !important;
    color: #111111 !important;
}
div[data-testid="stFileUploaderFile"] {
    border: 1px solid #efd3a1 !important;
    border-radius: 12px !important;
}

/* v17 overrides */
.open-notes {
    color: #111111 !important;
    text-shadow: none !important;
}
.open-notes strong {
    color: #111111 !important;
}
.form-compact .step-title {
    color: #111111 !important;
}
.form-compact .step-subtitle {
    color: #4b5563 !important;
}
.stSelectbox label p {
    white-space: normal !important;
    line-height: 1.2 !important;
    font-size: 0.94rem !important;
}
@media (min-width: 600px) {
    .stSelectbox label p {
        white-space: nowrap !important;
    }
}

/* v18 label spacing */
.form-compact { max-width: 860px !important; }
.stSelectbox label p {
    white-space: normal !important;
    overflow-wrap: normal !important;
    word-break: normal !important;
    line-height: 1.25 !important;
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


def normalizar_whatsapp(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def formatar_whatsapp(valor: str) -> str:
    digitos = normalizar_whatsapp(valor)
    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    return valor.strip()


def formatar_whatsapp_state():
    valor = st.session_state.get("whatsapp", "")
    formatado = formatar_whatsapp(valor)
    if formatado != valor:
        st.session_state["whatsapp"] = formatado


def email_valido(valor: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", (valor or "").strip()))


def whatsapp_valido(valor: str) -> bool:
    return len(normalizar_whatsapp(valor)) in (10, 11)


def email_ou_whatsapp_ja_cadastrado(email: str, whatsapp: str) -> tuple[bool, str]:
    email_normalizado = email.strip().lower()
    whatsapp_formatado = formatar_whatsapp(whatsapp)
    whatsapp_digits = normalizar_whatsapp(whatsapp)

    por_email = (
        supabase.table("participantes")
        .select("id")
        .eq("email", email_normalizado)
        .limit(1)
        .execute()
        .data
    )
    if por_email:
        return True, "Este e-mail já foi usado em uma inscrição."

    candidatos = [whatsapp_formatado, whatsapp.strip(), whatsapp_digits]
    for telefone in set(filter(None, candidatos)):
        por_whatsapp = (
            supabase.table("participantes")
            .select("id")
            .eq("whatsapp", telefone)
            .limit(1)
            .execute()
            .data
        )
        if por_whatsapp:
            return True, "Este WhatsApp já foi usado em uma inscrição."

    return False, ""


def render_banner():
    banner_path = Path(__file__).parent / "banner_festa_julina.png"
    if not banner_path.exists():
        st.error("Banner não encontrado: banner_festa_julina.png")
        return

    encoded = base64.b64encode(banner_path.read_bytes()).decode("utf-8")
    html(f'<div class="banner-wrap"><img class="hero-img" src="data:image/png;base64,{encoded}" alt="Festa Julina da Mary"></div>')


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


def gerar_nome_seguro_arquivo(email, extensao):
    base_email = email.strip().lower()
    base_email = unicodedata.normalize("NFKD", base_email).encode("ascii", "ignore").decode("ascii")
    base_email = re.sub(r"[^a-z0-9]+", "_", base_email)
    base_email = base_email.strip("_") or "participante"

    extensao = unicodedata.normalize("NFKD", extensao.lower()).encode("ascii", "ignore").decode("ascii")
    extensao = re.sub(r"[^a-z0-9]", "", extensao) or "png"

    return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base_email}_{uuid4().hex}.{extensao}"


def salvar_comprovante(arquivo, email):
    extensao = arquivo.name.split(".")[-1].lower()
    nome_arquivo = gerar_nome_seguro_arquivo(email, extensao)

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
        valor_cota = {"completa_35": 35.0, "reduzida_10": 10.0}[tipo_cota]
        item = itens_por_adulto[idx] if tipo_cota == "reduzida_10" else None

        registros.append({
            "nome": adulto,
            "email": email.strip().lower(),
            "whatsapp": formatar_whatsapp(whatsapp),
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
        "milho cozido (10 unidades)": ("🌽", "Milho cozido", "10 unidades"),
        "cachorro quente (30 unidades)": ("🌭", "Cachorro quente", "30 unidades"),
        "caldo verde (2 litros)": ("🥣", "Caldo verde", "2 litros"),
        "caldinho de feijão (2 litros)": ("🥣", "Caldinho de feijão", "2 litros"),
        "caldinho de mandioquinha (2 litros)": ("🥣", "Caldinho de mandioquinha", "2 litros"),
        "caldinho de mandioca (2 litros)": ("🥣", "Caldinho de mandioca", "2 litros"),
        "cuscuz (25 pedaços)": ("🍲", "Cuscuz", "25 pedaços"),
        "bolinho caipira (20 unidades)": ("🥟", "Bolinho caipira", "20 unidades"),
        "pastelzinho (25 unidades)": ("🥟", "Pastelzinho", "25 unidades"),
        "bolinha de queijo (25 unidades)": ("🧀", "Bolinha de queijo", "25 unidades"),
        "coxinha (25 unidades)": ("🍗", "Coxinha", "25 unidades"),
        "kibe (25 unidades)": ("🥙", "Kibe", "25 unidades"),
        "amendoim (50 saquinhos)": ("🥜", "Amendoim", "50 saquinhos"),
        "canjica (2 litros)": ("🌽", "Canjica", "2 litros"),
        "arroz doce (2 litros)": ("🍚", "Arroz doce", "2 litros"),
        "bolo de chocolate (20 pedaços)": ("🍫", "Bolo de chocolate", "20 pedaços"),
        "bolo de milho (20 pedaços)": ("🌽", "Bolo de milho", "20 pedaços"),
        "bolo de cenoura (20 pedaços)": ("🥕", "Bolo de cenoura", "20 pedaços"),
        "bolo de fubá (20 pedaços)": ("🍰", "Bolo de fubá", "20 pedaços"),
        "pé de moleque (50 unidades)": ("🥜", "Pé de moleque", "50 unidades"),
        "paçoquinha (50 unidades)": ("🥜", "Paçoquinha", "50 unidades"),
        "cocada (20 unidades)": ("🥥", "Cocada", "20 unidades"),
        "doce de abóbora (20 unidades)": ("🎃", "Doce de abóbora", "20 unidades"),
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

if "inscricao_concluida" not in st.session_state:
    st.session_state.inscricao_concluida = False


# =========================
# DADOS
# =========================

config = buscar_configuracao()
itens_disponiveis = buscar_itens_disponiveis()

LIMITE_COTA_35 = 52
LIMITE_COTA_10 = 52

total_35 = contar_participantes_por_cota("completa_35")
total_10 = contar_participantes_por_cota("reduzida_10")


# =========================
# PAGE
# =========================

render_banner()

INSCRICOES_ENCERRAM = datetime(2026, 7, 6, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))
agora_sp = datetime.now(ZoneInfo("America/Sao_Paulo"))
inscricoes_encerradas = agora_sp >= INSCRICOES_ENCERRAM

if inscricoes_encerradas and not st.session_state.inscricao_concluida:
    html("""
    <section class="section section-cream">
        <div class="closed-card">
            <h2>Inscrições encerradas</h2>
            <p>
                Que pena, o prazo para se inscrever terminou em 5 de julho.<br>
                Agora a organização precisa fechar as compras, quantidades e estrutura da festa.<br>
                Obrigada pela compreensão 🌽🔥
            </p>
        </div>
    </section>
    """)
    html("""
    <div class="footer-note">
        Festa Julina da Mary • Organização das inscrições e contribuições<br>
        <strong>Desenvolvimento by Levz</strong>
    </div>
    """)
    st.stop()

if st.session_state.inscricao_concluida:
    html('''
    <section class="section section-cream">
        <div class="success-card">
            <h2>Inscrição enviada com sucesso! 🎉</h2>
            <p>
                Nós já recebemos sua inscrição e o comprovante.<br>
                O pagamento ficará aguardando conferência da organização.<br>
                Nos vemos dia 18 de julho a partir das 19h 🌽🔥🍰
            </p>
        </div>
    </section>
    ''')
    btn_s1, btn_s2, btn_s3 = st.columns([1, 1.1, 1])
    with btn_s2:
        if st.button("Voltar", use_container_width=True):
            st.session_state.inscricao_concluida = False
            st.session_state.familia_confirmada = False
            st.session_state.adultos_nomes = []
            st.session_state.criancas_nomes = []
            st.rerun()
    html("""
    <div class="footer-note">
        Festa Julina da Mary • Organização das inscrições e contribuições<br>
        <strong>Desenvolvimento by Levz</strong>
    </div>
    """)
    st.stop()

html("""
<section class="section section-white" id="inicio">
    <div class="section-inner hero-single">
        <div class="hero-title">A Festa Julina da Mary está chegando.</div>
        <div class="hero-text">
            Uma noite gostosa, divertida e bem organizada para reunir todo mundo.
            Quem participar já terá acesso às comidas principais, às brincadeiras,
            à estrutura preparada e a uma programação cheia de clima julino.<br><br>
            <strong>Vagas limitadas, se inscreva até 5 de julho.</strong>
        </div>
        <a class="cta-link" href="#inscricao">Quero me inscrever</a>
    </div>
</section>
""")

included = [
    ("🥟", "Bolinho caipira"),
    ("🥣", "Caldinhos"),
    ("🌭", "Cachorro-quente"),
    ("🍽️", "Estrutura e descartáveis"),
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
        <div class="open-notes">
            🥤 <strong>Bebidas:</strong> Cada pessoa leva o que quiser beber. Para garantir sua bebida geladinha a noite toda, leve seu cooler!<br>
            🎁 <strong>Bingo:</strong> leve prendas para o bingo e deixe a brincadeira ainda mais divertida!
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
        <div class="how-grid" style="grid-template-columns: repeat(2, 1fr);">
            <div class="how-card">
                <div class="how-emoji">🎟️</div>
                <div class="how-title">Cota R$35</div>
                <div class="how-text">Cada pessoa contribui com R$35 e não precisa levar nada.</div>
            </div>
            <div class="how-card">
                <div class="how-emoji">🧺</div>
                <div class="how-title">Cota R$10</div>
                <div class="how-text">Cada pessoa contribui com R$10 e escolhe um item da lista para levar.</div>
            </div>
        </div>
    </div>
</section>
""")


# =========================
# FORMULÁRIO
# =========================

html('''
<section class="section section-cream" id="inscricao">
    <div class="section-inner">
        <div class="form-compact">
            <div class="step-title">Inscreva o seu grupo</div>
            <div class="step-subtitle">
                Preencha com seus dados e informe quem mais da sua família/amigos vai participar.<br>
                Crianças até 10 anos não pagam.
            </div>
        </div>
    </div>
</section>
''')

form_col_left, form_col, form_col_right = st.columns([1.35, 1.5, 1.35])

with form_col:
    responsavel_nome = st.text_input("Nome completo do responsável", key="responsavel_nome")

    email = st.text_input("E-mail", key="email", placeholder="seu@email.com")
    whatsapp = st.text_input("WhatsApp", key="whatsapp", placeholder="(12) 98888-7777", on_change=formatar_whatsapp_state)
    whatsapp = formatar_whatsapp(whatsapp)

    col3, col4 = st.columns([1.35, 1.0], gap="large")
    with col3:
        qtd_outros_adultos = st.selectbox(
            "Outros adultos além de você",
            options=list(range(13)),
            index=0,
            key="qtd_outros_adultos",
        )
    with col4:
        qtd_criancas = st.selectbox(
            "Crianças até 10 anos",
            options=list(range(13)),
            index=0,
            key="qtd_criancas",
        )

    adultos_nomes = [responsavel_nome.strip()] if responsavel_nome.strip() else [""]
    if int(qtd_outros_adultos) > 0:
        st.markdown("#### Nomes dos outros adultos")
        for i in range(int(qtd_outros_adultos)):
            adultos_nomes.append(st.text_input(f"Adulto adicional {i + 1}", key=f"adulto_nome_{i}"))

    criancas_nomes = []
    if int(qtd_criancas) > 0:
        st.markdown("#### Nomes das crianças")
        for i in range(int(qtd_criancas)):
            criancas_nomes.append(st.text_input(f"Criança {i + 1}", key=f"crianca_nome_{i}"))

    confirmar_participantes = st.button("Confirmar", use_container_width=True)

    if confirmar_participantes:
        adultos_ok = all(nome.strip() for nome in adultos_nomes)
        criancas_ok = all(nome.strip() for nome in criancas_nomes)

        if not responsavel_nome or not email or not whatsapp:
            st.error("Preencha nome, e-mail e WhatsApp do responsável.")
        elif not email_valido(email):
            st.error("Informe um e-mail válido, com @ e domínio. Exemplo: nome@email.com")
        elif not whatsapp_valido(whatsapp):
            st.error("Informe um WhatsApp válido com DDD. Exemplo: (12) 98888-7777")
        elif not adultos_ok:
            st.error("Preencha o nome do responsável e de todos os adultos adicionais.")
        elif not criancas_ok:
            st.error("Preencha o nome de todas as crianças informadas.")
        else:
            duplicado, mensagem_duplicidade = email_ou_whatsapp_ja_cadastrado(email, whatsapp)
            if duplicado:
                st.error(mensagem_duplicidade)
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
            '<div class="step-subtitle">Cada adulto deve escolher uma cota. Quem escolher R$10 também escolhe um item para levar.</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'''
            <div class="payment-box">
                <strong>Cotas já escolhidas até agora:</strong><br>
                🎟️ R$35: {total_35}/{LIMITE_COTA_35} cota(s) &nbsp; | &nbsp;
                🧺 R$10 + item: {total_10}/{LIMITE_COTA_10} cota(s)
            </div>
            ''',
            unsafe_allow_html=True,
        )

        cotas_por_adulto = []
        itens_por_adulto = []
        valor_total = 0.0
        formulario_cotas_ok = True

        item_placeholder = "Selecione o item que vai levar"
        item_options = [item_placeholder] + [item["nome"] for item in itens_disponiveis]

        cota_options = [
            "🎟️ Cota R$35 - não preciso levar nada",
            "🧺 Cota R$10 - levo um item",
        ]

        for idx, adulto in enumerate(adultos):
            st.markdown(f'<div class="person-card"><div class="person-title">{adulto}</div>', unsafe_allow_html=True)

            cota_label = st.selectbox(
                f"Escolha a cota de {adulto}",
                cota_options,
                key=f"cota_adulto_{idx}",
            )

            if "R$35" in cota_label:
                tipo = "completa_35"
                valor_total += 35.0
                item = None
            else:
                tipo = "reduzida_10"
                valor_total += 10.0
                item = st.selectbox(
                    f"Item que {adulto} vai levar",
                    item_options,
                    key=f"item_adulto_{idx}",
                )
                if item == item_placeholder:
                    formulario_cotas_ok = False
                    item = None

            cotas_por_adulto.append(tipo)
            itens_por_adulto.append(item)

            st.markdown("</div>", unsafe_allow_html=True)

        resumo_itens = "".join(
            f"<li>{adultos[i]}: {itens_por_adulto[i] or 'não precisa levar item'}</li>"
            for i in range(len(adultos))
        )

        st.markdown(
            f'''
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
            ''',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="upload-native-block">'
            '<div class="upload-native-title">Anexo do Comprovante</div>'
            '<div class="upload-native-note">Máximo de 200KB • PNG, JPG, PDF</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        comprovante = st.file_uploader(
            "Comprovante do Pix",
            type=["png", "jpg", "jpeg", "pdf"],
            label_visibility="collapsed",
        )
        if comprovante:
            tamanho_kb = comprovante.size / 1024
            if comprovante.size <= 200 * 1024:
                st.success(f"Comprovante anexado: {comprovante.name} ({tamanho_kb:.0f}KB)")
            else:
                st.error(f"Arquivo anexado: {comprovante.name} ({tamanho_kb:.0f}KB). O limite é 200KB.")

        confirmar_inscricao = st.button("Confirmar inscrição", use_container_width=True)

        if confirmar_inscricao:
            from collections import Counter

            selecionadas_35 = sum(1 for c in cotas_por_adulto if c == "completa_35")
            selecionadas_10 = sum(1 for c in cotas_por_adulto if c == "reduzida_10")

            vagas_item_por_nome = {item["nome"]: int(item.get("vagas_restantes") or 0) for item in itens_disponiveis}
            itens_selecionados = [item for item in itens_por_adulto if item]
            itens_excedidos = [
                nome_item
                for nome_item, qtd in Counter(itens_selecionados).items()
                if qtd > vagas_item_por_nome.get(nome_item, 0)
            ]

            if not formulario_cotas_ok:
                st.error("Escolha o item de todos os adultos que selecionaram cota R$10.")
            elif total_35 + selecionadas_35 > LIMITE_COTA_35:
                st.error("Não há cotas R$35 suficientes disponíveis para todos os adultos selecionados.")
            elif total_10 + selecionadas_10 > LIMITE_COTA_10:
                st.error("Não há cotas R$10 suficientes disponíveis para todos os adultos selecionados.")
            elif itens_excedidos:
                st.error("Um ou mais itens selecionados não têm vagas suficientes. Atualize a página e escolha outro item: " + ", ".join(itens_excedidos))
            elif not comprovante:
                st.error("Anexe o comprovante do Pix.")
            elif comprovante.size > 200 * 1024:
                st.error("O comprovante deve ter no máximo 200KB. Comprima a imagem ou envie um arquivo menor.")
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

                    st.session_state.inscricao_concluida = True
                    st.session_state.familia_confirmada = False
                    st.session_state.mostrar_formulario = False
                    st.session_state.adultos_nomes = []
                    st.session_state.criancas_nomes = []
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
