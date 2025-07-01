# autocontrol_dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título del dashboard
st.title("Dificultad para Autocontrol según el Género")

# Cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")

df = cargar_datos()

# Renombrar valores para mayor legibilidad
df['Genero'] = df['Genero'].replace({1: 'Hombre', 2: 'Mujer'})
df['DificultadParaAutocontrol'] = df['DificultadParaAutocontrol'].replace({0: 'Ausente', 1: 'Presente'})

# Mostrar tabla de datos
if st.checkbox("Mostrar datos"):
    st.write(df[['Genero', 'DificultadParaAutocontrol']])

# Conteo de dificultad para autocontrol por género
conteo = df.groupby(['Genero', 'DificultadParaAutocontrol']).size().unstack().fillna(0)

st.subheader("Distribución de la dificultad para autocontrol por género")

# Gráfico de barras
fig, ax = plt.subplots()
conteo.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
plt.xlabel("Género")
plt.ylabel("Número de participantes")
plt.title("Dificultad para autocontrol por género")
st.pyplot(fig)

# Porcentaje por género
st.subheader("Porcentaje de dificultad para autocontrol por género")

porcentaje = conteo.div(conteo.sum(axis=1), axis=0) * 100
st.dataframe(porcentaje.round(2))
