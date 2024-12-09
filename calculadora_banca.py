import streamlit as st
import locale

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

# Reset da página
if 'calculo_feito' not in st.session_state:
    st.session_state.calculo_feito = False

# Entrada dos dados
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função para formatar os valores
def formatar_em_cru(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Botão de cálculo
if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        st.session_state.calculo_feito = True
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        banca_evolucao = []
        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            necessidade_dia = round(banca_atual * porcentagem_diaria, 2)
            banca_evolucao.append(f"**Dia {dia}:** {formatar_em_cru(banca_atual)} - Necessário: {formatar_em_cru(necessidade_dia)}")

        # Botão "Apagar Agenda" aparece aqui
        if st.session_state.calculo_feito:
            if st.button("Apagar Agenda"):
                st.session_state.calculo_feito = False
                st.experimental_rerun()

        # Mostrar agenda
        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária Necessária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** {formatar_em_cru(stop_loss)}")
        for linha in banca_evolucao:
            st.write(linha)
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
