import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard de Cancelamentos", layout="wide")

st.title("🚫 Dashboard de Cancelamentos")

# Link da sua planilha (ajustado para exportar CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/1IJzjb6TH1JzLkEMh6r8kT9ZsgghBKbmsfP-Ig6Ejdi8/export?format=csv"

try:
    # Lendo os dados
    df = pd.read_csv(sheet_url)
    
    # IMPORTANTE: Converter a coluna de data para o formato que o Python entende
    # Supondo que o nome da coluna na sua planilha seja 'data'
    df['data'] = pd.to_datetime(df['data'])

    # --- CRIAÇÃO DOS FILTROS NA BARRA LATERAL ---
    st.sidebar.header("Filtros")

    # 1. Filtro de Período (Data)
    min_data = df['data'].min().date()
    max_data = df['data'].max().date()
    
    periodo = st.sidebar.date_input(
        "Selecione o período",
        value=(min_data, max_data),
        min_value=min_data,
        max_value=max_data
    )

    # 2. Filtro de Franquia
    franquias = ["Todas"] + list(df['franquia'].unique())
    franquia_selecionada = st.sidebar.selectbox("Selecione a Franquia", franquias)

    # 3. Filtro de Motivo
    motivos = ["Todos"] + list(df['motivo'].unique())
    motivo_selecionado = st.sidebar.selectbox("Motivo do Cancelamento", motivos)

    # --- APLICANDO OS FILTROS AOS DADOS ---
    df_filtrado = df.copy()

    # Filtrar por data (verifica se o usuário selecionou início e fim)
    if len(periodo) == 2:
        data_inicio, data_fim = periodo
        df_filtrado = df_filtrado[(df_filtrado['data'].dt.date >= data_inicio) & 
                                  (df_filtrado['data'].dt.date <= data_fim)]

    # Filtrar por franquia
    if franquia_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['franquia'] == franquia_selecionada]

    # Filtrar por motivo
    if motivo_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['motivo'] == motivo_selecionado]

    # --- EXIBIÇÃO DOS RESULTADOS ---
    
    # Métricas principais
    col1, col2 = st.columns(2)
    col1.metric("Total de Cancelamentos", len(df_filtrado))
    col2.metric("Clientes Afetados", df_filtrado['cliente'].nunique())

    # Gráfico de Cancelamentos por Motivo
    st.subheader("Motivos de Cancelamento")
    st.bar_chart(df_filtrado['motivo'].value_counts())

    # Tabela detalhada
    st.subheader("Dados Detalhados")
    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Erro: Verifique se os nomes das colunas na planilha estão corretos (data, franquia, motivo, cliente).")
    st.info(f"Detalhe do erro: {e}")
