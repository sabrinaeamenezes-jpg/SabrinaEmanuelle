import streamlit as st
import pandas as pd
import plotly.express as px # Biblioteca para gráficos bonitos

st.set_page_config(page_title="Dashboard de Cancelamentos", layout="wide")

# Estilização CSS para mudar a cor de fundo ou fontes (opcional)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚫 Dashboard de Cancelamentos Profissional")

sheet_url = "https://docs.google.com/spreadsheets/d/1IJzjb6TH1JzLkEMh6r8kT9ZsgghBKbmsfP-Ig6Ejdi8/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    df['data'] = pd.to_datetime(df['data'])

    # --- FILTROS SIDEBAR ---
    st.sidebar.header("Configurações de Filtro")
    
    # Filtro de Data
    min_data = df['data'].min().date()
    max_data = df['data'].max().date()
    periodo = st.sidebar.date_input("Período", value=(min_data, max_data))

    # Filtro de Franquia
    franquias = ["Todas"] + list(df['franquia'].unique())
    franquia_sel = st.sidebar.selectbox("Franquia", franquias)

    # --- LÓGICA DE FILTRO ---
    df_filtrado = df.copy()
    if len(periodo) == 2:
        df_filtrado = df_filtrado[(df_filtrado['data'].dt.date >= periodo[0]) & (df_filtrado['data'].dt.date <= periodo[1])]
    if franquia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['franquia'] == franquia_sel]

    # --- LAYOUT DE MÉTRICAS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cancelados", len(df_filtrado))
    col2.metric("Franquias Ativas", df_filtrado['franquia'].nunique())
    col3.metric("Motivos Distintos", df_filtrado['motivo'].nunique())

    st.divider()

    # --- GRÁFICOS VISUAIS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Motivos por Volume")
        # Criando um gráfico de barras horizontal mais moderno
        fig_bar = px.bar(
            df_filtrado['motivo'].value_counts().reset_index(),
            x='count', 
            y='motivo',
            orientation='h',
            labels={'count': 'Quantidade', 'motivo': 'Motivo'},
            color_discrete_sequence=['#EF553B'] # Cor coral/vermelha
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("🍩 Proporção de Motivos")
        # Gráfico de Rosca (Donut)
        fig_pie = px.pie(
            df_filtrado, 
            names='motivo', 
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABELA FINAL ---
    st.subheader("📋 Lista Detalhada")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
