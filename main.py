import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo CSV
st.title("Visualización de Datos de Eventos Sísmicos")
uploaded_file = st.file_uploader("Cargar archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)

    # Convertir la columna de fecha a datetime si es necesario
    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y/%m/%d')

    # Título y descripción del archivo
    st.write("Datos cargados correctamente. Exploración de datos:")

    # Filtro por fecha
    start_date = st.date_input('Fecha de inicio', df['FECHA_UTC'].min())
    end_date = st.date_input('Fecha de fin', df['FECHA_UTC'].max())

    # Filtrar el DataFrame según las fechas seleccionadas
    df_filtered = df[(df['FECHA_UTC'] >= pd.to_datetime(start_date)) & (df['FECHA_UTC'] <= pd.to_datetime(end_date))]

    # Filtro por hora (si tienes una columna de hora)
    # Asumimos que 'FECHA_UTC' también contiene información de la hora
    df_filtered['HORA'] = pd.to_datetime(df['HORA_UTC'], format='%H:%M:%S').dt.time
    df_filtered['HORA'] = df_filtered['HORA'].apply(lambda x: x.hour)

    # Convertir la columna 'HORA' a tipo int de Python
    df_filtered['HORA'] = df_filtered['HORA'].apply(lambda x: int(x))

    # Usar el slider con los valores convertidos a int
    selected_hour_range = st.slider(
        'Filtrar por hora',
        min_value=int(df_filtered['HORA'].min()),  # Asegurarse de que sea un entero de Python
        max_value=int(df_filtered['HORA'].max()),  # Asegurarse de que sea un entero de Python
        value=(int(df_filtered['HORA'].min()), int(df_filtered['HORA'].max()))  # Asegurarse de que sea un entero de Python
    )

    # Filtrar el DataFrame según el rango de horas
    df_filtered = df_filtered[(df_filtered['HORA'] >= selected_hour_range[0]) & (df_filtered['HORA'] <= selected_hour_range[1])]

    # Mostrar los datos filtrados
    st.dataframe(df_filtered)

    # 1. Mapa de Dispersión Geográfica
    st.subheader("Distribución Geográfica de los Eventos")
    fig = px.scatter_geo(df_filtered, lat='LATITUD', lon='LONGITUD', color='MAGNITUD',
                         hover_name='FECHA_UTC', size='MAGNITUD',
                         title='Distribución Geográfica de los Eventos')
    st.plotly_chart(fig)

    # 2. Gráfico de Líneas para Profundidad vs. Fecha
    st.subheader("Profundidad de los Eventos a lo Largo del Tiempo")
    fig = px.line(df_filtered, x='FECHA_UTC', y='PROFUNDIDAD', title='Profundidad de los Eventos a lo Largo del Tiempo')
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Profundidad (km)')
    st.plotly_chart(fig)

    # 3. Gráfico de Dispersión de Magnitud vs. Profundidad
    st.subheader("Relación entre Profundidad y Magnitud")
    fig = px.scatter(df_filtered, x='PROFUNDIDAD', y='MAGNITUD', title='Relación entre Profundidad y Magnitud',
                     labels={'PROFUNDIDAD': 'Profundidad (km)', 'MAGNITUD': 'Magnitud'})
    st.plotly_chart(fig)

    # 4. Histograma de la Magnitud
    st.subheader("Distribución de la Magnitud de los Eventos")
    fig = px.histogram(df_filtered, x='MAGNITUD', nbins=20, title='Distribución de la Magnitud de los Eventos')
    fig.update_layout(xaxis_title='Magnitud', yaxis_title='Frecuencia')
    st.plotly_chart(fig)

    # 5. Gráfico de Barras de la Frecuencia Mensual de Eventos
    st.subheader("Frecuencia Mensual de Eventos")
    df_filtered['MES'] = df_filtered['FECHA_UTC'].dt.month
    fig = px.histogram(df_filtered, x='MES', title='Frecuencia Mensual de Eventos')
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Frecuencia',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                      'Noviembre', 'Diciembre']
        )
    )
    st.plotly_chart(fig)
