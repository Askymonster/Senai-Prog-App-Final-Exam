import streamlit as st
import pandas as pd


st.header("It! Refrigerantes")
st.subheader("Análise de dados de produção e de máquinas da linha de montagem")

st.markdown("---")

st.subheader("Faça Upload dos dados de Produção")
up_file = st.file_uploader("Carregar Dados")

if up_file is not None:
    df = pd.read_csv(up_file)
    st.success("Dados Carregados com Sucesso")
    for index, row in df:
        if df["Peças Totais"] != df["Peças Boas"] + df["Peças Ruins"]:
            st.error("Peças totais não pode ser diferente da soma de peças boas e peças ruins")
else:
    df = []
    

edited_df = st.data_editor(df)


dayprod_graph = st.bar_chart(data = edited_df, 
                             x = edited_df[5], y = edited_df[1],
                             x_label = "Peças Produzidas", y_label = "Data",
                             color = ["#751B96", "FFCF0F"])

total_prod = edited_df.iloc["Data","Peças Produzidas"].sum()
def_prod = edited_df.iloc["Data","Peças Ruins"].sum()

dif_totaldef = (total_prod/def_prod) * 100
              
error_rate_graph = st.area_chart(data = edited_df, x = edited_df["Data"], y = dif_totaldef,
                                 x_label = "Data", y_label = "Taxa de Defeitos")


with st.form("Filtros"):
    mindate = edited_df["Data"].min()
    maxdate = edited_df["Data"].max()
    
    date = st.date_input("Data Inicial - Final",
                         min_value = mindate,
                         max_value = maxdate,
                         value = None,
                         format = "DD-MM-YYYY")
    
    mach_name = st.selectbox("Nome do Maquinário", edited_df["Maquina"])
    shift = st.selectbox("Turno", edited_df["Turno"])
    
    st.form_submit_button("Salvar Dados")


st.markdown("---")

st.subheader("Funcionalidades Avançadas")

