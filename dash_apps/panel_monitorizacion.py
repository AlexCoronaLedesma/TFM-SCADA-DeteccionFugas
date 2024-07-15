from dash import Dash, dcc, html, Input, Output, callback, State,  dash_table
import plotly.graph_objs as go
import pandas as pd
from collections import deque
from utils.funciones_dash_monitorizacion import *
from utils.database import *
import logging
import paho.mqtt.client as mqtt


log_file = os.path.join('logs', 'panel_monitorizacion_logs.txt')

# Configurar el logger
logger = logging.getLogger('monitorizacion_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


dispense_values1 = deque(maxlen=20)
dispense_values2 = deque(maxlen=20)
dispense_values3 = deque(maxlen=20)
fuga_values = deque(maxlen=20) 
last_valid_data = None











# Configuración del cliente MQTT
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'proyecto/monitorizacion'
MQTT_USER = 'panel_monitorizacion'
MQTT_PASS = 'scada'
mqtt_data = None


def on_connect(client, userdata, flags, reason_code, properties=None):
    logger.info(f"Connected to MQTT Broker with result code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global mqtt_data
    mqtt_data = msg.payload.decode()
    logger.info(f"Received message: {mqtt_data}")

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()





# Inicializar la base de datos
db = DataBase()
logger.info("Base de datos inicializada")


# Crear la aplicación Dash
app = dash.Dash(__name__)
logger.info("Aplicación Dash creada")



############## Panel 1 - Estado de la planta ##############
def render_plant_state_panel():
    logger.info("Renderizando panel de estado de la planta")
    image_path = "/assets/prototipo-estructura.svg"
    image_content = html.Img(src=image_path, style={'width': '25%', 'height': '90vh', 'position': 'absolute'})
    
    
    return html.Div([  
            
            # Primera sección vertical (25% de ancho)
            html.Div([
                image_content,
                html.Div([
                    # Subsección 1.1
                    html.Div([
                       create_tank('DESCARGAS', 10, 0, 33, 120, 355, color=light_blue)
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'position': 'relative','height': '19vh'}),
                    # Subsección 1.2
                    html.Div([
                        create_tank('ALMACENAMIENTO', 10, 0, 125, 300, 280, color=light_blue)
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'position': 'relative', 'height': '42.6vh', 'align-items': 'center'}),
                    #Subsección 1.3
                    html.Div([
                        create_tank('VENTAS 1', 0, 0, 4, 100, 90, color=light_blue),
                        create_tank('VENTAS 2', 0, 0, 4, 100, 90, color=light_blue),
                        create_tank('FUGAS', 5, 0, 4, 100, 90, color=light_blue)
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center','gap': '40px', 'position': 'relative', 'height': '15.4vh', 'align-items': 'center'}),
                ]),
            ], style={'width': '25%','display': 'grid', 'grid-template-columns': '1fr', 'gap': '5px'}),
            
            
            # Segunda columna (75%)
        html.Div([
            # Sección horizontal superior dividida en tres contenedores
            html.Div([
                html.Div([
                    create_caudal_fuga_gauge() 
                ], style={'width': '30%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div([
                    dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in ["Depósito", "Prox. Dispensación", "Dispensaciones"]],
                                data=[{" ": "", "Prox. Dispensación": "Depósito", "Dispensaciones": ""} for _ in range(3)], 
                                style_cell={'textAlign': 'center', 'fontFamily': 'system-ui', 'fontSize': '18px', 'padding': '7px'},  
                                style_header={'font-size': '18px', 'fontWeight': 'bold'},
                                style_table={
                                    "width": "85%",
                                    "marginRight": "10px",
                                    "marginLeft": "0px",
                                },
                                
                                style_cell_conditional=[
                                    {'if': {'column_id': 'Depósito'},
                                    'font-size': '15px', 'fontWeight': 'bold'},
                                    {'if': {'column_id': 'Prox. Dispensación'},
                                    'font-size': '15px'},
                                    {'if': {'column_id': 'Dispensaciones'},
                                    'font-size': '15px'}
                                ]),
                ], style={'width': '50%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div([
                    dcc.Graph(id='fuga-chart') 
                ], style={'width': '40%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            ], style={'display': 'flex', 'height': '50vh'}),
            
            # Sección horizontal inferior dividida en dos contenedores
            html.Div([
                html.Div([
                    dcc.Graph(id='dispense-next-volumes-2-3')
                ], style={'width': '60%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div([
                    dcc.Graph(id='dispense-next-volumes-1')
                ], style={'width': '40%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            ], style={'display': 'flex', 'height': '30vh'}),
        
        ], style={'width': '75%','height': '100%','display': 'flex', 'flexDirection': 'column', 'gap': '15px'}),
    
    ], style={'display': 'flex','height': '100%','width': '100%'})
###########################################################


################## Panel 2 - Historicos ###################
def render_historic_panel():
    logger.info("Renderizando panel de históricos")
    return html.Div([
        # Contenedor del 20%
        html.Div([
            ## Opciones gráfico 1
            html.P('GRÁFICO 1', style={'font-weight': 'bold', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-around'}),
            html.Div([
                html.Img(src="/assets/calendario.svg", style={'width': '15%', 'height': '15vh'}),
                create_date_picker_range('date_picker_1')
            ], style={'height': '5%', 'font-weight': 'bold', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            
            html.Div([
                create_checklist('checklist_1')
            ], style={'height': '20%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            create_switch('graph_type_switch_1', "green"),
            
            ## Opciones gráfico 2
            html.P('GRÁFICO 2', style={'font-weight': 'bold', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-around'}),
            html.Div([
                html.Img(src="/assets/calendario.svg", style={'width': '15%', 'height': '15vh'}),
                create_date_picker_range('date_picker_2')
            ], style={'height': '5%', 'font-weight': 'bold', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            
            html.Div([
                create_checklist('checklist_2')
            ], style={'height': '20%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            create_switch('graph_type_switch_2', "blue"),

            html.Div([          
                create_button("Descargar CSV", "download-CSV-button"),
                dcc.Download(id="download-dataframe-csv"),
            ], style={'height': '10%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection': 'column'})

        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'height': '100vh'}),
    
        # Contenedor del 80%
        html.Div([
            html.Div([
                dcc.Graph(id='graph_1')
            ], style={'alignItems': 'center', 'justifyContent': 'center', 'height': '42vh'}),
            html.Div([
                dcc.Graph(id='graph_2')
            ], style={'alignItems': 'center', 'justifyContent': 'center', 'height': '42vh'}),
        ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    ], style={'width': '100%', 'display': 'flex', 'flexDirection': 'row', 'height': '90vh'})
###########################################################



######### Panel 3 - Depuracion, Alarmas y Alertas #########
def render_debug_panel():
    logger.info("Renderizando panel de depuración, alarmas y alertas")
    return html.Div([
        html.Div([
            create_button("Panel Mando Logs", "control-panel-button"),
            create_button("Panel Monitorización Logs", "monitorization-panel-button"),
            create_button("Conexión Serial Logs", "serial-connection-logs-button"),
            create_button("Database Logs", "database-logs-button"),
            create_button("Controladora Logs", "controller-logs-button"),
            create_button("Descargar Registro", "download-button"),
        ], style={'width': '20%','height': '80vh','display': 'grid', 'grid-template-rows': '1fr 1fr 1fr 1fr 1fr 1fr', 'gap': '5px'}),

        html.Div([
            dcc.Textarea(
                id='debug-messages',
                value='',
                style={
                    'width': '90%',
                    'height': '80vh',
                    'overflowY': 'scroll',
                    'whiteSpace': 'pre-wrap',
                    'backgroundColor': '#1e1e1e',
                    'color': '#d4d4d4',
                    'fontFamily': 'Courier New, monospace',
                    'padding': '20px',
                    'border': '1px solid #3c3c3c',
                    'borderRadius': '5px'
                }
            ),
        
        
        ], style={'width': '80%', 'float': 'left'}),
        
        dcc.Interval(id='debug-interval', interval=2000, n_intervals=0),
        dcc.Store(id='debug-store', data={'messages': [], 'current_display': 'debug'})

    ], style={'display': 'flex', 'flex-direction': 'row', 'height': '100vh'})
###########################################################



image_path_ull = "/assets/logo-ull.png"
image_content1 = html.Img(src=image_path_ull, style={'width': '10%','height': '5vh'})

# Layout de la aplicación
app.layout = html.Div([
    image_content1,
    dcc.Store(id='live-update-data'),
    dcc.Store(id='selected-log-file', data='logs/panel_mando_logs.txt'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Intervalo de 1 segundo
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Estado de la Planta', value='tab-1', selected_style={'font-weight': 'bold', 'font-size': '20px','background-color': 'lightblue'}, style={'font-size': '20px'}),
        dcc.Tab(label='Históricos', value='tab-2', selected_style={'font-weight': 'bold', 'font-size': '20px','background-color': 'lightblue'}, style={'font-size': '20px'}),
        dcc.Tab(label='Depuración, Alarmas y Alertas', value='tab-3', selected_style={'font-weight': 'bold', 'font-size': '20px','background-color': 'lightblue'}, style={'font-size': '20px'}),
    ]),
    html.Div(id='tabs-content')
])



# Callback para actualizar el contenido según la pestaña seleccionada
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def choose_panel(tab):
    logger.info(f"Seleccionando panel: {tab}")
    if tab == 'tab-1':
        return render_plant_state_panel()
    elif tab == 'tab-2':
        return render_historic_panel()
    elif tab == 'tab-3':
        return render_debug_panel()




@app.callback(Output('live-update-data', 'children'), Input('interval-component', 'n_intervals'))
def update_data(n):
    global historical_data, last_valid_data
    try:
        # Obtener los datos desde MQTT
        if mqtt_data:        
            logger.debug(f"Datos recibidos: {mqtt_data}")
            
            # Verificar que los datos sean válidos
            data_list = mqtt_data.split(',')
            if all(isinstance(d, (int, float)) for d in map(float, data_list)):
                logger.info("Datos válidos recibidos")
                last_valid_data = data_list  # Actualizar el último dato válido
                return mqtt_data  # Convertir los datos a una cadena separada por comas
            
            else:
                if last_valid_data:
                    return ','.join(map(str, last_valid_data))  # Devolver el último dato válido
                else:
                    return "Esperando datos..."  # Mensaje si no hay datos válidos disponibles
        
        else:
            if last_valid_data:
                return ','.join(map(str, last_valid_data))  # Devolver el último dato válido
            else:
                return "Esperando datos..."  # Mensaje si no hay datos disponibles
    
    except Exception as e:
        logger.error(f"Error de lectura: {e}")
        if last_valid_data:
            return ','.join(map(str, last_valid_data))  # Devolver el último dato válido en caso de error
        else:
            return f"Error de lectura: {e}"  # Mensaje de error si no hay datos válidos disponibles
    


###############################################################

##### CALLBACKS PARA ACTUALIZACION DE TANQUES #####
@app.callback(
    [Output('DESCARGAS', 'value'),
     Output('ALMACENAMIENTO', 'value'),
     Output('VENTAS 1', 'value'),
     Output('VENTAS 2', 'value'),
     Output('FUGAS', 'value'),
     Output('DESCARGAS', 'color'),
     Output('ALMACENAMIENTO', 'color'),
     Output('VENTAS 1', 'color'),
     Output('VENTAS 2', 'color'),
     Output('FUGAS', 'color')],
    Input('live-update-data', 'children')
)
def update_all_tanks(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        valores = [float(data_list[i]) for i in range(1, 6)]
        indicadores = [int(float(data_list[i])) for i in range(25, 30)]
        
        colores = [light_green if indicador == 1 else light_blue for indicador in indicadores]
        
        return valores + colores
    return [0, 0, 0, 0, 0, light_blue, light_blue, light_blue, light_blue, light_blue]  # Valores y colores por defecto


######## Callback para actualizar el caudal de fuga ###########
@app.callback(
    Output('caudal-fuga', 'value'),
    Input('live-update-data', 'children')
)
def update_caudal_fuga(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        caudal_fuga_value = float(data_list[20])  # Índice
        return caudal_fuga_value
###############################################################



@app.callback(Output('time', 'children'),
              [Input('live-update-data', 'children')])
def update_time(data):
    try:
        if data and "Error" not in data and "Esperando" not in data:
            data_list = data.split(',')
            ms_value = int(data_list[0])
            return "T = " + ms_to_time(ms_value)
        return "T = N/A"
    except (ValueError, IndexError) as e:
        logger.error(f"Error al convertir tiempo: {e}")
        return "T = N/A"


######## Callback para actualizar la tabla ###########
@app.callback(Output('table', 'data'),
              [Input('live-update-data', 'children')])
def update_table(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        next_dispense_times = data_list[13:16]
        dispense_counts = data_list[16:19]

        row_titles = ["Descargas", "Ventas1", "Ventas2"]
        table_data = [{"Depósito": row_titles[i], "Prox. Dispensación": ms_to_time(next_dispense_times[i]), "Dispensaciones": dispense_counts[i]} for i in range(3)]

        return table_data
    return []
##############################################################



########## CALLBACK PARA GENERAR GRAFICO VOLUMENES DE DESCARGA ##########
@app.callback(Output('dispense-next-volumes-1', 'figure'),
              [Input('live-update-data', 'children')])
def update_next_dispense_volumes_1(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        next_volumes = list(map(float, data_list[6:9]))
        dispense_values1.append(next_volumes[0])

        trace1 = go.Scatter(
            x=list(range(len(dispense_values1))),
            y=list(dispense_values1),
            name='Descargas',
            mode='lines+markers',
            line=dict(color='#2ECC71')
        )

        

        layout = go.Layout(
            title={'text': 'Volúmenes de descarga', 'y':0.85, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            title_font=dict(size=20),
            yaxis=dict(range=[0, None])
        )

        return {"data": [trace1], "layout": layout}
    return go.Figure()  # Devuelve una figura vacía si no hay datos válidos
##########################################################################





########## CALLBACK PARA GENERAR GRAFICO VOLUMENES DE VENTA ##########
@app.callback(Output('dispense-next-volumes-2-3', 'figure'),
              [Input('live-update-data', 'children')])
def update_next_dispense_volumes_2_3(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        next_volumes = list(map(float, data_list[6:9]))
        dispense_values2.append(next_volumes[1])
        dispense_values3.append(next_volumes[2])

        trace2 = go.Scatter(
            x=list(range(len(dispense_values2))),
            y=list(dispense_values2),
            name='Ventas 1',
            mode='lines+markers',
            line=dict(color='#00CCCC')
        )

        trace3 = go.Scatter(
            x=list(range(len(dispense_values3))),
            y=list(dispense_values3),
            name='Ventas 2',
            mode='lines+markers',
            line=dict(color='#FF5733')
        )

        layout = go.Layout(
            title={'text': 'Volúmenes de venta', 'y':0.85, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            title_font=dict(size=20),
            yaxis=dict(range=[0, None])
        )

        return {"data": [trace2, trace3], "layout": layout}
    return go.Figure()  # Devuelve una figura vacía si no hay datos válidos
##########################################################################




########## CALLBACK PARA GENERAR GRAFICO VOLUMENES DE FUGA ##########
@app.callback(Output('fuga-chart', 'figure'),
              [Input('live-update-data', 'children')])
def update_fuga_chart(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        next_fuga_volume = float(data_list[5])  
        fuga_values.append(next_fuga_volume)

        trace_fuga = go.Scatter(
            x=list(range(len(fuga_values))),
            y=list(fuga_values),
            name='Fugas',
            mode='lines+markers',
            line=dict(color='#8E44AD')
        )

        layout = go.Layout(
            title={'text': 'Volúmenes de fugas', 'y':0.85, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            title_font=dict(size=20),
            yaxis=dict(range=[0, None]),
        )

        return {"data": [trace_fuga], "layout": layout}
    return go.Figure()
##########################################################################





###################### CALLBACK GRAFICO 1 ######################
@app.callback(
    Output('graph_1', 'figure'),
    [
        Input('date_picker_1', 'start_date'),
        Input('date_picker_1', 'end_date'),
        Input('checklist_1', 'value'),
        Input('graph_type_switch_1', 'on')
    ]
)
def update_graph_1(start_date, end_date, selected_values, is_line_chart):
    # Cargar datos desde la base de datos
    df = load_csv()

    # Filtrar los datos por la fecha seleccionada
    if start_date:
        df = df[df['InstanteActual'] >= start_date]
    if end_date:
        df = df[df['InstanteActual'] <= end_date]

    # Crear trazos para el gráfico
    traces = create_traces(df, selected_values, is_line_chart)

    # Definir el layout del gráfico
    layout = go.Layout(
        title='Gráfico 1',
        xaxis=dict(title='Fecha', tickformat='%Y-%m-%d'),  # Solo se muestra la fecha
        yaxis=dict(title='Volumen'),
        height=400
    )

    # Devolver la figura final con los trazos y el layout
    return {'data': traces, 'layout': layout}
################################################################





###################### CALLBACK GRAFICO 2 ######################
@app.callback(
    Output('graph_2', 'figure'),
    [
        Input('date_picker_2', 'start_date'),
        Input('date_picker_2', 'end_date'),
        Input('checklist_2', 'value'),
        Input('graph_type_switch_2', 'on')
    ]
)
def update_graph_1(start_date, end_date, selected_values, is_line_chart):
    # Cargar datos desde la base de datos
    df = load_csv()

    # Filtrar los datos por la fecha seleccionada
    if start_date:
        df = df[df['InstanteActual'] >= start_date]
    if end_date:
        df = df[df['InstanteActual'] <= end_date]

    # Crear trazos para el gráfico
    traces = create_traces(df, selected_values, is_line_chart)

    # Definir el layout del gráfico
    layout = go.Layout(
        title='Gráfico 2',
        xaxis=dict(title='Fecha', tickformat='%Y-%m-%d'),  # Solo se muestra la fecha
        yaxis=dict(title='Volumen'),
        height=400
    )

    # Devolver la figura final con los trazos y el layout
    return {'data': traces, 'layout': layout}
################################################################



########### CALLBACK PARA DESCARGAR CSV CON TODOS LOS DATOS ###########
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-CSV-button", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    logger.debug("Descargando CSV con todos los datos")
    df = load_csv()
    return dcc.send_data_frame(df.to_csv, "data.csv")
########################################################################









########### CALLBACK PARA ACTUALIZAR EL AREA DE TEXTO DE LOS MENSAJES DEBUG ###########
@app.callback(
    Output('selected-log-file', 'data'),
    [Input('control-panel-button', 'n_clicks'),
     Input('monitorization-panel-button', 'n_clicks'),
     Input('serial-connection-logs-button', 'n_clicks'),
     Input('database-logs-button', 'n_clicks'),
     Input('controller-logs-button', 'n_clicks')]
)
def update_selected_log_file(control_clicks, monitor_clicks, serial_clicks, database_clicks, controller_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return 'logs/panel_mando_logs.txt'

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'control-panel-button':
        return 'logs/panel_mando_logs.txt'
    
    elif button_id == 'monitorization-panel-button':
        return 'logs/panel_monitorizacion_logs.txt'
    
    elif button_id == 'serial-connection-logs-button':
        return 'logs/serial_connection_logs.txt'
    
    elif button_id == 'database-logs-button':
        return 'logs/database_logs.txt'
    
    elif button_id == 'controller-logs-button':
        return 'logs/controladora_logs.txt'
    else:
        return 'logs/panel_mando_logs.txt'
########################################################################













####### Callback para actualizar el área de texto de los mensajes debug con interval_component ######
@app.callback(
    Output('debug-messages', 'value'),
    [Input('interval-component', 'n_intervals')],
    [State('selected-log-file', 'data')]
)
def update_debug_messages(n_intervals, selected_log_file):
    try:
        with open(selected_log_file, 'r') as file:
            logs = file.read()
            return logs
    except FileNotFoundError:
        return f"Error: {selected_log_file} no encontrado."
######################################################################################################





if __name__ == '__main__':
    app.run_server(debug=False)

