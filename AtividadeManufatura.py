import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np


st.header("It! Refrigerantes")
st.subheader("Análise de dados de produção e de máquinas da linha de montagem")

st.markdown("---")

st.subheader("Faça Upload dos dados de Produção")
up_file = st.file_uploader("Carregar Dados")


if up_file is not None:
    df = pd.read_csv(up_file)
    st.success("Dados Carregados com Sucesso")
    
    edited_df = st.data_editor(df, num_rows = "dynamic")
    
    data_efic = pd.DataFrame(
        {
        "Eficiência Diária (em %)": np.round((edited_df["Peças Boas"]/edited_df["Peças Totais"] * 100)),
        "Data de Produção": edited_df["Data"]
        }
    )
    
    if edited_df["Maquina"].any() == edited_df["Maquina"].any():
        edited_df["Peças Totais"]
        
    
    d_efic = data_efic.set_index("Data de Produção")
    
    d_efic




    dayprod_graph = st.bar_chart(data = edited_df, 
                                 x = "Data", y = "Peças Totais",
                                 color = ["#751B96"])


    

    edited_df["Taxa de Defeitos (em %)"] = (edited_df["Peças Ruins"]/edited_df["Peças Totais"]) * 100
    if edited_df["Taxa de Defeitos (em %)"].any() > 10:
        st.error(f"Eficiência de {edited_df['Taxa de Defeitos (em %)']} em  {edited_df['Data']}")
                  
    error_rate_graph = st.area_chart(data = edited_df, x = "Data", y = "Taxa de Defeitos (em %)",
                                    color = ["#FFE529"])


    with st.form("Filtros"):
        mindate = min(edited_df["Data"])
        maxdate = max(edited_df["Data"])
        parsed_date_min = datetime.strptime(mindate, "%d-%m-%Y")
        parsed_date_max = datetime.strptime(maxdate, "%d-%m-%Y")
        
        date = st.date_input("Data Inicial - Final",
                             value = None,
                             min_value = parsed_date_min,
                             max_value = parsed_date_max,
                             format = "DD-MM-YYYY")
        
        mach_name = st.selectbox("Nome do Maquinário", edited_df["Maquina"])
        shift = st.selectbox("Turno", edited_df["Turno"])
        
        st.form_submit_button("Salvar Dados")


    st.markdown("---")

    st.subheader("Funcionalidades Avançadas")

else:
    df = []
 



