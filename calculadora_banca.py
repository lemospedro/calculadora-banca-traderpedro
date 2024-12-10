import streamlit as st
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
import locale
import os

# Definir o locale para garantir a formatação em português
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# CSS global
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Bebas+Neue&display=swap');

        /* Título */
        .stApp h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 48px;
            text-align: center;
            color: #ff4b4b;
            margin-bottom: 50px;
        }

        /* Aplicando Montserrat em todo o texto */
        * {
            font-family: 'Montserrat';
        }

        /* Labels dos inputs estilizados */
        .stNumberInput label, .stTextInput label {
            font-family: 'Montserrat', !important;
            font-weight: bold;
            color: #ffffff !important; /* Cor branca */
        }

        /* Fundo da aplicação em preto */
        .stApp {
            background-color: #0d1216;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal com fonte Bebas Neue
st.markdown("""
    <h1>Calculadora de Metas - Trader Pedro</h1>
""", unsafe_allow_html=True)

# Entrada dos dados com os rótulos embutidos nos campos
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função para formatar os valores
def formatar_em_cru(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para gerar PDF
def gerar_pdf(banca_evolucao, porcentagem_diaria, stop_loss):
    pdf_file = "agenda_de_metas.pdf"
    c = canvas.Canvas(pdf_file)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Agenda de Metas - Trader Pedro")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Porcentagem Diária Necessária: {porcentagem_diaria * 100:.2f}%")
    c.drawString(50, 750, f"Stop Loss Diário: R$ {formatar_em_cru(stop_loss)}")

    y = 720
    c.setFont("Helvetica", 10)
    for linha in banca_evolucao:
        c.drawString(50, y, linha.replace("**", "").replace("R$", "").strip())
        y -= 15
        if y < 50:  # Adiciona uma nova página se necessário
            c.showPage()
            y = 770

    c.save()
    return pdf_file

# Botão de cálculo
if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        valores_banca = [banca_inicial]
        banca_evolucao = []

        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            necessidade_dia = round(banca_atual * porcentagem_diaria, 2)
            linha = f"**Dia {dia}:** {formatar_em_cru(banca_atual)} - Necessário: {formatar_em_cru(necessidade_dia)}"
            banca_evolucao.append(linha)
            valores_banca.append(banca_atual)

        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária Necessária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** {formatar_em_cru(stop_loss)}")
        for linha in banca_evolucao:
            st.write(linha)

        # **Gerar o Gráfico de Evolução da Banca**
        fig, ax = plt.subplots()

        # Definir a cor do fundo
        fig.patch.set_facecolor('#0d1216')
        ax.set_facecolor('#0d1216')

        # Configurar a linha e os pontos
        ax.plot(range(dias_para_meta + 1), valores_banca, marker='o', linestyle='-', color='#ff4b4b', label="Banca (R$)")

        # Personalizar os textos (cor branca)
        ax.set_title("Evolução da Banca ao Longo dos Dias", color='#FFFFFF', fontsize=14, fontweight='bold')
        ax.set_xlabel("Dias", color='#FFFFFF', fontsize=12)
        ax.set_ylabel("Banca (R$)", color='#FFFFFF', fontsize=12)

        # Personalizar os eixos
        ax.tick_params(axis='x', colors='#FFFFFF')
        ax.tick_params(axis='y', colors='#FFFFFF')

        ax.grid(color='#444444', linestyle='--', linewidth=0.5)
        ax.legend(facecolor='#0d1216', edgecolor='None', labelcolor='white')
        st.pyplot(fig)

        # Botão para exportar PDF
        st.write("---")
        st.write("### Exportar Agenda para PDF:")
        pdf_file = gerar_pdf(banca_evolucao, porcentagem_diaria, stop_loss)
        with open(pdf_file, "rb") as file:
            st.download_button(label="📥 Baixar Agenda em PDF", data=file, file_name="agenda_de_metas.pdf", mime="application/pdf")
        os.remove(pdf_file)
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")

# Botões de link estilizados
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<a href="https://trade.polariumbroker.com/register?aff=436446&aff_model=revenue&afftrack=" target="_blank" style="background-color: #ffffff; color: #0d1216; font-weight: bold; border: none; border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none; text-align: center; display: inline-block; transition: all 0.3s;">Crie sua conta na Polarium Broker</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a href="https://br.tradingview.com/pricing/?share_your_love=traderpedrobr" target="_blank" style="background-color: #ffffff; color: #0d1216; font-weight: bold; border: none; border-radius: 5px; padding: 10px 15px; font-size: 16px; text-decoration: none; text-align: center; display: inline-block; transition: all 0.3s;">Crie sua conta no TradingView</a>',
        unsafe_allow_html=True
    )
