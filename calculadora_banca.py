import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

# Definir o tema claro/escuro
theme = st.session_state.get("theme", "dark")

# CSS global
if theme == "dark":
    st.markdown("""
        <style>
            .stApp {
                background-color: #0d1216;
                color: white;
            }
            .stNumberInput, .stTextInput {
                background-color: #2e343d;
                color: white;
            }
            .stButton, .stDownloadButton {
                background-color: #ff4b4b;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .stApp {
                background-color: #f0f0f0;
                color: black;
            }
            .stNumberInput, .stTextInput {
                background-color: #ffffff;
                color: black;
            }
            .stButton, .stDownloadButton {
                background-color: #4caf50;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Título da aplicação
st.title("Calculadora de Metas - Trader Pedro")

# Inputs
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1)

# Função de geração de gráfico
def gerar_grafico():
    dias = np.arange(1, dias_para_meta + 1)
    banca = banca_inicial * (1 + (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1) ** dias
    plt.plot(dias, banca, color='red', linewidth=2)
    plt.title('Evolução da Banca', fontsize=16, color='white')
    plt.xlabel('Dias', fontsize=12, color='white')
    plt.ylabel('Valor da Banca (R$)', fontsize=12, color='white')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='white')
    plt.gca().set_facecolor('#0d1216')  # fundo escuro do gráfico
    return plt

# Gerar gráfico
grafico = gerar_grafico()

# Função de exportar PDF
def exportar_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)

    # Título
    c.drawString(100, 750, "Agenda de Metas - Trader Pedro")
    
    # Agenda gerada
    y_position = 730
    for dia in range(1, dias_para_meta + 1):
        banca_atual = banca_inicial * (1 + (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1) ** dia
        c.drawString(100, y_position, f"Dia {dia}: {banca_atual:,.2f}")
        y_position -= 20

    # Salvar gráfico no buffer de imagem
    img_buffer = BytesIO()
    grafico.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    # Adicionar imagem do gráfico no PDF
    c.drawImage(img_buffer, 100, y_position - 300, width=400, height=300)
    
    # Finalizar o PDF
    c.save()
    buffer.seek(0)
    return buffer

# Botão para gerar PDF
if st.button("Exportar Agenda"):
    pdf_buffer = exportar_pdf()
    st.download_button(
        label="Baixar PDF",
        data=pdf_buffer,
        file_name="agenda_trader_pedro.pdf",
        mime="application/pdf"
    )
