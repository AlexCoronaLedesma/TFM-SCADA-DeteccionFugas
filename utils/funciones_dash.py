import dash
from dash import dcc, html
from dash import Dash, html, Output, callback, State
import dash_daq as daq
from dash import html


states = ['1', '2', '3'] # Estados para los selectores

dark_blue = '#0000B8'
light_blue = '#4136FF'
black = '#000000'



##### Función para crear los indicadores #####
def indicadores(color: str, name: str):
    return html.Div([
        html.Div(name, style={'font-size': '24px', 'margin-top': '10px', 'margin-bottom': '20px'}),  # Estilo para el texto
        html.Div([
            daq.Indicator(id=name, value=True, color=color, size=75),
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'width': '75px', 'height': '75px', 
                  'border-radius': '50%', 'border': '4px solid black'}),   
    ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center' ,'margin-top': '10%'})



##### Función para crear los selectores #####
def create_selector(id: str, type: int):
    # Determinar el contenido específico basado en el tipo de selector (2 o 3 opciones)
    if type == 2:
        middle_children =[
                html.Div('Realizar', style={'font-size': '16px', 'text-align': 'center'}),
                html.Div(
                style={'display': 'flex', 'align-items': 'center', 'position': 'relative', 'width': '200px', 'height': '200px', 'justify-content': 'center'},
                children = [
                    html.Div(
                        id=f"{id}_svg",
                            children=[
                                html.Img(src='/assets/switch-knob-base2.svg', style={'width': '150px', 'height': '150px', 'position': 'absolute'}),
                                html.Img(src='/assets/switch-knob-perilla.svg', id=f"{id}_perilla", style={'width': '150px', 'height': '150px', 'position': 'absolute', 'transform': 'rotate(270deg)'})
                            ],
                            style={'position': 'relative', 'width': '200px', 'height': '200px', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    html.Button(id=f"{id}_button", style={'border-radius': '50px' ,'width': '100px', 'height': '100px','position': 'absolute', 'opacity': 0, 'cursor': 'pointer'})                     
                    ]
                ),
                html.Div('Saltar', style={'font-size': '16px', 'text-align': 'center'})
        ] 
    
    elif type == 3:
        middle_children =[
                html.Div('Realizar por Tiempo', style={'font-size': '16px', 'text-align': 'right'}),
                html.Div(
                style={'display': 'flex', 'align-items': 'center', 'position': 'relative', 'width': '200px', 'height': '200px', 'justify-content': 'center'},
                children = [
                    html.Div('Saltar', style={'font-size': '16px'}),
                    html.Div(
                        id=f"{id}_svg",
                            children=[
                                html.Img(src='/assets/switch-knob-base3.svg', style={'width': '150px', 'height': '150px', 'position': 'absolute'}),
                                html.Img(src='/assets/switch-knob-perilla.svg', id=f"{id}_perilla", style={'width': '150px', 'height': '150px', 'position': 'absolute', 'transform': 'rotate(270deg)'})
                            ],
                            style={'position': 'relative', 'width': '200px', 'height': '200px', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    html.Button(id=f"{id}_button", style={'border-radius': '50px' ,'width': '100px', 'height': '100px','position': 'absolute', 'left': '70px', 'opacity': 0, 'cursor': 'pointer', 'border': 'none'})                 
                    ]
                ),
                html.Div('Realizar por Pulsación', style={'font-size': '16px', 'text-align': 'right'})
        ]    

    return html.Div(
        id=f"{id}_container", style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'},
        children=[
            html.Div(id, style={'font-size': '24px', 'margin-top': '2px', 'margin-bottom': '50px'}),
            html.Div(
                children = middle_children
            ),
            #html.Button(id=f"{id}_button", style={'display': 'none'})
        ]
    )


##### Función para crear los pulsadores #####
default_button_style = {
    'border': 'none', 'color': 'white', 
    'padding': '15px', 'text-align': 'center', 
    'text-decoration': 'none', 'font-size': '20px',
    'display': 'inline-block', 
    'cursor': 'pointer',
    'border-radius': '50%',
    'width': '116px', 'height': '116px',        
    'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'
}

def create_button(name: str):
    return html.Div(
        style={'position': 'relative',  'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '200px', 'height': '200px'},
        children=[
            html.Img(src='/assets/pulsador.svg', style={'width': '100%', 'height': '100%'}),
            html.Button(
                name,
                id=name,
                n_clicks=0,
                style=default_button_style
            )
        ]
    )


##### Función para crear los interruptores #####
def create_switch(name: str, top_label: str, bottom_label: str, color: str):
    return html.Div(
        style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column', 'margin-bottom': '30px'},
        children=[
            html.Div(top_label, style={'font-size': '23px', 'text-align': 'center', 'margin-bottom': '75px'}),
            daq.BooleanSwitch(
                id=name,
                on=True,
                vertical=True,
                color=color,
                style={'transform': 'scale(3)'}
            ),
           html.Div(bottom_label, style={'font-size': '23px', 'text-align': 'center', 'margin-top': '75px'}),
        ]
    )


##### Función para crear los sliders y el display LED #####
def create_slider_with_display(label: str, id: str, default_value: int, element_side: str):
    # Verificar el lado especificado
    if element_side not in ['left', 'right']:
        raise ValueError("El lado del elemento debe ser 'left' o 'right'.")

    # Definir el estilo del contenedor dependiendo del lado del elemento
    container_style = {
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'margin': '10px'
    }
    if element_side == 'left':
        container_style['flex-direction'] = 'row'
    else:
        container_style['flex-direction'] = 'row-reverse'

    # Estilo para agregar espacio entre el slider y el display
    slider_container_style = {'margin-right': '20px'} if element_side == 'left' else {'margin-left': '20px'}

    # Estilo para las marcas del slider
    slider_marks = {i: {'label': str(i), 'style': {'color': 'black', 'fontSize': '14px'}} for i in range(0, 101, 10)}

    return html.Div(
        style=container_style,
        children=[
            html.Div(
                style=slider_container_style,
                children=[
                    dcc.Slider(
                        id=f'{id}-slider',
                        min=0,
                        max=100,
                        step=5,
                        value=default_value,
                        vertical=True,
                        marks=slider_marks,
                        included=True,
                        updatemode='drag',
                        verticalHeight=400,
                    )
                ]
            ),
            html.Div(
                style={'text-align': 'center'},
                children=[
                    html.Div(
                        label,
                        style={'color': 'black', 'font-size': '20px', 'margin-bottom': '10px'}  # Estilo del texto del nombre
                    ),
                    daq.LEDDisplay(
                        id=f'{id}-display',
                        value=str(default_value),  # Asegurarse de que el valor se pase como string
                        style={'font-size': '36px', 'color': '#00AEEF'},
                    )
                ]
            )
        ]
    )



##### Función para crear la seta de emergencia #####
def create_emergency_button(png_path):
    button_color = '#FF4136'  # Color rojo

    return html.Div(
        style={
            'display': 'flex',
            'justify-content': 'center',  # Centrado horizontal
            'align-items': 'center',  # Centrado vertical
            'height': '100%',  
        },
        children=[
            html.Div(
                id='our-round-button',
                style={
                    'width': '250px',
                    'height': '250px',
                    'background-image': f"url('{png_path}')",
                    'background-size': 'cover',
                    'background-repeat': 'no-repeat',
                    'background-position': 'center',
                    'position': 'relative',  # Posición relativa para el botón
                },
                children=[
                    html.Button(
                        id='emergency_button',
                        children='PE',
                        style={
                            'width': '75px',
                            'height': '75px',
                            'borderRadius': '50%',
                            'border': 'none',
                            'backgroundColor': 'red',
                            'cursor': 'pointer',
                            'color': 'black',
                            'fontSize': '30px',
                            'position': 'absolute',  
                            'left': '52%', 
                            'top': '50%',  
                            'transform': 'translate(-50%, -50%)', 
                        }
                    ),
                ]
            ),
            html.Div(id='round-button-result')
        ]
    )



