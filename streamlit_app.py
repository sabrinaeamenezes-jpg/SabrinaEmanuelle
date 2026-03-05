import streamlit as st
import pandas as pd

# Título do Dashboard
st.title("📊 Meu Controle de Gastos")

# Substitua o link abaixo pelo link que você copiou da sua planilha
# Importante: O link deve terminar com /export?format=csv
sheet_url = "https://docs.google.com/spreadsheets/d/1IJzjb6TH1JzLkEMh6r8kT9ZsgghBKbmsfP-Ig6Ejdi8/export?format=csv"

# Lendo os dados da planilha "Gastos"
try:
    df = pd.read_csv(sheet_url)
    
    st.write("Aqui estão os seus dados mais recentes:")
    st.dataframe(df) # Mostra a tabela interativa
    
    # Se você tiver colunas de números, o Streamlit pode criar um gráfico automático
    st.subheader("Visualização Gráfica")
    st.bar_chart(df)

except Exception as e:
    st.error(f"Erro ao conectar com a planilha: {e}")
    st.info("Dica: Verifique se a planilha está compartilhada como 'Qualquer pessoa com o link'.")
