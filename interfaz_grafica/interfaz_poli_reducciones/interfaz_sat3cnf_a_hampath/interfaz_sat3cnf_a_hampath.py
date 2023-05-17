from ...interfaz_app.ventanas.ventanas_hijas.ventana_secundaria import VentanaSecundaria

from ..interfaz_poli_reduccion import InterfazPoliReduccion

from .gestor_etapas import GestorEtapas

######################################################################
# Clase que contiene la interfaz gráfica asociada a la poli-reducción
# SAT3cnf -> HAMPATH.
######################################################################
class InterfazSat3cnfAHampath(InterfazPoliReduccion):

    def __init__(self, nombre, ventana):

        self._nombre = nombre
        self._ventana = ventana

    # Lanza la interfaz
    def lanzar_interfaz_poli_reduccion(self, lista_resultados_previos):

        # Creamos una ventana en la que mostraremos cómo se va realizando la poli-reducción
        ventana_poli_reduccion = VentanaSecundaria(self._ventana)

        ventana_poli_reduccion.geometry("")
        ventana_poli_reduccion.configure(background="#9AA4B0")
        ventana_poli_reduccion.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_poli_reduccion.title("Poli-reducción de SAT3cnf a HAMPATH. HAMPATH es NP-Completo")

        # Creamos el controlador de etapas
        self.gestor_etapas = GestorEtapas(ventana_poli_reduccion)

        # Lanzamos etapa informativa (subetapa 0 de etapa 0)
        self.gestor_etapas.get_etapa(0).lanzar_subetapa_0()

        ventana_poli_reduccion.center()
        ventana_poli_reduccion.mainloop()


        






