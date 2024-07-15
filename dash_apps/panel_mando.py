import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from utils.funciones_dash import *
from utils.theme import *
from utils.serial_connection import *
import logging
import os

log_file = os.path.join('logs', 'panel_mando_logs.txt')

# Configurar el logger
logger = logging.getLogger('panel_mando_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/panel_mando_logs.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


led_inicializacion_value = 0
led_funcionamiento_normal_value = 0  
led_pausa_cierre_value = 0  
led_fuga_detectada_value = 0


# Inicializar la aplicación Dash
app = dash.Dash(__name__)
logger.info("Aplicación Dash creada")


# Definir el diseño del panel de mando
app.layout = daq.DarkThemeProvider(
    children=[
    # Contenedor pantalla completa
    html.Div([
        dcc.Store(id='live-update-data'),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
        html.Div([
            # Primera sección vertical (70% de ancho)
            html.Div([
                html.Div([
                    
                    # Subsección 1.1
                    html.Div([
                        indicadores("purple", "Inicialización"),
                        indicadores("blue", "Funcionamiento Normal"),
                        indicadores("yellow", "Pausa - Cierre"),
                        indicadores('red', 'Emergencia'),
                        indicadores('red', "FUGA DETECTADA"),
                    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr 1fr 1fr', 'gap': '1px','height': '25vh'}),
                    
                    # Subsección 1.2
                    html.Div([
                        create_selector('VACIADO', 3),
                        create_selector('RECIRCULACIÓN',3),
                        create_selector('TARA',2),
                        create_selector('CALIBRACIÓN',2),
                        create_selector('CONDICIONES INICIALES',2),
                    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr 1fr 1fr', 'gap': '1px','height': '40vh', 'align-items': 'center'}),
                    
                    #Subsección 1.3
                    html.Div([
                        create_button('BOMBEO'),
                        create_button('START'),
                        create_button('STOP'),
                        html.Div(
                            'EJECUCIÓN',
                            style={'font-size': '23px', 'text-align': 'center', 'position': 'absolute', 'top': '75%', 'left': '48%','transform': 'rotate(-90deg)',}
                        ),
                        create_switch('Ejecucion','Manual','Automática', "blue"),
                        html.Div(
                            'CIERRE',
                            style={'font-size': '23px', 'text-align': 'center', 'position': 'absolute', 'top': '75%', 'left': '65%','transform': 'rotate(-90deg)',}
                        ),
                        create_switch('Cierre','Realizar','No realizar', "green"),
                    ], style={'align-items': 'center', 'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr 1fr 1fr', 'gap': '7.5%','height': '25vh', 'padding': '0 4.5%'}),
               
                ], style={'grid-template-rows': '1fr 1fr 1fr'}),
            ], style={'width': '80%', 'margin-right': '10px','display': 'grid', 'grid-template-columns': '1fr', 'gap': '5px'}),

            # Segunda sección vertical (30% de ancho)
            html.Div([
                html.Div([
                    #Subsección 2.1
                    html.Div([
                        create_slider_with_display('Altura de fuga', 'slider1', 5, 'left'),
                        create_slider_with_display('Dimensiones de fuga', 'slider2', 7, 'right'),  
                    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '1px'}),
                    
                    #Subsección 2.2
                    html.Div([
                        create_emergency_button("/assets/BOT-010.png")
                    ], style={'display': 'grid', 'grid-template-columns': '1fr', 'gap': '1px'}),
                
                ], style={'display': 'grid', 'grid-template-rows': '2.2fr 1fr', 'gap': '5px'}),
            ], style={'width': '20%','display': 'grid', 'grid-template-columns': '1fr', 'gap': '5px'}),
        
        ], style={'display': 'flex', 'width': '100%', 'height': '100%', 'justify-content': 'space-between'}),
    ], style={'display': 'flex','height': '100%','width': '100%'})    #'backgroundColor': '#6E6E6E'
    ])


######## CALLBACK PARA RECIBIR LOS DATOS DEL ARDUINO ########
@app.callback(Output('live-update-data', 'children'), Input('interval-component', 'n_intervals'))
def update_data(n):
    try:
        data = get_serial_data()
        if data:
            return ','.join(map(str, data))
        else:
            logger.warning("No se recibieron datos válidos")
            return "Esperando datos..."
    except Exception as e:
        logger.error(f"Error de lectura: {e}")
        return f"Error de lectura: {e}"
###############################################################
    


######## CALLBACKS PARA LOS LEDS INDICADORES DEL MODO ########
@app.callback(
    [Output('Inicialización', 'value'),
     Output('Funcionamiento Normal', 'value'),
     Output('Pausa - Cierre', 'value'),
     Output('FUGA DETECTADA', 'value')],
    [Input('live-update-data', 'children')]
)

def update_leds(data):
    if data and "Error" not in data and "Esperando" not in data:
        data_list = data.split(',')
        led_inicializacion_value = float(data_list[21])  
        led_funcionamiento_normal_value = float(data_list[22])
        led_pausa_cierre_value = float(data_list[23])  
        led_fuga_detectada_value = float(data_list[24])
        logger.debug(f"Datos leds: {led_inicializacion_value}, {led_funcionamiento_normal_value}, {led_pausa_cierre_value}, {led_fuga_detectada_value}")

    return [
        led_inicializacion_value,
        led_funcionamiento_normal_value, 
        led_pausa_cierre_value,
        led_fuga_detectada_value
    ]
################################################################





######## CALLBACKS PARA LOS SELECTORES TRIPLES ########

# Selector de VACIADO
@app.callback(
    Output('VACIADO_perilla', 'style'),
    Input('VACIADO_button', 'n_clicks')
)
def update_rotation_VACIADO(n_clicks):
    if n_clicks is None:
        ser.write(("Estado_selector_vaciado: " + str(1)).encode())
        return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer','transform': 'rotate(270deg)'}
    rotations = ['rotate(270deg)', 'rotate(0deg)', 'rotate(90deg)']

    current_state = n_clicks % 3
    ser.write(("Estado_selector_vaciado: " + str(states[current_state])  + '\n').encode())
    logger.debug(f"Estado selector VACIADO: {states[current_state]}")
    
    return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer', 'transform': rotations[n_clicks % 3]}

    

# Selector de RECIRCULACIÓN
@app.callback(
    Output('RECIRCULACIÓN_perilla', 'style'),
    Input('RECIRCULACIÓN_button', 'n_clicks')
)
def update_rotation_RECIRCULACIÓN(n_clicks):
    if n_clicks is None:
        ser.write(("Estado_selector_recirculacion: " + str(1)).encode())
        return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer','transform': 'rotate(270deg)'}
    rotations = ['rotate(270deg)', 'rotate(0deg)', 'rotate(90deg)']
    
    current_state = n_clicks % 3
    ser.write(("Estado_selector_recirculacion: " + str(states[current_state])  + '\n').encode())
    logger.debug(f"Estado selector RECIRCULACIÓN: {states[current_state]}")
    
    return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer', 'transform': rotations[n_clicks % 3]}

########################################################





######## CALLBACKS PARA LOS SELECTORES DOBLES ########

# Definir los callbacks para rotar la perilla de TARA
@app.callback(
    Output('TARA_perilla', 'style'),
    [Input('TARA_button', 'n_clicks')]
)
def update_rotation_TARA(n_clicks):
    if n_clicks is None:
        ser.write(("Estado_selector_tara: " + str(1)).encode())
        return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer','transform': 'rotate(270deg)'}
    rotations = ['rotate(270deg)', 'rotate(90deg)']
    
    current_state = n_clicks % 2
    ser.write(("Estado_selector_tara: " + states[current_state]  + '\n').encode())
    logger.debug(f"Estado selector TARA: {states[current_state]}")

    return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer', 'transform': rotations[n_clicks % 2]}


# Definir los callbacks para rotar la perilla de CALIBRACIÓN
@app.callback(
    Output('CALIBRACIÓN_perilla', 'style'),
    [Input('CALIBRACIÓN_button', 'n_clicks')]
)
def update_rotation_CALIBRACIÓN(n_clicks):
    if n_clicks is None:
        ser.write(("Estado_selector_calibracion: " + str(1)).encode())
        return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer','transform': 'rotate(270deg)'}
    rotations = ['rotate(270deg)', 'rotate(90deg)']
    
    current_state = n_clicks % 2
    ser.write(("Estado_selector_calibracion: " + states[current_state] + '\n').encode())
    logger.debug(f"Estado selector CALIBRACIÓN: {states[current_state]}")
    
    return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer', 'transform': rotations[n_clicks % 2]}


# Definir los callbacks para rotar la perilla de CONDICIONES INICIALES
@app.callback(
    Output('CONDICIONES INICIALES_perilla', 'style'),
    [Input('CONDICIONES INICIALES_button', 'n_clicks')]
)
def update_rotation_inicio(n_clicks):
    if n_clicks is None:
        ser.write(("Estado_selector_inicio: " + str(1)).encode())
        return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer','transform': 'rotate(270deg)'}
    rotations = ['rotate(270deg)', 'rotate(90deg)']
    
    current_state = n_clicks % 2
    ser.write(("Estado_selector_inicio: " + states[current_state]  + '\n').encode())
    logger.debug(f"Estado selector CONDICIONES INICIALES: {states[current_state]}")

    return {'width': '150px', 'height': '150px', 'position': 'absolute', 'cursor': 'pointer', 'transform': rotations[n_clicks % 2]}
########################################################




###### CALLBACKS DE LA PARADA DE EMERGENCIA ######
@app.callback(
    Output('emergency_button', 'style'),
    [Input('emergency_button', 'n_clicks')]
)
def update_button_style(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    
    dark_red = '#B80000'
    light_red = '#FF4136'
    black = '#000000'
    # Cambiar el color del botón alternativamente entre rojo claro y oscuro
    if n_clicks % 2 == 0:
        button_style = {
            'width': '76px',
            'height': '76px',
            'borderRadius': '50%',
            'border': 'none',
            'background': f'radial-gradient(circle, {light_red} 30%, {black} 100%)',  # Gradiente radial desde el centro al borde
            'color': 'black',
            'fontSize': '30px',
            'position': 'absolute',  # Cambiado a posición absoluta
            'left': '51%',  # Mover al centro horizontal
            'top': '50%',  # Mover al centro vertical
            'transform': 'translate(-50%, -50%)',  # Corrección para centrar
        }
    else:
        button_style = {
            'width': '76px',
            'height': '76px',
            'borderRadius': '50%',
            'border': 'none',
            'background': f'radial-gradient(circle, {dark_red} 30%, {black} 100%)', 
            'color': 'black',
            'fontSize': '30px',
            'position': 'absolute',  # Cambiado a posición absoluta
            'left': '51%',  # Mover al centro horizontal
            'top': '50%',  # Mover al centro vertical
            'transform': 'translate(-50%, -50%)',  # Corrección para centrar
        }

    return button_style

@app.callback(
    Output('Emergencia', 'value'),
    Input('emergency_button', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    # Determinar el estado de emergencia
    Emer_Dash_status = 0 if n_clicks % 2 == 0 else 1
    
    # Enviar el estado por el puerto serie
    ser.write(("Emergencia_Dash: " + str(Emer_Dash_status) + '\n').encode())
    logger.debug(f"Estado de emergencia: {Emer_Dash_status}")
    
    return Emer_Dash_status
##################################################












###### CALLBACKS DEL BOTÓN DE BOMBA ######
@app.callback(
    Output('BOMBEO', 'style'),
    [Input('BOMBEO', 'n_clicks')]
)
def update_button_style(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    
    # Cambiar el color del botón alternativamente entre azul claro y oscuro
    if n_clicks % 2 == 0:
        button_style = style={
            'background': f'radial-gradient(circle, {light_blue} 30%, {black} 100%)',  # Gradiente radial desde el centro al borde
        }
    else:
        button_style = {
            'background': f'radial-gradient(circle, {dark_blue} 30%, {black} 100%)', 
        }

    # Combinar el estilo actualizado con el estilo por defecto
    combined_style = default_button_style.copy()
    combined_style.update(button_style)

    return combined_style

@app.callback(
    Output('BOMBEO', 'value'),
    Input('BOMBEO', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    # Determinar el estado de bombeo
    Bombeo_Dash_status = 0 if n_clicks % 2 == 0 else 1
    
    # Enviar el estado por el puerto serie
    ser.write(("Bombeo_Dash: " + str(Bombeo_Dash_status) + '\n').encode())   #Para enviarlo con el formato Bombeo_Dash: 0
    logger.debug(f"Estado BOMBA: {Bombeo_Dash_status}")

    return Bombeo_Dash_status
##################################################





###### CALLBACKS DEL BOTÓN DE START ######
@app.callback(
    Output('START', 'style'),
    [Input('START', 'n_clicks')]
)
def update_button_style(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    
    # Cambiar el color del botón alternativamente entre claro y oscuro
    if n_clicks % 2 == 0:
        button_style = style={
            'background': f'radial-gradient(circle, {light_blue} 30%, {black} 100%)',  # Gradiente radial desde el centro al borde
        }
    else:
        button_style = {
            'background': f'radial-gradient(circle, {dark_blue} 30%, {black} 100%)', 
        }

    # Combinar el estilo actualizado con el estilo por defecto
    combined_style = default_button_style.copy()
    combined_style.update(button_style)

    return combined_style

@app.callback(
    Output('START', 'value'),
    Input('START', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    # Determinar el estado de START
    START_Dash_status = 0 if n_clicks % 2 == 0 else 1
    
    # Enviar el estado por el puerto serie
    ser.write(("Start_Dash: " + str(START_Dash_status) + '\n').encode())
    logger.debug(f"Estado START: {START_Dash_status}")

    return START_Dash_status
##################################################





###### CALLBACKS DEL BOTÓN DE STOP ######
@app.callback(
    Output('STOP', 'style'),
    [Input('STOP', 'n_clicks')]
)
def update_button_style(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    
    # Cambiar el color del botón alternativamente entre claro y oscuro
    if n_clicks % 2 == 0:
        button_style = style={
            'background': f'radial-gradient(circle, {light_blue} 30%, {black} 100%)',
        }
    else:
        button_style = {
            'background': f'radial-gradient(circle, {dark_blue} 30%, {black} 100%)', 
        }

    # Combinar el estilo actualizado con el estilo por defecto
    combined_style = default_button_style.copy()
    combined_style.update(button_style)

    return combined_style

@app.callback(
    Output('STOP', 'value'),
    Input('STOP', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    # Determinar el estado de STOP
    STOP_Dash_status = 0 if n_clicks % 2 == 0 else 1
    
    # Enviar el estado por el puerto serie
    ser.write(("Stop_Dash: " + str(STOP_Dash_status) + '\n').encode())
    logger.debug(f"Estado STOP: {STOP_Dash_status}")

    return STOP_Dash_status
##################################################



###### CALLBACKS DEL BOTÓN DE EJECUCION ######
@app.callback(
    Output('Ejecucion', 'on'),
    Input('Ejecucion', 'on')
)
def update_boolean_switch(on):
    # Enviar el estado por el puerto serie
    Ejecucion_Dash_status = 1 if on else 0
    ser.write(("Ejecucion_Dash: " + str(Ejecucion_Dash_status) + '\n').encode())
    logger.debug(f"Estado EJECUCION: {Ejecucion_Dash_status}")
    
    return on
##################################################


###### CALLBACKS DEL BOTÓN DE CIERRE ######
@app.callback(
    Output('Cierre', 'on'),
    Input('Cierre', 'on')
)
def update_boolean_switch(on):
    # Enviar el estado por el puerto serie
    Cierre_Dash_status = 1 if on else 0
    ser.write(("Cierre_Dash: " + str(Cierre_Dash_status) + '\n').encode())
    logger.debug(f"Estado CIERRE: {Cierre_Dash_status}")

    return on
##################################################




# Callback para actualizar los valores de los displays LED y enviar datos por el puerto serie
@app.callback(
    [Output('slider1-display', 'value'),
     Output('slider2-display', 'value')],
    [Input('slider1-slider', 'value'),
     Input('slider2-slider', 'value')]
)
def update_displays_and_send_data(slider1_value, slider2_value):
    # Convertir los valores de los sliders a cadenas
    slider1_str = str(slider1_value)
    slider2_str = str(slider2_value)
    
    # Convertir los valores de porcentaje a un rango de 0 a 1023
    slider1_scaled = int(slider1_value * 1023 / 100)
    slider2_scaled = int(slider2_value * 1023 / 100)

    try:
        # Enviar los datos por el puerto serie
        ser.write((f"Altura de fuga: {slider1_scaled}\n").encode())
        ser.write((f"Dimensiones de fuga: {slider2_scaled}\n").encode())
        logger.debug(f"Datos enviados - Altura de fuga: {slider1_scaled}, Dimensiones de fuga: {slider2_scaled}")
    except serial.SerialTimeoutException as e:
        logger.error(f"Error enviando datos por el puerto serie: {e}")
    
    # Devolver los valores para actualizar los displays
    return slider1_str, slider2_str

if __name__ == '__main__':
    app.run_server(debug=False)



















# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=False)