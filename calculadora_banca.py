import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# CSS global
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        .stApp h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 48px;
            text-align: center;
            color: #ff4b4b;
            margin-bottom: 50px;
            animation: fadeIn 2s ease-out;  /* Nova animação */
        }
        .stApp {
            background-color: #0d1216;
        }
        .stNumberInput label, .stTextInput label {
            font-family: 'Helvetica', !important;
            font-weight: bold;
            color: #ffffff !important;
        }
        * {
            font-family: 'Helvetica', sans-serif;
        }

        /* Nova animação do título */
        @keyframes fadeIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Efeito nos botões com aumento e sombra */
        .stButton>button {
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);  /* Aumenta o botão */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* Adiciona sombra */
            background-color: #ff4b4b; /* Muda a cor de fundo */
            color: white; /* Muda a cor do texto */
        }

        /* Botões personalizados */
        .stButton>button#btn-analise-abundante {
            background-color: #0d1216;
            color: #ffffff;
            border: 2px solid #00b140; /* Borda verde */
        }
        .stButton>button#btn-analise-abundante:hover {
            background-color: #0d1216;
            border: 2px solid #00b140;
            color: #00b140; /* Muda a cor do texto para verde */
        }

        .stButton>button#btn-create-polarium {
            background-color: #0d1216;
            color: #ffffff;
            border: 2px solid #ff4b4b; /* Borda vermelha */
        }
        .stButton>button#btn-create-polarium:hover {
            background-color: #0d1216;
            border: 2px solid #ff4b4b;
            color: #ff4b4b; /* Muda a cor do texto para vermelho */
        }

        .stButton>button#btn-tradingview {
            background-color: #0d1216;
            color: #ffffff;
            border: 2px solid #ff4b4b; /* Borda vermelha */
        }
        .stButton>button#btn-tradingview:hover {
            background-color: #0d1216;
            border: 2px solid #ff4b4b;
            color: #ff4b4b; /* Muda a cor do texto para vermelho */
        }

    </style>
""", unsafe_allow_html=True)

# Título principal com fonte Bebas Neue
st.markdown("""
    <h1>Calculadora de Metas - Trader Pedro</h1>
""", unsafe_allow_html=True)

# Entrada dos dados
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função de formatação
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
        bancas = [banca_atual]  # Lista para o gráfico
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
        plt.plot(range(dias_para_meta + 1), bancas, marker='o', linestyle='-', color='#ff4b4b')  # Linha avermelhada
        plt.title("Evolução da Banca", color="white", fontsize=14, fontweight="bold")  # Título em branco
        plt.xlabel("Dias", color="white", fontweight="bold")  # Texto eixo X em branco
        plt.ylabel("Banca (R$)", color="white", fontweight="bold")  # Texto eixo Y em branco
        plt.grid(True, color="white")
        plt.gca().set_facecolor('#0d1216')
        plt.tick_params(colors='white')  # Ticks em branco
        plt.gca().spines['bottom'].set_color('white')  # Eixo inferior em branco
        plt.gca().spines['left'].set_color('white')  # Eixo esquerdo em branco
        grafico_buffer = BytesIO()
        plt.savefig(grafico_buffer, format="png", transparent=True)  # Removendo a transparência para fundo escuro
        st.pyplot(plt)
        grafico_buffer.seek(0)  # Resetar o buffer para leitura posterior
        grafico_gerado = True
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")

# Função para exportar para PDF
def exportar_pdf():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []

    # Estilos
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_bold = styles["Heading2"]

    # Adicionar textos
    elementos.append(Paragraph("Calculadora de Metas - Trader Pedro", style_bold))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Banca Inicial: R$ {banca_inicial:.2f}", style_normal))
    elementos.append(Paragraph(f"Meta Total: R$ {meta_desejada:.2f}", style_normal))
    elementos.append(Paragraph(f"Dias para atingir a meta: {dias_para_meta}", style_normal))
    elementos.append(Spacer(1, 12))

    # Adicionar a agenda
    for linha in banca_evolucao:
        elementos.append(Paragraph(linha, style_normal))

    # Adicionar o gráfico como imagem
    if grafico_gerado:
        grafico_buffer.seek(0)
        elementos.append(Spacer(1, 12))
        elementos.append(Image(grafico_buffer, width=500, height=300))

    # Construir o PDF
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
        'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none; text-align: center; '
        'display: inline-block;" id="btn-create-polarium">Crie sua conta na Polarium Broker</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="https://br.tradingview.com/pricing/?share_your_love=traderpedrobr" target="_blank" '
        'style="background-color: #0d1216; color: #ffffff; font-weight: bold; border: 2px solid #ff4b4b; '
        'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none; text-align: center; '
        'display: inline-block;" id="btn-tradingview">Crie sua conta no TradingView</a>',
        unsafe_allow_html=True
    )

with col1:
    st.markdown(
        '<a href="https://drive.google.com/file/d/1H_VNOgYSRNnsGIEj_g2B3xwQxSa-Zu4d/view?usp=sharing" target="_blank" '
        'style="background-color: #0d1216; color: #ffffff; font-weight: bold; border: 2px solid #ff4b4b; '
        'border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none; text-align: center; '
        'display: inline-block;" id="btn-analise-abundante">Abrir Análise Abundante</a>',
        unsafe_allow_html=True
    )
