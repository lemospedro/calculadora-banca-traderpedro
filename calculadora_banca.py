import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

# CSS global
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        /* Fundo da aplicação */
        .stApp {
            background-color: #0d1216;
        }

        /* Labels dos inputs estilizados */
        .stNumberInput label, .stTextInput label {
            font-family: 'Helvetica', !important;
            font-weight: bold;
            color: #ffffff !important;
        }

        /* Aplicando Helvetica em todo o texto */
        * {
            font-family: 'Helvetica', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal com gradiente de cores
st.markdown("""
    <h1 style="
        font-family: 'Bebas Neue', sans-serif;
        font-size: 48px;
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff914d, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 50px;">
        Calculadora de Metas - Trader Pedro
    </h1>
""", unsafe_allow_html=True)

# Entrada dos dados
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função para formatar os valores
def formatar_em_cru(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Botão de cálculo
banca_evolucao = []
grafico_gerado = False
if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        bancas = [banca_atual]
        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            necessidade_dia = round(banca_atual * porcentagem_diaria, 2)
            banca_evolucao.append(f"**Dia {dia}:** {formatar_em_cru(banca_atual)} - Necessário: {formatar_em_cru(necessidade_dia)}")
            bancas.append(banca_atual)

        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária Necessária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** {formatar_em_cru(stop_loss)}")
        for linha in banca_evolucao:
            st.write(linha)

        # Geração do gráfico
        plt.figure(facecolor="#0d1216")
        plt.plot(range(dias_para_meta + 1), bancas, marker='o', linestyle='-', color='#ff4b4b')
        plt.title("Evolução da Banca", color="white", fontsize=14, fontweight="bold")
        plt.xlabel("Dias", color="white", fontweight="bold")
        plt.ylabel("Banca (R$)", color="white", fontweight="bold")
        plt.grid(True, color="white")
        plt.gca().set_facecolor('#0d1216')
        plt.tick_params(colors='white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        grafico_buffer = BytesIO()
        plt.savefig(grafico_buffer, format="png", transparent=False)
        st.pyplot(plt)
        grafico_buffer.seek(0)
        grafico_gerado = True
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")

# Função para exportar para PDF
def exportar_pdf():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_bold = styles["Heading2"]

    elementos.append(Paragraph("Calculadora de Metas - Trader Pedro", style_bold))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Banca Inicial: R$ {banca_inicial:.2f}", style_normal))
    elementos.append(Paragraph(f"Meta Total: R$ {meta_desejada:.2f}", style_normal))
    elementos.append(Paragraph(f"Dias para atingir a meta: {dias_para_meta}", style_normal))
    elementos.append(Spacer(1, 12))

    for linha in banca_evolucao:
        elementos.append(Paragraph(linha, style_normal))

    if grafico_gerado:
        grafico_buffer.seek(0)
        elementos.append(Spacer(1, 12))
        elementos.append(Image(grafico_buffer, width=500, height=300))

    pdf.build(elementos)
    buffer.seek(0)
    return buffer

if grafico_gerado:
    pdf_buffer = exportar_pdf()
    st.download_button("Baixar Agenda em PDF", data=pdf_buffer, file_name="agenda_trader_pedro.pdf", mime="application/pdf")

# Links finais
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<a href="https://trade.polariumbroker.com/register?aff=436446&aff_model=revenue&afftrack=" target="_blank" '
        'style="background-color: #0d1216; color: #ffffff; font-weight: bold; border: 2px solid #ff4b4b; '
        'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none;">Abrir Polarium Broker</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="https://br.tradingview.com/pricing/?share_your_love=traderpedrobr" target="_blank" '
        'style="background-color: #0d1216; color: #ffffff; font-weight: bold; border: 2px solid #ff4b4b; '
        'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none;">Abrir TradingView</a>',
        unsafe_allow_html=True
    )

st.markdown(
    '<a href="https://drive.google.com/file/d/1H_VNOgYSRNnsGIEj_g2B3xwQxSa-Zu4d/view?usp=sharing" target="_blank" '
    'style="background-color: #0d1216; color: #ffffff; font-weight: bold; border: 2px solid #14b802; '
    'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none;">Baixar - Análise Abundante</a>',
    unsafe_allow_html=True
)
