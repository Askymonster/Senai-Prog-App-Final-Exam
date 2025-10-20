import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np


st.header("It! Refrigerantes") # Titulo da Pagina
st.subheader("Análise de dados de produção e de máquinas da linha de montagem") # Subtitulo/Funcao

st.markdown("---")

# Instrução de Upload do CSV
st.subheader("Faça Upload dos dados de Produção")
up_file = st.file_uploader("Carregar Dados")


# Checa se um csv foi inserido
if up_file is not None:
    df = pd.read_csv(up_file)
    st.success("Dados Carregados com Sucesso")
    
    edited_df = st.data_editor(df, num_rows = "dynamic")
    
    # Transformar DataFrame em csv para poder ser baixado
    edit_df_csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar Data", data = edit_df_csv, file_name = "Dados Editados.csv")
    
    # Agrupar por Data e Máquina: peças boas, totais e as ruins
    maq_sum = edited_df.groupby(["Data", "Maquina"])[["Peças Boas", "Peças Totais", "Peças Ruins"]].sum().reset_index()
    
    # Codigo para eficiencia diaria (separado por data)
    maq_sum["Eficiência (%)"] = np.round((maq_sum["Peças Boas"] / maq_sum["Peças Totais"]) * 100, 2)

    # Tabela de eficiencia diaria
    st.subheader("Eficiência Diária")
    st.dataframe(maq_sum[["Data", "Eficiência (%)"]], hide_index=True)
    
    # # Codigo para media diaria por maquina (separado por maquina)
    med = maq_sum.groupby("Maquina")[["Peças Totais"]].sum().reset_index()
    days = maq_sum["Data"].nunique()
    med["Média Diária (Peças)"] = np.round(med["Peças Totais"] / days, 2)

    # Tabela de media por maquina
    st.subheader("Média de Produção por Máquina")
    st.dataframe(med, hide_index=True)
    
    st.markdown("---")

    
    # Codigo para taxa de defeitos
    maq_sum["Taxa de Defeitos (em %)"] = (maq_sum["Peças Ruins"]/edited_df["Peças Totais"]) * 100
         
    # Grafico de taxa de defeitos em %
    st.subheader("Gráfico da Taxa de Defeito Diária (em %)")         
    error_rate_graph = st.area_chart(data = maq_sum, x = "Data", y = "Taxa de Defeitos (em %)",
                                    color = ["#FFE529"])
    
    # Grafico de producao diaria
    st.subheader("Gráfico da Produção Diária")
    dayprod_graph = st.bar_chart(data = edited_df, 
                                 x = "Data", y = "Peças Totais",
                                 color = ["#751B96"])


    st.markdown("---")

    # Formulario para filtrar itens
    with st.form("Filtros"):
        edited_df["Data"] = pd.to_datetime(edited_df["Data"], errors="coerce", dayfirst=True)

        
        mindate = min(edited_df["Data"])
        maxdate = max(edited_df["Data"])
        parsed_date_min = mindate.date()
        parsed_date_max = maxdate.date()
        date = st.date_input("Data Inicial - Final",
                             value = (parsed_date_min,parsed_date_max),
                             min_value = parsed_date_min,
                             max_value = parsed_date_max,
                             format = "DD-MM-YYYY")
        
        df_noduplicates_mach = edited_df["Maquina"].drop_duplicates()
        df_noduplicates_shift = edited_df["Turno"].drop_duplicates()
        
        mach_name = st.selectbox("Nome do Maquinário", df_noduplicates_mach)
        shift = st.selectbox("Turno", df_noduplicates_shift)
        
        submit = st.form_submit_button("Filtrar")


    st.markdown("---")
    
    # Codigo para dataframe dos itens filtrados
    if submit:
        start_date, end_date = date

        df_filtered = edited_df[
            (edited_df["Data"].dt.date >= start_date)
            & (edited_df["Data"].dt.date <= end_date)
            & (edited_df["Maquina"] == mach_name)
            & (edited_df["Turno"] == shift)
        ]

        st.subheader("Dados Filtrados")
        st.dataframe(df_filtered)
        
        filtered_df_csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Baixar Dados Filtrados", data = filtered_df_csv,
                           file_name = "Dados Filtrados.csv")
        
        
    # Codigo dos alertas de erros 
    st.subheader("Alertas Automáticos")

    for index, row in maq_sum.iterrows():
        if row["Eficiência (%)"] < 90:
            st.error(f"⚠️ Eficiência baixa em {row['Data']} ({row['Maquina']}): {row['Eficiência (%)']}%")

        if row["Peças Totais"] < 80:
            st.error(f"⚠️ Produção abaixo do mínimo em {row['Data']} ({row['Maquina']}): {row['Peças Totais']} peças")


else:
    df = []
    st.write("Nenhum Dado Selecionado")
 



