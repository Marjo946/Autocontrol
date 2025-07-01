import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Dificultad para Autocontrol según el Género")

# Cargar los datos desde 'Datos.csv'
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("Datos.csv")
        # Validar que existan las columnas necesarias
        if 'Genero' not in df.columns or 'DificultadParaAutocontrol' not in df.columns:
            st.error("❌ Las columnas 'Genero' y 'DificultadParaAutocontrol' no se encuentran en el archivo.")
            return pd.DataFrame()  # Retorna un DataFrame vacío
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # Renombrar los valores para mejor visualización
    df['Genero'] = df['Genero'].replace({1: 'Hombre', 2: 'Mujer'})
    df['DificultadParaAutocontrol'] = df['DificultadParaAutocontrol'].replace({0: 'Ausente', 1: 'Presente'})

    # Mostrar los datos si el usuario lo desea
    if st.checkbox("Mostrar datos"):
        st.write(df[['Genero', 'DificultadParaAutocontrol']])

    # Conteo por género
    conteo = df.groupby(['Genero', 'DificultadParaAutocontrol']).size().unstack().fillna(0)

    st.subheader("Distribución de la dificultad para autocontrol por género")

    fig, ax = plt.subplots()
    conteo.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
    plt.xlabel("Género")
    plt.ylabel("Número de participantes")
    plt.title("Dificultad para autocontrol por género")
    st.pyplot(fig)

    # Porcentaje
    st.subheader("Porcentaje de dificultad para autocontrol por género")
    porcentaje = conteo.div(conteo.sum(axis=1), axis=0) * 100
    st.dataframe(porcentaje.round(2))
