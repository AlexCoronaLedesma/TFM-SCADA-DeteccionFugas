//PanelControl.cpp

#include "Arduino.h"
#include "PanelControl.h"


// Inicialización de la estructura global
EstadoDispositivos estadoDispositivos;


//Constantes empleadas
const int ERROR_ENTRADA_PANEL = 2;

const int TIEMPO_REBOTE_PRED = 50;

const int PARPADEO_LENTO = 0;
const int PARPADEO_RAPIDO = 1;
const int PARPADEO_ERROR = 2;

const unsigned long TIEMPO_PARPADEO_RAPIDO = 250;
const unsigned long TIEMPO_ON_PARPADEO_LENTO  = 500;
const unsigned long TIEMPO_OFF_PARPADEO_LENTO  = 1000;
const unsigned long TIEMPO_PARPADEO_ERROR  = 1500;

const float LED_UMBRAL_INF_INTERVALO1 = 0.10;
const float LED_UMBRAL_INF_INTERVALO2 = 0.30;
const float LED_UMBRAL_INF_INTERVALO3 = 0.60;
const float LED_UMBRAL_INF_INTERVALO4 = 0.75;
const float LED_UMBRAL_INF_INTERVALO5 = 0.90;

const int MAX_PWM = 255;
const float UMBRAL_25 = 0.25;
const float UMBRAL_50 = 0.50;
const float UMBRAL_75 = 0.75;





PanelControl::PanelControl(int Pin, int Tipo, String Nombre) {  
	_Pin = Pin;
	_Tipo = Tipo;     //INPUT o OUTPUT
	_EstadoAnterior = 0;
	_InstanteAnteriorRebote = 0;
	_TiempoRebote = TIEMPO_REBOTE_PRED;
  _Nombre = Nombre;
  
	pinMode(_Pin, _Tipo);
}


int PanelControl::ComprobarEstado() {
    if (_Tipo == INPUT) {
        if (_Nombre == "VaciadoTiempo") _EstadoActual = estadoDispositivos.VaciadoTiempo;
        else if (_Nombre == "VaciadoPulsacion") _EstadoActual = estadoDispositivos.VaciadoPulsacion;
        else if (_Nombre == "RecirculacionTiempo") _EstadoActual = estadoDispositivos.RecirculacionTiempo;
        else if (_Nombre == "RecirculacionPulsacion") _EstadoActual = estadoDispositivos.RecirculacionPulsacion;
        else if (_Nombre == "SelectorTara") _EstadoActual = estadoDispositivos.SelectorTara;
        else if (_Nombre == "SelectorCalibracion") _EstadoActual = estadoDispositivos.SelectorCalibracion;
        else if (_Nombre == "SelectorInicio") _EstadoActual = estadoDispositivos.SelectorInicio;
        else if (_Nombre == "Cierre") _EstadoActual = estadoDispositivos.Cierre;
        else if (_Nombre == "Bombeo") _EstadoActual = estadoDispositivos.Bombeo;
        else if (_Nombre == "Start") _EstadoActual = estadoDispositivos.Start;
        else if (_Nombre == "Stop") _EstadoActual = estadoDispositivos.Stop;
        else if (_Nombre == "Ejecucion") _EstadoActual = estadoDispositivos.Ejecucion;
        else if (_Nombre == "Emergencia") _EstadoActual = estadoDispositivos.Emergencia;
        else if (_Nombre == "AlturaFuga") _EstadoActual = estadoDispositivos.AlturaFuga;
        else if (_Nombre == "DimensionesFuga") _EstadoActual = estadoDispositivos.DimensionesFuga;
        else _EstadoActual = 0; // Valor por defecto

        Serial.print("Debug valor pin: ");
        Serial.print(_Nombre);
        Serial.println(_EstadoActual);
        return _EstadoActual;
    } else {
        return ERROR_ENTRADA_PANEL;
    }
}


int PanelControl::ComprobarFlanco(unsigned long InstanteActual) {
	//No hay "if (_Tipo == INPUT)" porque lo primero que hago aquí es invocar ComprobarEstado(), que ya tiene ese if
	
  _InstanteActual = InstanteActual;
	_EstadoActual = ComprobarEstado();

	if(_EstadoActual == _EstadoAnterior) {
    return 0;
  }

	if((_InstanteActual - _InstanteAnteriorRebote) < _TiempoRebote) {  
    return 0;                                                        
	}

	if(_EstadoActual > _EstadoAnterior) {
    _Flanco = 1;
  } else {
    _Flanco = -1;
  }

  _EstadoAnterior = _EstadoActual;
  _InstanteAnteriorRebote = _InstanteActual;

  return _Flanco;

}


int PanelControl::LeerValor() { // Para entradas analógicas
    if (_Tipo == INPUT) {
        if (_Nombre == "AlturaFuga") {
            _LecturaActual = estadoDispositivos.AlturaFuga;
        } else if (_Nombre == "DimensionesFuga") {
            _LecturaActual = estadoDispositivos.DimensionesFuga;
        } else {
            _LecturaActual = 0; // Valor por defecto para otras entradas
        }
        return _LecturaActual;
    } else {
        return ERROR_ENTRADA_PANEL;
    }
}



void PanelControl::Encender() {
    if (_Tipo == OUTPUT) {
        if (_Nombre == "LedInicializacion") estadoDispositivos.LedInicializacion = 1;
        else if (_Nombre == "LedFuncionamientoNormal") estadoDispositivos.LedFuncionamientoNormal = 1;
        else if (_Nombre == "LedPausa") estadoDispositivos.LedPausa = 1;
        else if (_Nombre == "LedEmergencia") estadoDispositivos.LedEmergencia = 1;
        else if (_Nombre == "LedDescargas") estadoDispositivos.LedDescargas = 1;
        else if (_Nombre == "LedAlmacenamiento") estadoDispositivos.LedAlmacenamiento = 1;
        else if (_Nombre == "LedVentas1") estadoDispositivos.LedVentas1 = 1;
        else if (_Nombre == "LedVentas2") estadoDispositivos.LedVentas2 = 1;
        else if (_Nombre == "LedFugas") estadoDispositivos.LedFugas = 1;
        Serial.print("Debug LED: ");
        Serial.print(_Nombre);
        Serial.println(_EstadoActual);
    }
}



