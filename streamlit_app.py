import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Meu Dash", layout="wide")

# Função para ler qualquer aba do Google Sheets
def carregar_dados(gid):
    url = f"https://docs.google.com/spreadsheets/d/1IJzjb6TH1JzLkEMh6r8kT9ZsgghBKbmsfP-Ig6Ejdi8/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# --- NAVEGAÇÃO POR ABAS ---
aba1, aba2 = st.tabs(["🚫 Cancelamentos", "🤝 Reuniões Realizadas"])

# --- ABA 1: CANCELAMENTOS ---
with aba1:
    st.title("Controle de Cancelamentos")
    try:
        # O GID 0 costuma ser a primeira aba da planilha
        df_canc = carregar_dados("0") 
        df_canc['data'] = pd.to_datetime(df_canc['data'])
        
        # (Aqui mantemos a lógica de filtros que já funcionou para você)
        st.write("Visualize abaixo os indicadores de cancelamento.")
        st.plotly_chart(px.bar(df_canc['motivo'].value_counts().reset_index(), x='count', y='motivo', orientation='h', color_discrete_sequence=['#EF553B']))
        st.dataframe(df_canc, use_container_width=True)
    except Exception as e:
        st.error(f"Erro na aba de Cancelamentos: {e}")

# --- ABA 2: REUNIÕES ---
with aba2:
    st.title("Cronograma de Reuniões")
    try:
        # IMPORTANTE: Você precisa descobrir o GID da sua segunda aba no Google Sheets
        # Olhe a URL da planilha quando estiver na aba de reuniões, aparecerá algo como gid=123456
        df_reunioes = carregar_dados("1837071827") 
        df_reunioes['data'] = pd.to_datetime(df_reunioes['data'])

        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.metric("Total de Reuniões", len(df_reunioes))
            status_sel = st.selectbox("Filtrar por Status", ["Todas"] + list(df_reunioes['status'].unique()))

        with col2:
            df_reun_filt = df_reunioes.copy()
            if status_sel != "Todas":
                df_reun_filt = df_reun_filt[df_reun_filt['status'] == status_sel]
            
            st.write("Histórico de Reuniões:")
            st.dataframe(df_reun_filt, use_container_width=True)

        # Gráfico de reuniões por tempo
        fig_reun = px.line(df_reunioes.groupby('data').size().reset_index(name='qtd'), x='data', y='qtd', title="Volume de Reuniões no Tempo")
        st.plotly_chart(fig_reun, use_container_width=True)

    except Exception as e:
        st.info("Para visualizar as reuniões, certifique-se de que a aba 'reunioes' existe e o GID está correto.")
        st.warning("Dica: O GID é o número que aparece no final do link da planilha quando você clica na aba de reuniões.")

