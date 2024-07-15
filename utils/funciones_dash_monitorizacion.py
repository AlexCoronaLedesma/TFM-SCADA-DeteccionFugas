import dash
from dash import dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import pandas as pd
import logging
import plotly.graph_objects as go
import os

light_blue = '#B3CDE0'
light_green = '#B3E2CD'

def ms_to_time(ms):
    ms = float(ms)
    seconds = (ms / 1000) % 60
    seconds = int(seconds)
    minutes = (ms / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (ms / (1000 * 60 * 60)) % 24

    time_format = "%02d:%02d:%02d" % (hours, minutes, seconds)
    logging.debug(f"Converted time: {time_format}")
    return time_format



def read_debug_log():
    with open('debug.log', 'r') as file:
        lines = file.readlines()
    return lines


##### Función para crear los tanques #####
def create_tank(id, value, min_val, max_val, height, width, color=light_blue):
    return daq.Tank(
        id=id,
        value=value,
        showCurrentValue=True,
        units='Litros',
        label=id, 
        labelPosition='top',
        min=min_val,
        max=max_val,
        height=height,
        width=width,
        color=color,
        #color="#FFA07A", 
       style={
            'position': 'relative',
            'font-weight': 'bold',
            'text-color': 'red'
        },
    )
##############################################


##### Función para crear los botones #####
def create_button(name: str, id: str):
    return html.Button(
        name,  
        id=id,  
        style={
            'fontSize': '16px',
            'margin': '5px',
            'font-weight': 'bold',
            'padding': '10px',
            'cursor': 'pointer',
            'backgroundColor': 'lightblue',
            'borderRadius': '5px'
        }
    )
##############################################






##############################################
def create_caudal_fuga_gauge(value=0):
    return daq.Gauge(
        id='caudal-fuga',
        showCurrentValue=True,
        label={'label': 'Caudal de Fuga', 'style': {'fontSize': 20}},
        units="%",
        value=value,
        max=100,
        min=0,
        size=250,
        scale={'start': 0, 'interval': 10, 'labelInterval': 1, 'labelStyle': {'fontSize': 24}},
        color={
            "gradient": True,
            "ranges": {
                "green": [0, 50],
                "yellow": [50, 80],
                "red": [80, 100]
            },
            "default": "#0000FF"  # Color del indicador del valor (azul)
        },
        style={'margin': 'auto', 'padding': '20px', 'width': '50%','detail': '#0000FF'}
    )
##############################################



##############################################
def create_pie(volumenes_acumulados):
        labels = ['Descargas', 'Ventas 1', 'Ventas 2', 'Fugas']
        fig = px.pie(values=volumenes_acumulados, names=labels, title='Distribución de Volúmenes Acumulados', hole=0.3)
        fig.update_traces(
            textinfo='percent+label',
            textfont_size=12,
            textfont_color='black',
            textposition='inside'
        )
        fig.update_layout(
            title={
                'text': 'Distribución de Volúmenes Acumulados',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend=dict(
                orientation="v",
                yanchor="middle",
                 y=0.5,
                xanchor="left",
                x=-0.5
            ),
            margin=dict(l=20, r=20, t=0, b=5),
            height=400,
            width=450
        )
        return fig
##############################################



##############################################
def create_date_picker_range(date_picker_id):
    return dcc.DatePickerRange(
        id=date_picker_id,
        start_date_placeholder_text='Fecha inicio',
        end_date_placeholder_text='Fecha fin',
        display_format='DD-MM-YYYY',
        start_date_id='start-date-id',
        end_date_id='end-date-id',
        min_date_allowed='2024-06-01',
        max_date_allowed='2025-12-31',
        clearable=True,
        with_portal=True
    )
##############################################



##############################################
def create_checklist(checklist_id):
    return dcc.Checklist(
        id=checklist_id,
        options=[
            {'label': 'Volumen Inicial', 'value': 'a'},
            {'label': 'Volumen Final', 'value': 'b'},
            {'label': 'Volumen Descargas', 'value': 'c'},
            {'label': 'Volumen Almacenamiento', 'value': 'd'},
            {'label': 'Volumen Ventas 1', 'value': 'e'},
            {'label': 'Volumen Ventas 2', 'value': 'f'},
            {'label': 'Volumen Fugas', 'value': 'g'},
            {'label': 'Variación Fugas', 'value': 'h'}
        ],
        value=['a'],
        style={'color': 'black', 'fontSize': '20px'}
    )
##############################################


##### Función para crear los interruptores #####
def create_switch(name: str, color: str):
    return daq.DarkThemeProvider(
        children=[
            html.Div(
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',  'margin-bottom': '30px', 'margin-top': '20px'},
                children=[
                    html.Div('BARRAS', style={'font-size': '15px', 'text-align': 'center', 'margin-right': '15px'}),
                    daq.BooleanSwitch(
                        id=name,
                        on=True,
                        color=color,
                    ),
                    html.Div('LÍNEAS', style={'font-size': '15px', 'text-align': 'center', 'margin-left': '15px'}),
                ]
            )
        ]
    )
##############################################



######################################################
def create_traces(df, selected_values, is_line_chart):
  
    # Convertir la columna 'InstanteActual' a datetime
    df['InstanteActual'] = pd.to_datetime(df['InstanteActual'])

    # Agrupar por día 
    df_grouped = df.groupby(df['InstanteActual'].dt.date)

    # Calcular volumen inicial y final
    first_volumes = df_grouped.first()[['VolumenAlmacenamiento']]
    last_volumes = df_grouped.last()[['VolumenAlmacenamiento']]


    # Calcular los datos acumulados
    df_grouped_sum = df_grouped.sum(numeric_only=True)


    # Calcular el volumen teórico final
    volumen_ventas = df_grouped_sum['VolumenVentas1'] + df_grouped_sum['VolumenVentas2']
    volumen_teorico_final = first_volumes + volumen_ventas

    # Calcular la variación de volumen debida a fugas
    variacion_fugas = last_volumes['VolumenAlmacenamiento'] - volumen_teorico_final

    # Lista para almacenar los trazos del gráfico
    traces = []

    # Diccionario para mapear los valores seleccionados con las columnas del dataframe
    columns_map = {
        'a': 'VolumenAlmacenamiento',  # Volumen Inicial
        'b': 'VolumenAlmacenamiento',  # Volumen Final
        'c': 'VolumenDescargas',
        'd': 'VolumenAlmacenamiento',
        'e': 'VolumenVentas1',
        'f': 'VolumenVentas2',
        'g': 'VolumenFugas',
        'h': 'VariacionFugas' 
    }

    # Crear trazos solo para las columnas seleccionadas
    for value in selected_values:
        if value == 'a':
            if is_line_chart:
                trace = go.Scatter(
                    x=first_volumes.index.astype(str),          # Convertir el índice a cadena para mostrar solo la fecha
                    y=first_volumes['VolumenAlmacenamiento'],
                    mode='lines+markers',
                    name='Volumen Inicial'
                )
            else:
                trace = go.Bar(
                    x=first_volumes.index.astype(str),
                    y=first_volumes['VolumenAlmacenamiento'],
                    name='Volumen Inicial'
                )
        elif value == 'b':
            if is_line_chart:
                trace = go.Scatter(
                    x=last_volumes.index.astype(str),
                    y=last_volumes['VolumenAlmacenamiento'],
                    mode='lines+markers',
                    name='Volumen Final'
                )
            else:
                trace = go.Bar(
                    x=last_volumes.index.astype(str),
                    y=last_volumes['VolumenAlmacenamiento'],
                    name='Volumen Final'
                )
        elif value == 'h':
            if is_line_chart:
                trace = go.Scatter(
                    x=variacion_fugas.index.astype(str),
                    y=variacion_fugas,
                    mode='lines+markers',
                    name='Variacion Fugas'
                )
            else:
                trace = go.Bar(
                    x=variacion_fugas.index.astype(str),
                    y=variacion_fugas,
                    name='Variacion Fugas'
                )
        
        
        elif value in columns_map:
            if is_line_chart:
                trace = go.Scatter(
                    x=df_grouped_sum.index.astype(str),  
                    y=df_grouped_sum[columns_map[value]],
                    mode='lines+markers',
                    name=columns_map[value]
                )
            else:
                trace = go.Bar(
                    x=df_grouped_sum.index.astype(str), 
                    y=df_grouped_sum[columns_map[value]],
                    name=columns_map[value]
                )
        traces.append(trace)


    return traces
######################################################


