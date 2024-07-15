from dash_apps.panel_mando import app as app_mando
from dash_apps.panel_monitorizacion import app as app_monitorizacion
import threading
import os

# Crear el directorio de logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

def run_app(app, port):
    app.run_server(debug=False, port=port)

if __name__ == "__main__":
    threading.Thread(target=run_app, args=(app_mando, 8050)).start()
    threading.Thread(target=run_app, args=(app_monitorizacion, 8051)).start()
