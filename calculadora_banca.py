import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import locale

# CSS Global
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Bebas+Neue&display=swap');

        .stApp h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 48px;
            text-align: center;
            color: #ff4b4b;
            margin-bottom: 30px;
        }

        * { font-family: 'Montserrat'; }
        .stNumberInput label { font-weight: bold; color: #ffffff !important; }
        .stApp { background-color: #0d1216; }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1>Calculadora de Metas - Trader Pedro</h1>", unsafe_allow_html=True)

# Entradas
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função para formatar os valores
def formatar_em_cru(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Variáveis globais para gráfico
dias = []
banca_evolucao = []

# Botão de cálculo
if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        # Cálculos
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        banca_evolucao = [banca_inicial]
        dias = list(range(1, dias_para_meta + 1))

        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            banca_evolucao.append(banca_atual)

        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária Necessária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** {formatar_em_cru(stop_loss)}")
        
        # Exibindo os valores dia a dia
        for i, valor in enumerate(banca_evolucao[:-1]):
            st.write(f"**Dia {i + 1}:** {formatar_em_cru(valor)}")

        # Gráfico de Evolução da Banca
        fig, ax = plt.subplots()
        ax.plot(dias, banca_evolucao[:-1], marker='o', linestyle='-', color='#ff4b4b')
        ax.set_title("Evolução da Banca")
        ax.set_xlabel("Dias")
        ax.set_ylabel("Valor da Banca (R$)")
        st.pyplot(fig)

        # Salvar gráfico em memória
        buffer_grafico = BytesIO()
        plt.savefig(buffer_grafico, format="png")
        buffer_grafico.seek(0)

        # Exportar para PDF
        def exportar_pdf():
            buffer_pdf = BytesIO()
            c = canvas.Canvas(buffer_pdf, pagesize=letter)
            
            # Cabeçalho
            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, 750, "Agenda de Metas - Trader Pedro")

            # Adicionando texto
            c.setFont("Helvetica", 12)
            y = 720
            for i, valor in enumerate(banca_evolucao[:-1]):
                c.drawString(50, y, f"Dia {i + 1}: R$ {formatar_em_cru(valor)}")
                y -= 20
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 720

            # Adicionando gráfico
            c.showPage()
            c.drawImage(ImageReader(buffer_grafico), 50, 300, width=500, height=300)
            c.save()
            buffer_pdf.seek(0)
            return buffer_pdf

        # Botão de download
        st.download_button(
            label="Baixar Agenda em PDF",
            data=exportar_pdf(),
            file_name="agenda_gerenciamento.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")
