import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import pdfmetrics

# Definir o local para garantir a formatação em português
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para alternar entre os temas claro e escuro
def toggle_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Estilo do botão
    if st.session_state.theme == 'light':
        button_text = 'Escuro'
        button_style = 'background-color: #ff4b4b; color: #ffffff; border-radius: 20px; width: 80px; height: 40px; display: flex; align-items: center; justify-content: center;'
    else:
        button_text = 'Claro'
        button_style = 'background-color: #0d1216; color: #ffffff; border-radius: 20px; width: 80px; height: 40px; display: flex; align-items: center; justify-content: center;'

    # Exibir o botão
    if st.button(button_text, key="theme_toggle", help=f"Ativar tema {button_text.lower()}", use_container_width=True, on_click=toggle_button, args=(st.session_state.theme,)):
        pass

    st.markdown(f"<div style='{button_style}'>{button_text}</div>", unsafe_allow_html=True)

def toggle_button(theme):
    if theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'


# CSS para personalizar o tema
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
            .stApp {
                background-color: #0d1216;
            }
            .stApp h1 {
                color: #ff4b4b;
            }
            .stNumberInput label, .stTextInput label {
                color: #ffffff !important;
            }
            .stButton button {
                background-color: #ff4b4b;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
            }
            .stApp h1 {
                color: #000000;
            }
            .stNumberInput label, .stTextInput label {
                color: #000000 !important;
            }
            .stButton button {
                background-color: #000000;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)


# Aplicando o tema
apply_theme()

# Título principal
st.markdown("""
    <h1>Calculadora de Metas - Trader Pedro</h1>
""", unsafe_allow_html=True)

# Entrada dos dados
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")


# Função para formatar valores
def formatar_em_cru(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


# Função para gerar o gráfico
def gerar_grafico(banca_inicial, meta_desejada, dias_para_meta):
    porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
    banca_atual = banca_inicial
    banca_evolucao = [banca_atual]

    for dia in range(1, dias_para_meta + 1):
        ganho_diario = banca_atual * porcentagem_diaria
        banca_atual += ganho_diario
        banca_evolucao.append(banca_atual)

    # Gerar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(range(dias_para_meta + 1), banca_evolucao, label='Evolução da Banca', color='red', linewidth=2)
    plt.xlabel('Dia')
    plt.ylabel('Valor da Banca (R$)')
    plt.title('Evolução da Banca ao Longo dos Dias')
    plt.grid(True)
    plt.tight_layout()

    # Salvar o gráfico em uma imagem
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf


# Gerar a agenda e gráfico quando o botão for pressionado
if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        banca_evolucao = []
        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            necessidade_dia = round(banca_atual * porcentagem_diaria, 2)
            banca_evolucao.append(f"**Dia {dia}:** {formatar_em_cru(banca_atual)} - Necessário: {formatar_em_cru(necessidade_dia)}")

        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária Necessária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** {formatar_em_cru(stop_loss)}")
        for linha in banca_evolucao:
            st.write(linha)

        # Gerar gráfico
        img_buf = gerar_grafico(banca_inicial, meta_desejada, dias_para_meta)
        st.image(img_buf)

    else:
        st.error("Por favor, insira valores válidos para todos os campos!")


# Função para exportar PDF com gráfico
def exportar_pdf():
    img_buf = gerar_grafico(banca_inicial, meta_desejada, dias_para_meta)

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Definir fontes
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)

    # Título do PDF
    c.drawString(200, 750, "Agenda de Metas - Trader Pedro")

    # Escrever a agenda
    y_position = 700
    for linha in banca_evolucao:
        c.drawString(50, y_position, linha)
        y_position -= 20

    # Adicionar gráfico no PDF
    img_buf.seek(0)
    c.drawImage(img_buf, 50, 300, width=500, height=300)

    # Salvar o PDF
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


# Botão para exportar PDF
if st.button("Exportar Agenda para PDF"):
    pdf_buffer = exportar_pdf()
    st.download_button(
        label="Clique para baixar o PDF",
        data=pdf_buffer,
        file_name="agenda_de_metas.pdf",
        mime="application/pdf"
    )
