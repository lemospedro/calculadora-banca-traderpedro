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

        /* Título */
        .stApp h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 48px;
            text-align: center;
            color: #ff4b4b;
            margin-bottom: 50px;
        }

        /* Fundo da aplicação em preto */
        .stApp {
            background-color: #0d1216;
        }

        /* Labels dos inputs estilizados */
        .stNumberInput label, .stTextInput label {
            font-family: 'Helvetica', sans-serif;
            font-weight: bold;
            color: #ffffff !important; /* Cor branca */
        }

        /* Aplicando Helvetica em todo o texto */
        * {
            font-family: 'Helvetica', sans-serif;
        }

        /* Estilo base dos botões */
        a {
            background-color: #0d1216; /* Cor padrão */
            border: 2px solid #ff4b4b; /* Borda padrão */
            color: #ffffff !important; /* Texto branco */
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            text-decoration: none;
            text-align: center;
            display: inline-block;
            transition: all 0.3s ease-in-out; /* Transição suave */
            box-shadow: 0 0 0 transparent; /* Inicialmente sem sombra */
        }

        /* Hover: Mudança de cor, sombra e leve aumento */
        a:hover {
            background-color: #1a1f25; /* Cor levemente mais clara */
            color: #ffcccb; /* Texto em tom suave */
            transform: scale(1.05); /* Leve aumento */
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.5); /* Sombra sutil */
        }

        /* Estilo do botão específico 'Abrir Análise Abundante' */
        a.analise-abundante {
            border-color: #00c418; /* Borda verde */
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
        plt.savefig(grafico_buffer, format="png", transparent=False)
        st.pyplot(plt)
        grafico_buffer.seek(0)
        grafico_gerado = True
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")

# Links finais com animações
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<a href="https://trade.polariumbroker.com/register?aff=436446&aff_model=revenue&afftrack=" target="_blank">Crie sua conta na Polarium Broker</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="https://br.tradingview.com/pricing/?share_your_love=traderpedrobr" target="_blank">Crie sua conta no TradingView</a>',
        unsafe_allow_html=True
    )

st.markdown(
    '<a class="analise-abundante" href="https://drive.google.com/file/d/1H_VNOgYSRNnsGIEj_g2B3xwQxSa-Zu4d/view?usp=sharing" target="_blank">Abrir Análise Abundante</a>',
    unsafe_allow_html=True
)
