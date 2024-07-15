import serial
import logging
import time
import threading
import os
import paho.mqtt.client as mqtt



log_file = os.path.join('logs', 'serial_connection_logs.txt')
log_file1 = os.path.join('logs', 'controladora_logs.txt')

# Configurar el logger para la conexión serial
logger = logging.getLogger('serial_logger')
logger.setLevel(logging.DEBUG)
file_handler_serial = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_serial.setFormatter(formatter)
logger.addHandler(file_handler_serial)

# Configurar el logger para los mensajes de depuración
logger_arduino = logging.getLogger('controladora_logger')
logger_arduino.setLevel(logging.DEBUG)
file_handler_debug = logging.FileHandler(log_file1)
file_handler_debug.setFormatter(formatter)
logger_arduino.addHandler(file_handler_debug)

# Variable global para almacenar la última lectura válida
global last_valid_data
last_valid_data = []



############### FUNCION PARA ESTABLECER LA COMUNICACIÓN SERIAL ###############
def start_serial_connection():
    puerto_com = 'COM11'
    ser = None
    while ser is None:
        try:
            ser = serial.Serial(puerto_com, 9600, timeout=1)
            logger.info("Conexión serial establecida en %s", puerto_com)
        except Exception as e:
            logger.error("Error en start_serial_connection: %s", e)
            time.sleep(1)  # Espera un segundo antes de intentar nuevamente
    return ser
################################################################################




############### FUNCION PARA LEER DEL PUERTO SERIAL ###############
def read_from_serial(ser, last_valid_data):
    global mensajes_debug  # Se almacenan las líneas que no son numéricas

    try:
        if ser is not None:
            line = ser.readline().decode('utf-8').strip()
            logger.debug("Línea recibida: %s", line)

            # Comprobamos si la línea empieza con "Debug"
            if line.startswith("Debug"):
                # Registrar la línea en el archivo de logs de depuración
                logger_arduino.debug("Línea: %s", line)
                return last_valid_data
            else:
                # Si no, se intenta convertir cada elemento a float
                data = line.split(',')
                try:
                    cleaned_data = [float(item) for item in data]
                    last_valid_data = cleaned_data  # Se guarda la data válida como la última válida
                    logger.debug("Data: %s", cleaned_data)
                    
                   # Convertir cleaned_data a una cadena separada por comas
                    cleaned_data_str = ','.join(map(str, cleaned_data))
                    
                    # Enviar los datos a través de MQTT
                    mqtt_client.publish(MQTT_TOPIC, cleaned_data_str)
                    logger.debug("Datos enviados por MQTT: %s", cleaned_data_str)                           
                    
                    return cleaned_data
                except ValueError:
                    logger.warning("No se puede convertir los datos a float. Datos: %s", data)
                    return last_valid_data  # Si hay un error, devolvemos la última data válida
                
        else:
            logger.warning("Conexión serial no establecida")
            return last_valid_data  # Si no hay conexión, devolvemos la última data válida
    except Exception as e:
        logger.error("Error leyendo del puerto serie: %s", e)
        return last_valid_data  # Si hay un error general, devolvemos la última data válida
################################################################################



def clean_data(line):
    """Limpia y valida los datos recibidos de la línea serial"""
    data = line.split(',')
    # Validar que tenemos la cantidad correcta de datos y que todos son números
    if len(data) == 30 and all(d.isdigit() for d in data):
        return data
    return None


global ser
ser = start_serial_connection()

def get_serial_data():
    return data

def continuously_read_serial_data():
    global data
    while True:
        data = read_from_serial(ser, last_valid_data)
        logger.info(f"Datos arduino: {data}")  # Mostrar datos en la consola y en el log
        time.sleep(1)




# Iniciar el hilo para leer los datos del puerto serie continuamente
serial_thread = threading.Thread(target=continuously_read_serial_data)
serial_thread.daemon = True  # Esto asegura que el hilo se cerrará cuando el programa principal termine
serial_thread.start()



################## IMPLEMENTACION MQTT ##################

# Variable global para almacenar los datos recibidos
mqtt_data = []

# Configuración del broker MQTT y autenticación
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'proyecto/monitorizacion'
MQTT_USER = 'tu_usuario'
MQTT_PASS = 'tu_contraseña'


# Función que se llama al conectarse al broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPIC)  # Suscribirse al tópico definido


# Función que se llama al recibir un mensaje
def on_message(client, userdata, msg):
    print(f"Message received-> {msg.topic} {msg.payload}")


# Configuración del cliente MQTT
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)  # Establecer usuario y contraseña
mqtt_client.on_connect = on_connect 
mqtt_client.on_message = on_message 


# Conectarse al broker y empezar el bucle
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()


# Función para publicar mensajes al tópico MQTT
def publish_to_mqtt(message):
    mqtt_client.publish(MQTT_TOPIC, message)








