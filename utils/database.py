import pandas as pd
import time
import os
import logging
from dash import dcc
from dash import Dash, html, Input, Output, callback



log_file = os.path.join('logs', 'database_logs.txt')

# Configurar el logger
logger = logging.getLogger('database_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



# Ruta del csv
file_path = 'data_sample.csv'



def load_csv():
    if os.path.exists(file_path):
        logger.info(f"Cargando datos desde {file_path}.")
        return pd.read_csv(file_path)
    else:
        logger.error(f"El archivo {file_path} no existe.")
        return pd.DataFrame()

class DataBase:
    def __init__(self, sample_interval=6, output_file=file_path):
        self.columns = [
            "InstanteActual", "VolumenDescargas", "VolumenAlmacenamiento", "VolumenVentas1", "VolumenVentas2",
            "VolumenFugas", "ProxVolumenDescargas", "ProxVolumenVentas1", "ProxVolumenVentas2",
            "VolumenAcumuladoDescargas", "VolumenAcumuladoVentas1", "VolumenAcumuladoVentas2", "VolumenAcumuladoFugas",
            "InstanteProxDispDescargas", "InstanteProxDispVentas1", "InstanteProxDispVentas2",
            "RecargasTotalesDescargas", "RecargasTotalesVentas1", "RecargasTotalesVentas2",
            "AlturaFuga", "CaudalFuga"
        ]
        self.output_file = output_file
        self.sample_interval = sample_interval
        self.last_sample_time = None  # Para asegurar que se guarde el primer dato inmediatamente
        
        # Cargar datos existentes si el archivo ya existe
        if os.path.exists(self.output_file):
            logger.info(f"Cargando datos existentes desde {self.output_file}.")
            self.df = pd.read_csv(self.output_file)
        else:
            logger.info(f"Archivo {self.output_file} no encontrado. Creando un nuevo DataFrame.")
            self.df = pd.DataFrame(columns=self.columns)
            

    def add_data(self, data):
        current_time = time.time()
        logger.info(f"Datos recibidos: {data}")  # Verificar los datos recibidos

        # Asegurarse de que los datos tengan la longitud correcta
        if data and len(data) >= len(self.columns):
            data = data[:len(self.columns)]  # Truncar los datos si hay más elementos de los necesarios
            if self.last_sample_time is None or (current_time - self.last_sample_time) >= self.sample_interval:
                data[0] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')  # Reemplaza el valor de InstanteActual con la fecha y hora actual
                try:
                    self.df.loc[len(self.df)] = data
                    logger.info("Datos añadidos al DataFrame correctamente.")
                    self.save_to_csv()
                    self.last_sample_time = current_time
                    logger.info(f"Datos guardados en el archivo {self.output_file}.")
                except Exception as e:
                    logger.error(f"Error al añadir los datos al DataFrame o al guardar el archivo CSV: {e}")
            else:
                logger.info("El intervalo de muestreo no se ha cumplido. No se añadirán datos.")
        else:
            logger.error(f"Los datos no son válidos o no coinciden con las columnas esperadas. Datos recibidos: {data}, Columnas esperadas: {self.columns}")

    def save_to_csv(self):
        try:
            self.df.to_csv(self.output_file, index=False)
            logger.info(f"Datos guardados correctamente en {self.output_file}.")
        except Exception as e:
            logger.error(f"Error al guardar los datos en {self.output_file}: {e}")