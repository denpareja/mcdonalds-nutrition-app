import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="McDonald's Nutrition App", page_icon="🍔", layout="wide")
st.title("🍔 McDonald's Nutrition App")

# 1) Carga de datos (con manejo de error)
try:
    df = pd.read_csv("mcdonalds.csv")
except Exception as e:
    st.error(f"❌ Error leyendo mcdonalds.csv: {e}")
    st.stop()

# 2) Filtro por categoría + vista previa
st.subheader("Vista previa y filtros")

categorias = ["Todas"] + sorted(df["Category"].dropna().unique().tolist())
cat = st.selectbox("Filtrar por categoría", categorias, index=0)

df_f = df if cat == "Todas" else df[df["Category"] == cat]

st.write(df_f.head())

if st.checkbox("Mostrar todos los datos filtrados"):
    st.dataframe(df_f, use_container_width=True)

# 3) Gráficos (respetan el filtro)
st.subheader("Distribución de calorías")
try:
    fig_cal = px.histogram(df_f, x="Calories", nbins=40, title="Histograma de Calorías")
    st.plotly_chart(fig_cal, use_container_width=True)
except Exception as e:
    st.error(f"❌ Error en histograma: {e}")

st.subheader("Calorías vs Grasa Total")
try:
    fig_scatter = px.scatter(
        df_f,
        x="Total Fat",
        y="Calories",
        color="Category",
        hover_data=["Item"],
        title="Relación Calorías vs Grasa Total",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
except Exception as e:
    st.error(f"❌ Error en scatter: {e}")

# 4) (Opcional PRO) Top 10 y stats rápidas
st.subheader("Top 10 productos por calorías (según filtro)")
top10 = (
    df_f.nlargest(10, "Calories")[["Item", "Category", "Calories", "Total Fat"]]
    .reset_index(drop=True)
)
st.dataframe(top10, use_container_width=True)

st.subheader("Estadísticas descriptivas")
st.write(df_f[["Calories", "Total Fat"]].describe())