void PanelControl::Apagar() {
    if (_Tipo == OUTPUT) {
        if (_Nombre == "LedInicializacion") estadoDispositivos.LedInicializacion = 1;
        else if (_Nombre == "LedFuncionamientoNormal") estadoDispositivos.LedFuncionamientoNormal = 1;
        else if (_Nombre == "LedPausa") estadoDispositivos.LedPausa = 1;
        else if (_Nombre == "LedEmergencia") estadoDispositivos.LedEmergencia = 1;
        else if (_Nombre == "LedDescargas") estadoDispositivos.LedDescargas = 1;
        else if (_Nombre == "LedAlmacenamiento") estadoDispositivos.LedAlmacenamiento = 1;
        else if (_Nombre == "LedVentas1") estadoDispositivos.LedVentas1 = 1;
        else if (_Nombre == "LedVentas2") estadoDispositivos.LedVentas2 = 1;
        else if (_Nombre == "LedFugas") estadoDispositivos.LedFugas = 1;
    }
}





void PanelControl::Parpadear(int TipoParpadeo, unsigned long InstanteActual) {  // El led parpadeará a distintas frecuencias en función del parámetro de entrada PARPADEO_RAPIDO, PARPADEO_LENTO o PARPADEO_ERROR.
                                    // Los tiempos son: TIEMPO_PARPADEO_RAPIDO = 250, TIEMPO_ON_PARPADEO_LENTO = 500, TIEMPO_OFF_PARPADEO_LENTO = 1000, TIEMPO_PARPADEO_ERROR = 1500
  
  _TipoParpadeo = TipoParpadeo;
  _InstanteActual = InstanteActual;

  if(_TipoParpadeo == PARPADEO_RAPIDO) {

    // Comprobar si ha pasado el tiempo suficiente para cambiar el estado del parpadeo, ya sea estando encendido o apagado
    if ((_InstanteActual - _InstanteUltimoCambioParpadeo) >= TIEMPO_PARPADEO_RAPIDO) {
      
      _ParpadeoEncendido = !_ParpadeoEncendido;  // Cambiar el estado del parpadeo
      _InstanteUltimoCambioParpadeo = _InstanteActual;  // Actualizar el tiempo del último cambio de estado

      if (_ParpadeoEncendido) {
        Encender(); 
        
      } else {
        Apagar();  
      }
    }
  

  } else if (_TipoParpadeo == PARPADEO_LENTO) {

    if ( ((_ParpadeoEncendido)  &&  ((_InstanteActual - _InstanteUltimoCambioParpadeo) >= TIEMPO_ON_PARPADEO_LENTO))   ||   (!_ParpadeoEncendido  &&  ((_InstanteActual - _InstanteUltimoCambioParpadeo) >= TIEMPO_OFF_PARPADEO_LENTO)) ) {
      
      _ParpadeoEncendido = !_ParpadeoEncendido;
      _InstanteUltimoCambioParpadeo = _InstanteActual;

      if (_ParpadeoEncendido) {
        Encender();
        
      } else {
        Apagar();
      }
    }

  } else if (_TipoParpadeo == PARPADEO_ERROR) {

    if ((_InstanteActual - _InstanteUltimoCambioParpadeo) >= TIEMPO_PARPADEO_ERROR) {
      
      _ParpadeoEncendido = !_ParpadeoEncendido;  
      _InstanteUltimoCambioParpadeo = _InstanteActual;  

      if (_ParpadeoEncendido) {
        Encender(); 
        
      } else {
        Apagar();  
      }
    }

  }


}






void PanelControl::EncenderPorNivel(float VolumenActual, float VolumenMax, unsigned long InstanteActual) {
  _RatioLlenado = VolumenActual / VolumenMax; 


  if (_RatioLlenado <= LED_UMBRAL_INF_INTERVALO1){    //Menos del 10%
    analogWrite(_Pin, 0);

  } else if ((_RatioLlenado > LED_UMBRAL_INF_INTERVALO1) && (_RatioLlenado <= LED_UMBRAL_INF_INTERVALO2)) {    //Dentro del 10 - 30% 
    analogWrite(_Pin, MAX_PWM * UMBRAL_25);

  } else if ((_RatioLlenado > LED_UMBRAL_INF_INTERVALO2) && (_RatioLlenado <= LED_UMBRAL_INF_INTERVALO3)) {    //Dentro del 30 - 60% 
    analogWrite(_Pin, MAX_PWM * UMBRAL_50);

  } else if ((_RatioLlenado > LED_UMBRAL_INF_INTERVALO3) && (_RatioLlenado <= LED_UMBRAL_INF_INTERVALO4)) {    //Dentro del 60 - 75% 
    analogWrite(_Pin, MAX_PWM * UMBRAL_75);

  } else if ((_RatioLlenado > LED_UMBRAL_INF_INTERVALO4) && (_RatioLlenado <= LED_UMBRAL_INF_INTERVALO5)) {    //Dentro del 75 - 90% 
    analogWrite(_Pin, MAX_PWM);

  }else if (_RatioLlenado > LED_UMBRAL_INF_INTERVALO5) {    //Más del 90% 
    Parpadear(PARPADEO_RAPIDO, InstanteActual);

  }
}


