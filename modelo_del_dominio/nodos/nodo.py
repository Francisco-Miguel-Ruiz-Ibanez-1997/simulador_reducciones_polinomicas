import qrcode
import qrcode.image.svg

###############################################################
# Clase Nodo que representa a un problema. Cada Nodo contendrá:
# id, nombre, alias (representativo del problema), color,
# información asociada y un código qr para ver más información
# sobre el problema.
###############################################################
class Nodo():

    # Constructor
    def __init__(self, id, nombre, alias, color, texto_info, url):

        self.id_nodo = id
        self.nombre = nombre
        self.alias = alias
        self.color = color
        self.texto_info = texto_info
        self.img_qr = self.crear_img_qr(url)
    
    ### Getters ###

    def get_id(self):
        return self.id_nodo

    def get_nombre(self):
        return self.nombre
    
    def get_alias(self):
        return self.alias

    def get_color(self):
        return self.color

    def get_texto_info(self):
        return self.texto_info
    
    def get_img_qr(self):
        return self.img_qr
    
    # Crea una imagen qr con la url pasada por parámetro.
    def crear_img_qr(self, url):

        data = url
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save("interfaz_grafica/interfaz_app/img/qr_" + self.nombre + ".png")

        return "interfaz_grafica/interfaz_app/img/qr_" + self.nombre + ".png"

