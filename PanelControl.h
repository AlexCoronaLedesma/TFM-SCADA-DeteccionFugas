//PanelControl.h

#ifndef PanelControl_h
#define PanelControl_h

#include "Arduino.h"

// Estructura para almacenar los estados de los dispositivos
struct EstadoDispositivos {
    int VaciadoTiempo;
    int VaciadoPulsacion;
    int RecirculacionTiempo;
    int RecirculacionPulsacion;
    int SelectorTara;
    int SelectorCalibracion;
    int SelectorInicio;
    int Cierre;
    int Bombeo;
    int Start;
    int Stop;
    int Ejecucion;
    int Emergencia;
    int AlturaFuga;
    int DimensionesFuga;
    int LedInicializacion;
    int LedFuncionamientoNormal;
    int LedPausa;
    int LedEmergencia;
    int LedDescargas;
    int LedAlmacenamiento;
    int LedVentas1;
    int LedVentas2;
    int LedFugas;
};

extern EstadoDispositivos estadoDispositivos;


class PanelControl {
	private:
		int _Pin;
		int _Tipo;
		int _EstadoActual;
		int _EstadoAnterior;
		int _Flanco;
    unsigned long _InstanteActual;
		unsigned long _TiempoRebote;
    unsigned long _InstanteAnteriorRebote;

    int _LecturaActual;

    int _TipoParpadeo;
    bool _ParpadeoEncendido;
    unsigned long _InstanteUltimoCambioParpadeo;
    unsigned long _TiempoEncendidoParpadeo;
    unsigned long _TiempoApagadoParpadeo;
    float _RatioLlenado;

    String _Nombre; // Nombre del dispositivo en el diccionario

    //const  
    const int ERROR_ENTRADA_PANEL;

    const int TIEMPO_REBOTE_PRED;

    const int PARPADEO_LENTO ;
    const int PARPADEO_RAPIDO;
    const int PARPADEO_ERROR;

    const unsigned long TIEMPO_PARPADEO_RAPIDO;
    const unsigned long TIEMPO_ON_PARPADEO_LENTO;
    const unsigned long TIEMPO_OFF_PARPADEO_LENTO;
    const unsigned long TIEMPO_PARPADEO_ERROR;

    const float LED_UMBRAL_INF_INTERVALO1;
    const float LED_UMBRAL_INF_INTERVALO2;
    const float LED_UMBRAL_INF_INTERVALO3;
    const float LED_UMBRAL_INF_INTERVALO4;
    const float LED_UMBRAL_INF_INTERVALO5;
		


	public:
		PanelControl(int Pin, int Tipo, String Nombre);
		int ComprobarEstado();  //Int porque se devuelvo un 2 en caso de error
		int ComprobarFlanco(unsigned long InstanteActual);
    int LeerValor();
		void Encender();
		void Apagar();
    void Parpadear(int TipoParpadeo, unsigned long InstanteActual);
    void EncenderPorNivel(float VolumenActual, float VolumenMax, unsigned long InstanteActual);

};





#endif