import streamlit as st
from PIL import Image
import pandas as pd
from ALBA_Functions import factoreo



# Cargar posibles imágenes (si las tuvieras)
# icon_colones = Image.open("Bancos_Colones.png")
# icon_dolares = Image.open("Bancos_Dolares.png")

# Definición de cada página como función

st.logo("pictures/ALBA_Logo_large.jpg",size="large")

def introduccion():
    st.title("Introducción")
    st.subheader("Informe Financiero - Junio 2025")
    st.write(
        "A continuación se presenta el informe financiero de ALBA Global al 30 de junio de 2025. "
        "Se presenta el estado de operación del Factoreo y la información de los movimientos bancarios."
    )
    #st.markdown("### Esta es la página de introducción donde puedes colocar tu descripción general.")




def bancos_en_colones():
    st.image("Pictures/Bancos_Colones.png")
    st.title("Bancos en Colones")
    # st.image(icon_colones, width=40)  # Descomenta si cargas iconos
    st.write(
        "En esta sección mostramos información relevante de los bancos que operan en colones costarricenses."
    )
    # Ejemplo de contenido
    bancos = [
        {"Nombre": "Banco de Costa Rica", "Activo_total": "₡10.000M"},
        {"Nombre": "BAC San José", "Activo_total": "₡7.500M"},
        {"Nombre": "BNCR S.A.", "Activo_total": "₡9.200M"},
    ]
    st.table(bancos)


def bancos_en_dolares():
    st.image("Pictures/Bancos_Dolares.png")
    st.title("Bancos en Dólares")
    # st.image(icon_dolares, width=40)  # Descomenta si cargas iconos
    st.write(
        "En esta sección mostramos información relevante de los bancos que operan en dólares estadounidenses."
    )
    # Ejemplo de contenido
    bancos_usd = [
        {"Nombre": "Citibank", "Activo_total": "$5.000M"},
        {"Nombre": "Scotiabank", "Activo_total": "$4.300M"},
        {"Nombre": "BNCR USD", "Activo_total": "$3.800M"},
    ]
    st.table(bancos_usd)

# Diccionario de páginas
pages = {
    "Introducción": introduccion,
    "Factoreo": factoreo,
    "Bancos en Colones": bancos_en_colones,
    "Bancos en Dólares": bancos_en_dolares,
}

# Sidebar para navegación
st.sidebar.title("Contenido")
st.image("Pictures/ALBA_Logo.jpg")
seleccion = st.sidebar.radio("", list(pages.keys()))

# Ejecutar la página seleccionada
pages[seleccion]()
