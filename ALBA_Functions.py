import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale
locale.setlocale(locale.LC_ALL, 'es_CR.UTF-8')  # o 'es_ES.UTF-8'



def factoreo():
    df_factoreo = pd.read_excel("Tabla_BD_Factoreo.xlsx")
    df_factoreo = df_factoreo.loc[:,["Zona","Factura","Fecha de pago a emisor","Ingreso neto","Neto a cobrar","Pagos recibidos","Saldo por cobrar"]]
    df_factoreo.rename(columns={'Fecha de pago a emisor': 'Fecha',
                                "Ingreso neto":"Ingreso",
                                "Neto a cobrar":"A_cobrar",
                                "Pagos recibidos":"Cobros",
                                "Saldo por cobrar":"Saldo",
                                }, inplace=True)
    
    # Convertir la columna 'Fecha' a tipo datetime (día/mes/año)
    #df_excel['Fecha'] = pd.to_datetime(df_excel['Fecha'], dayfirst=True, errors='coerce')
    df_factoreo["Fecha"] = pd.to_datetime(df_factoreo["Fecha"], dayfirst=True, errors="coerce")
    for col in ["Ingreso", "A_cobrar", "Cobros", "Saldo"]:
        df_factoreo[col] = pd.to_numeric(df_factoreo[col], errors="coerce")
    
    # Mostrar gráfico Gauge de indicador de Factoreo
    st.image("Pictures/Factoreo.png")
    st.title("Factoreo")
    # st.image(icon_colones, width=40)  # Descomenta si cargas iconos
    
    st.write(
        "A continuación se presenta el detalle del estado de la gestión de factoreo:"
    )
    
    

    # Contenedor de gráfico de barras de ingreso por mes
    # ===============================================================================
    
    
    # Crear gráfico de barras con seaborn
    # Agrupar por mes
    df_grouped = df_factoreo.set_index('Fecha').resample('ME')['Ingreso'].sum().reset_index()
    df_grouped['Mes'] = df_grouped['Fecha'].dt.strftime('%Y-%m')

    fig1 = plt.figure(figsize=(10, 6))
    sns.barplot(x='Mes', y='Ingreso', data=df_grouped)

    # Etiquetas y formato
    plt.xlabel('Mes')
    plt.ylabel('Ingreso')
    plt.title('Ingreso Mensual')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Gráfico por zona
    df_zone = df_factoreo.groupby('Zona')['Ingreso'].sum().reset_index()
    
    # Calcular porcentaje del total
    total_ingreso = df_zone['Ingreso'].sum()
    df_zone['Porcentaje'] = df_zone['Ingreso'] / total_ingreso * 100
    
    # Convertir ingreso a millones de colones
    df_zone['Ingreso_Millones'] = df_zone['Ingreso'] / 1e6
    
    # Preparar etiquetas para el pie chart
    labels = [
    f"{zona}: {im:.2f} MM ({por:.1f}%)"
    for zona, im, por in zip(
        df_zone['Zona'],
        df_zone['Ingreso_Millones'],
        df_zone['Porcentaje'])
        ]
    sizes = df_zone['Ingreso']

    # Crear gráfico de pie
    fig2 = plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, startangle=90)
    plt.title('Distribución de Ingresos por Zona')
    plt.axis('equal')  # Para que el pie sea un círculo
    

    # Mostrar gráfico
    
    container_Chart_Ingresos = st.container(border=True)

    with container_Chart_Ingresos:
        a, b, c  = st.columns(3)
        
        with a:
            st.image("Pictures/TAE_Factoreo.png")

        with b:
            st.pyplot(fig1)
        
        with c:
            st.pyplot(fig2)
        
    container_metrics = st.container(border=True)

    with container_metrics:
        col1, col2, col3 = st.columns(3) 
        col1.metric("Ingresos", "11.5 ¢MM", "2.4 ¢MM")
        col2.metric("Rendimiento", "28.48%", "0.7%")
        col3.metric("Recup. prom.", "90 días", "2 días")        
        #st.write("Hola")
        #st.pyplot(plt)

    # Contenedor base de datos
    #with container_BD:
    #    st.dataframe(df_factoreo)
    container_BD = st.container(border=True)
   
    with container_BD:
        """
        st.dataframe(
            df_factoreo,
            hide_index=True,
            column_config={
                "Fecha": st.column_config.DateColumn(
                    "Fecha",
                    format="DD-MMM-YYYY"     # 21-Ene-2025
                ),
                "Ingreso": st.column_config.NumberColumn(
                    "Ingreso",
                    format="¢ %,.2f"          # ¢ 36,963.09
                ),
                "A_cobrar": st.column_config.NumberColumn(
                    "A cobrar",
                    format="¢ %,.2f"
                ),
                "Cobros": st.column_config.NumberColumn(
                    "Cobros",
                    format="¢ %,.0f"          # sin decimales
                ),
                "Saldo": st.column_config.NumberColumn(
                    "Saldo",
                    format="¢ %,.2f"
                ),
            },
            use_container_width=True,
        )
        """

        df_fmt = df_factoreo.copy()

        def colones(x, dec=2):
            if pd.isna(x):      # evita problemas con NaN
                return ""
            return locale.currency(x, symbol='₡', grouping=True).replace(u'\xa0', u' ')

        for col in ["Ingreso", "A_cobrar"]:
            df_fmt[col] = df_fmt[col].apply(lambda v: colones(v, dec=2))

        df_fmt["Cobros"] = df_fmt["Cobros"].apply(lambda v: colones(v, dec=0))

        # La fecha ya la tienes con DateColumn; si prefieres texto:
        # df_fmt["Fecha"] = df_fmt["Fecha"].dt.strftime("%d-%b-%Y")

        st.table(df_fmt)  # o st.dataframe(df_fmt, hide_index=True)
        
        #use_container_width=True,


