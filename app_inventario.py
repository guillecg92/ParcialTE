# streamlit_app_inventario.py
import streamlit as st
import pandas as pd
# Cargar dataset
@st.cache_data
def cargar_datos():
 return pd.read_csv("dataset_inventario_consumomax.csv", parse_dates=["Fecha_Ingreso"])
df = cargar_datos()
# Configurar página
st.set_page_config(page_title="Sistema de Inventario ConsumoMax", page_icon=" ", 
layout="wide")
# Título principal
st.title(" Sistema Inteligente de Control de Inventario - ConsumoMax")
# Filtros laterales
st.sidebar.header("Filtros de busqueda")
almacen = st.sidebar.multiselect("Seleccionar almacen:", options=df["Almacen"].unique(), 
default=df["Almacen"].unique())
categoria = st.sidebar.multiselect("Seleccionar categoria:", options=df["Categoria"].unique(), 
default=df["Categoria"].unique())
# Aplicar filtros
df_filtrado = df[(df["Almacen"].isin(almacen)) & (df["Categoria"].isin(categoria))]
# Mostrar datos filtrados
st.subheader(" Inventario actual")
st.dataframe(df_filtrado, use_container_width=True)
# KPIs principales
st.subheader(" Indicadores rapidos")
col1, col2, col3 = st.columns(3)
with col1:
 st.metric(label="Productos registrados", value=len(df_filtrado))
with col2:
 st.metric(label="Total de stock disponible", value=int(df_filtrado["Cantidad_Actual"].sum()))
with col3:
 st.metric(label="Productos bajo umbral minimo", value=(df_filtrado["Cantidad_Actual"] < 
df_filtrado["Umbral_Minimo"]).sum())
# Gráficos
st.subheader(" Distribucion de Stock por Categoria")
stock_categoria = df_filtrado.groupby("Categoria")["Cantidad_Actual"].sum()
st.bar_chart(stock_categoria)
st.subheader(" Distribucion por Almacen")
stock_almacen = df_filtrado.groupby("Almacen")["Cantidad_Actual"].sum()
st.bar_chart(stock_almacen)
