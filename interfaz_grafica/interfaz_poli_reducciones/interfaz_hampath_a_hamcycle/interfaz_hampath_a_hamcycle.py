from ...interfaz_app.ventanas.ventanas_hijas.ventana_secundaria import VentanaSecundaria

from interfaz_grafica.interfaz_poli_reducciones.interfaz_poli_reduccion import InterfazPoliReduccion

from .gestor_etapas import GestorEtapas

######################################################################
# Clase que contiene la interfaz gráfica asociada a la poli-reducción
# HAMPATH -> HAMCYCLE.
######################################################################
class InterfazHampathHamcycle(InterfazPoliReduccion):


    # Constructor.
    def __init__(self, nombre_poli_reduccion, ventana):


        self._nombre = nombre_poli_reduccion
        self._ventana = ventana

    # Método que contiene la poli-reducción de HAMPATH a HAMCYCLE.
    def lanzar_interfaz_poli_reduccion(self, lista_resultados_previos):
        
        # Creamos una ventana en la que mostraremos cómo se va realizando la poli-reducción
        ventana_poli_reduccion = VentanaSecundaria(self._ventana)

        ventana_poli_reduccion.geometry("")
        ventana_poli_reduccion.configure(background="#9AA4B0")
        ventana_poli_reduccion.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_poli_reduccion.title("Poli-reducción de HAMPATH a HAMCYCLE. HAMCYCLE es NP-Completo")

        gestor_etapas = GestorEtapas(ventana_poli_reduccion, lista_resultados_previos)

        # Lanzamos etapa informativa (subetapa 0 de etapa 0)
        gestor_etapas.get_etapa(0).lanzar_subetapa_0()

        ventana_poli_reduccion.center()
        ventana_poli_reduccion.mainloop()