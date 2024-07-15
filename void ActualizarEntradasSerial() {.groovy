void ActualizarEntradasSerial() {
    
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Leer el comando recibido
        
        // Verificar si el comando es para la emergencia
        if (command.startsWith("Emergencia_Dash: ")) {
            String estado = command.substring(17);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoInterruptorEmergencia = 1;
            } else if (estado == "0") {
                EstadoInterruptorEmergencia = 0;
            }
        }

        // Verificar si el comando es para el selector de calibración
        if (command.startsWith("Estado_selector_calibracion: ")) {
            String estado = command.substring(29);  // Obtener el estado (1 o 2)
            if (estado == "1") {
                EstadoInterruptorCalibracion = 1;
            } else if (estado == "2") {
                EstadoInterruptorCalibracion = 0;
            }
        }

        // Verificar si el comando es para el selector de vaciado
        if (command.startsWith("Estado_selector_vaciado: ")) {
            String estado = command.substring(25);  // Obtener el estado (1, 2 o 3)
            if (estado == "1") {
                EstadoInterruptorVaciadoTiempo = 0;
                EstadoInterruptorVaciadoPulsacion = 1;
            } else if (estado == "2") {
                EstadoInterruptorVaciadoTiempo = 0;
                EstadoInterruptorVaciadoPulsacion = 0;
            } else if (estado == "3") {
                EstadoInterruptorVaciadoTiempo = 1;
                EstadoInterruptorVaciadoPulsacion = 0;
            }
        }

        // Verificar si el comando es para el selector de recirculación
        if (command.startsWith("Estado_selector_recirculacion: ")) {
            String estado = command.substring(31);  // Obtener el estado (1, 2 o 3)
            if (estado == "1") {
                EstadoInterruptorRecirculacionTiempo = 0;
                EstadoInterruptorRecirculacionPulsacion = 1;
            } else if (estado == "2") {
                EstadoInterruptorRecirculacionTiempo = 0;
                EstadoInterruptorRecirculacionPulsacion = 0;
            } else if (estado == "3") {
                EstadoInterruptorRecirculacionTiempo = 1;
                EstadoInterruptorRecirculacionPulsacion = 0;
            }
        }

        // Verificar si el comando es para el selector de tara
        if (command.startsWith("Estado_selector_tara: ")) {
            String estado = command.substring(22);  // Obtener el estado (1 o 2)
            if (estado == "1") {
                EstadoInterruptorTara = 1;
            } else if (estado == "2") {
                EstadoInterruptorTara = 0;
            }
        }

        // Verificar si el comando es para el selector de condiciones iniciales
        if (command.startsWith("Estado_selector_inicio: ")) {
            String estado = command.substring(24);  // Obtener el estado (1 o 2)
            if (estado == "1") {
                EstadoInterruptorCondIniciales = 1;
            } else if (estado == "2") {
                EstadoInterruptorCondIniciales = 0;
            }
        }

        // Verificar si el comando es para el botón de STOP
        if (command.startsWith("Stop_Dash: ")) {
            String estado = command.substring(11);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoPulsadorStop = 1;
            } else if (estado == "0") {
                EstadoPulsadorStop = 0;
            }
        }

        // Verificar si el comando es para el botón de START
        if (command.startsWith("Start_Dash: ")) {
            String estado = command.substring(12);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoPulsadorStart = 1;
            } else if (estado == "0") {
                EstadoPulsadorStart = 0;
            }
        }

        // Verificar si el comando es para el botón de BOMBEO
        if (command.startsWith("Bombeo_Dash: ")) {
            String estado = command.substring(13);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoPulsadorBombeo = 1;
            } else if (estado == "0") {
                EstadoPulsadorBombeo = 0;
            }
        }

        // Verificar si el comando es para el botón de EJECUCION
        if (command.startsWith("Ejecucion_Dash: ")) {
            String estado = command.substring(16);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoInterruptorManual = 1;
            } else if (estado == "0") {
                EstadoInterruptorManual = 0;
            }
        }

        // Verificar si el comando es para el botón de cierre
        if (command.startsWith("Cierre_Dash: ")) {
            String estado = command.substring(13);  // Obtener el estado (0 o 1)
            if (estado == "1") {
                EstadoInterruptorCierre = 1;
            } else if (estado == "0") {
                EstadoInterruptorCierre = 0;
            }
        }

        // Verificar si el comando es para la altura de fuga
        if (command.startsWith("Altura de fuga: ")) {
            String valor = command.substring(16);  // Obtener el valor después de "Altura de fuga: "
            LecturaPotenciometroAltura = valor.toInt();  // Convertir el valor a entero y almacenarlo
        }
      
        // Verificar si el comando es para las dimensiones de fuga
        else if (command.startsWith("Dimensiones de fuga: ")) {
            String valor = command.substring(21);  // Obtener el valor después de "Dimensiones de fuga: "
            LecturaPotenciometroDimensiones = valor.toInt();  // Convertir el valor a entero y almacenarlo
        }




    }
}







int estadoEmergencia = estadoDispositivos["Emergencia"];
int estadoCalibracion = estadoDispositivos["SelectorCalibracion"];