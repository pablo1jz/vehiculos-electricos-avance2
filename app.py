import os
import pandas as pd
import plotly.express as px
import streamlit as st

from src.carga import cargar_datos
from src.limpieza import limpiar_datos
from src.proyeccion import calcular_metricas_serie, proyectar_ventas
from src.transformacion import aplicar_transformaciones
from src.validaciones import validar_dataset

st.set_page_config(
    page_title="Dashboard EVs — Avance 4",
    page_icon="⚡",
    layout="wide",
)


@st.cache_data
def cargar_dataset_listo() -> pd.DataFrame:
    ruta_limpia = os.path.join("datos", "procesados", "dataset_limpio.csv")
    ruta_orig = os.path.join("datos", "electric-car-sales.csv")
    if os.path.exists(ruta_limpia):
        df = pd.read_csv(ruta_limpia)
    else:
        df = aplicar_transformaciones(limpiar_datos(cargar_datos(ruta_orig)))
    validar_dataset(df)
    return df


df = cargar_dataset_listo()

st.title("⚡ Dashboard de Crecimiento y Proyección de Vehículos Eléctricos")
st.caption("Exploración histórica, indicadores dinámicos y proyección matemática (Proyecto Final Integrador — Avance 4)")

# --- 1. FILTROS INTERACTIVOS (Requerimiento 5.1) ---
st.sidebar.header("1. Filtros Históricos")

entidades_disp = sorted(df["entity"].dropna().unique().tolist())
default_idx = entidades_disp.index("World") if "World" in entidades_disp else 0
entidad_sel = st.sidebar.selectbox("País / Entidad", options=entidades_disp, index=default_idx)

min_anio = int(df["year"].min())
max_anio = int(df["year"].max())
rango_anios = st.sidebar.slider("Rango de Años", min_value=min_anio, max_value=max_anio, value=(min_anio, max_anio))

tipo_entidad_disp = sorted(df["tipo_entidad"].dropna().unique().tolist()) if "tipo_entidad" in df.columns else ["País", "Agregado"]
tipo_sel = st.sidebar.multiselect("Tipo de Entidad", options=tipo_entidad_disp, default=tipo_entidad_disp)

# --- 2. PARÁMETROS AJUSTABLES DE PROYECCIÓN (Requerimientos 5.2 y 5.3) ---
st.sidebar.header("2. Parámetros de Proyección")
modelo_sel = st.sidebar.selectbox(
    "Modelo Matemático",
    options=["Regresión Lineal", "Promedio Móvil (3 Años)", "Tasa de Crecimiento Promedio"],
)
horizonte_sel = st.sidebar.slider("Años a Proyectar", min_value=1, max_value=10, value=5)

df_filt = df[
    (df["entity"] == entidad_sel)
    & (df["year"] >= rango_anios[0])
    & (df["year"] <= rango_anios[1])
].sort_values("year")

if "tipo_entidad" in df_filt.columns and tipo_sel:
    df_filt = df_filt[df_filt["tipo_entidad"].isin(tipo_sel)]

metricas = calcular_metricas_serie(df_filt)

# --- 3. INDICADORES DINÁMICOS (Requerimiento 5.1) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Acumulado", f"{metricas['total_ventas']:,.0f}")
c2.metric("Promedio Anual", f"{metricas['promedio_ventas']:,.0f}")
c3.metric("Máximo Histórico", f"{metricas['max_ventas']:,.0f}")
var_txt = f"{metricas['variacion_global_pct']:,.1f}%" if pd.notna(metricas["variacion_global_pct"]) else "N/D"
c4.metric("Variación en Rango", var_txt)

# --- 4. VISUALIZACIONES (Requerimiento 5.1) ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Histórico de Ventas")
    fig_hist = px.bar(
        df_filt,
        x="year",
        y="electric_cars_sold",
        title=f"Ventas Históricas — {entidad_sel} ({rango_anios[0]}–{rango_anios[1]})",
        labels={"year": "Año", "electric_cars_sold": "Vehículos Eléctricos Vendidos"},
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_der:
    st.subheader("Proyección Matemática")
    df_proj = proyectar_ventas(df_filt, modelo=modelo_sel, horizonte=horizonte_sel)
    if df_proj.empty:
        st.info("Selecciona al menos 2 años con datos para calcular la proyección.")
    else:
        df_hist_plot = df_filt[["year", "electric_cars_sold"]].copy()
        df_hist_plot["tipo"] = "Histórico"
        df_comb = pd.concat([df_hist_plot, df_proj[["year", "electric_cars_sold", "tipo"]]], ignore_index=True)

        fig_proj = px.line(
            df_comb,
            x="year",
            y="electric_cars_sold",
            color="tipo",
            markers=True,
            title=f"Histórico vs. Proyección ({modelo_sel}, +{horizonte_sel} años)",
            labels={"year": "Año", "electric_cars_sold": "Vehículos Eléctricos Vendidos", "tipo": "Serie"},
        )
        st.plotly_chart(fig_proj, use_container_width=True)
        st.dataframe(
            df_proj[["year", "electric_cars_sold"]].rename(columns={"year": "Año", "electric_cars_sold": "Ventas Proyectadas"}),
            use_container_width=True,
        )
