import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

# CSS Global
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        /* Fundo geral da aplicação */
        .stApp {
            background-color: #0d1216;
        }

        /* Título com animação */
        @keyframes fadeInPulse {
            0% { 
                opacity: 0; 
                transform: scale(0.95); 
            }
            50% { 
                opacity: 0.5; 
                transform: scale(1.02); 
            }
            100% { 
                opacity: 1; 
                transform: scale(1); 
            }
        }

        .stApp h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 48px;
            text-align: center;
            color: #ff4b4b;
            margin-bottom: 50px;
            animation: fadeInPulse 2s ease-in-out;
            text-shadow: 0 0 10px rgba(255, 75, 75, 0.6);
        }

        /* Botões Gerais */
        a, button {
            background-color: #1a1f25; /* Cor cinza estática */
            border: 2px solid transparent; /* Sem borda inicialmente */
            color: #ffffff !important;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            text-decoration: none;
            text-align: center;
            display: inline-block;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 0 transparent;
            cursor: pointer;
        }

        a:hover, button:hover {
            border: 2px solid #ff4b4b; /* Borda vermelha ao passar o mouse */
            color: #ffcccb;
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
        }

        /* Botão específico do Análise Abundante */
        a.analise-abundante {
            border-color: #00c418;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
    <h1>Calculadora de Metas - Trader Pedro</h1>
""", unsafe_allow_html=True)

# Entrada dos dados
banca_inicial = st.number_input("**Banca Inicial (R$):**", min_value=0.0, step=1.0, format="%.2f", key="banca_inicial")
meta_desejada = st.number_input("**Meta Total (R$):**", min_value=0.0, step=1.0, format="%.2f", key="meta_desejada")
dias_para_meta = st.number_input("**Tempo para atingir a meta (dias):**", min_value=1, step=1, key="dias_para_meta")

# Função de cálculo e exibição de resultados
banca_evolucao = []
grafico_gerado = False

# Adicionando animação ao botão "Calcular Agenda"
st.markdown("""
    <style>
        div.stButton > button {
            background-color: #1a1f25;
            border: 2px solid transparent; /* Sem borda por padrão */
            color: white;
            font-weight: bold;
            font-size: 16px;
            border-radius: 5px;
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        div.stButton > button:hover {
            border: 2px solid #ff4b4b; /* Borda vermelha no hover */
            color: #ffcccb;
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Calcular Agenda"):
    if banca_inicial > 0 and meta_desejada > 0 and dias_para_meta > 0:
        porcentagem_diaria = (meta_desejada / banca_inicial) ** (1 / dias_para_meta) - 1
        stop_loss = banca_inicial * 0.20

        banca_atual = banca_inicial
        bancas = [banca_atual]
        for dia in range(1, dias_para_meta + 1):
            ganho_diario = banca_atual * porcentagem_diaria
            banca_atual += ganho_diario
            banca_evolucao.append(f"**Dia {dia}:** R$ {banca_atual:.2f}")
            bancas.append(banca_atual)

        st.success("Aqui está sua agenda de gerenciamento:")
        st.write(f"**Porcentagem Diária:** {porcentagem_diaria * 100:.2f}%")
        st.write(f"**Stop Loss Diário:** R$ {stop_loss:.2f}")
        for linha in banca_evolucao:
            st.write(linha)

        # Gráfico
        plt.plot(range(dias_para_meta + 1), bancas, marker='o', linestyle='-', color='#ff4b4b')
        plt.title("Evolução da Banca", color="white", fontsize=14, fontweight="bold")
        plt.xlabel("Dias", color="white")
        plt.ylabel("Banca (R$)", color="white")
        plt.grid(True)
        plt.gca().set_facecolor("#0d1216")
        plt.tick_params(colors="white")
        grafico_buffer = BytesIO()
        plt.savefig(grafico_buffer, format="png", transparent=False)
        st.pyplot(plt)
        grafico_buffer.seek(0)
    else:
        st.error("Por favor, insira valores válidos para todos os campos!")

# Links finais
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<a href="https://trade.polariumbroker.com/register?aff=436446" target="_blank">Crie sua conta na Polarium Broker</a>',
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
