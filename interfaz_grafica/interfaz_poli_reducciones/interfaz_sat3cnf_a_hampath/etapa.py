#####################################################
# Clase padre de la que heredarán el resto de etapas.
#####################################################
class Etapa():
    def __init__(self, ventana, gestor_etapas):
        
        self.ventana = ventana
        self.gestor_etapas = gestor_etapas

        self.etapa_realizada = False
    
    def get_etapa_realizada(self):
        return self.etapa_realizada
    
    def set_etapa_realizada(self, valor):
        self.etapa_realizada = valor


    
    