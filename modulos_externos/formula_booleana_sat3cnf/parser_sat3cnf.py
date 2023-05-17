from sly import Lexer, Parser
import tkinter as tk
import customtkinter as ctk
import tkinter.font as tkfont
from PIL import ImageTk, Image

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

# https://stackoverflow.com/questions/63667899/python-precedence-order-syntaxerror-in-certain-not-and-expressions
# https://sly.readthedocs.io/en/latest/sly.html

########################################################
# Clase del analizador léxico. Hereda de la clase Lexer.
########################################################

class FormBoolLexer(Lexer):
    
    def __init__(self):
        super().__init__()
        self.lista_caracteres_erroneos = []
        self.error_lexico = False
        self.index = 0

    # Tokens a reconocer
    tokens = { LITERAL, AND, OR, NOT,
               LPAREN, RPAREN }

    # Cadena que contiene los tokens a ignorar
    ignore = ' \t'

    # Expresiones regulares para los tokens.
    # Importante establecer el orden. Toma el primer token reconocido. No obstante, como son exclusivos
    # los tokens unos con los otros, aquí no importa el orden
    LITERAL = r'x[1-9]'
    AND     = r'\^'
    OR      = r'v'
    NOT     = r'\!'
    LPAREN  = r'\('
    RPAREN  = r'\)'

    # Función manejadora de errores. Recabamos todos los errores léxicos para posteriormente mostrarlos por
    # pantalla.
    def error(self, t):
        self.lista_caracteres_erroneos.append("\'" + t.value[0] +"\'" + "   ")
        self.error_lexico = True
        self.index += 1

#   El lenguaje que recoge la estructura de las fórmulas booleanas 3-cnf introducidas se puede expresar como:
#   expr :  
#       (term) ^ expr
#       | (term)
#   
#   term :
#       factor v factor v factor
#       | factor v factor
#       | factor
#
#   factor :
#       LITERAL
#       | NOT LITERAL
#

#############################################################
# Clase del analizador sintáctico. Hereda de la clase Parser.
#############################################################
class FormBoolParser(Parser):

    def __init__(self):
        super().__init__()
        self.error_sintactico_general = False
        self.error_sintactico_en_pos = -1

    # Fichero reducciones (solución de conflictos, etc) realizadas en el parser
    #debugfile = 'parser.out'

    # Obtenemos la lista de tokens del analizador léxico
    tokens = FormBoolLexer.tokens
   
    # Reglas gramaticales. Definimos la gramática de nuestro lenguaje.
    @_('LPAREN term RPAREN AND expr')
    def expr(self, p):
        pass
    
    @_('LPAREN term RPAREN')
    def expr(self, p):
        pass

    @_('factor OR factor OR factor')
    def term(self, p):
        pass
    
    @_('factor OR factor')
    def term(self, p):
        pass

    @_('factor')
    def term(self, p):
        pass

    @_('LITERAL')
    def factor(self, p):
        pass

    @_('NOT LITERAL')
    def factor(self, p):
        pass

    # Función manejadora de errores. Guarda la posición en la que se da el error sintático (en caso de que lo encuentre),
    # o simplemente se activa un flag para indicar que ha habido error sintático, pero no sabe en dónde.
    def error(self, p):
        if p:
           self.error_sintactico_en_pos = p.index
        else:
            self.error_sintactico_general = True

############################################################
### Métodos que llaman al analizador sintáctico y léxico ###
############################################################

# Muestra mensaje de error indicando el error léxico cometido.
def mostrar_mensaje_error_lexico(ventana, cadena_error):

    panel = ctk.CTkFrame(ventana, corner_radius=0) 
    panel.pack(fill = "both", expand=True)

    label = ctk.CTkLabel(panel, text='Error léxico en los caracteres: ')
    label.grid(row=1,column=0, padx=10, pady=10)

    label = ctk.CTkLabel(panel, text=cadena_error, font=ctk.CTkFont(weight="bold"),
                            bg_color="#63A5E6")
    label.grid(row=2,column=0, padx=10, pady=(0,10))

    label = ctk.CTkLabel(panel, text='Recuerda que, el léxico a emplear es: xi, !xi, (,),v,^, con i = 1..9.')
    label.grid(row=3,column=0, padx=10, pady=(0,10))

    boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana.exit())
    boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

    # Imagen aviso
    bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
    label = ctk.CTkLabel(panel, image=bg_image, text="")
    label.grid(row=0,column=0, padx=10, pady=10)

# Muestra mensaje de error sintáctico indicando dónde se ha producido.
def mostrar_mensaje_error_sintactico_concreto(ventana, formula_booleana, posicion_error):

    # Creación de paneles
    panel = ctk.CTkFrame(ventana, corner_radius = 0)
    panel.pack(fill="both", expand=True)

    panel_superior = ctk.CTkFrame(panel) 
    panel_superior.pack(pady=10, padx=10, side='top')

    panel_inferior = ctk.CTkFrame(panel) 
    panel_inferior.pack(pady=10, padx=10, side='bottom', fill="both", expand=True) 

    # Partimos la fórmula booleana en 3 partes, para REMARCAR el error encontrado
    if posicion_error - 1 == 0:
        cadena1 = formula_booleana[0]
    else:
        cadena1 = formula_booleana[0:posicion_error]

    cadena_error = formula_booleana[posicion_error]
    cadena2 = formula_booleana[posicion_error + 1 : len(formula_booleana)]
        
    label = ctk.CTkLabel(panel_superior, text = 'Error sintáctico en: ')
    label.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

    label_frame = ctk.CTkFrame(panel_superior)
    label_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=3)

    label_cadena1 = ctk.CTkLabel(label_frame, text = cadena1)
    label_cadena1.grid(row=2, column=0, padx=2, pady=10)

    label_cadena_error = ctk.CTkLabel(label_frame, text=cadena_error, bg_color='red', font=ctk.CTkFont(weight="bold"))
    label_cadena_error.grid(row=2, column=1, padx=2, pady=10)
            
    label_cadena2 = ctk.CTkLabel(label_frame, text = cadena2)
    label_cadena2.grid(row=2, column=2, padx=2, pady=10)

    label = ctk.CTkLabel(panel_inferior, text='Recuerda que, la sintaxis a emplear es: (xi v ...) ^ (xi v ...) con i = 1..9,\n donde cada cláusula tiene a lo sumo 3 literales.')
    label.grid(row=3, column=0, padx=10, pady=5)

    boton_aceptar = ctk.CTkButton(panel_inferior, text="Aceptar", command=lambda:ventana.exit())
    boton_aceptar.grid(row=4, column=0, padx=10, pady=10)

    # Imagen de aviso
    bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))

    label = ctk.CTkLabel(panel_superior, image=bg_image, text="")
    label.grid(row=0, column=0, padx=10, pady=10,columnspan=3)

# Muestra mensaje error sintáctico general (cuando el parser no sabe dónde encontró el error sintáctico).
def mostrar_error_sintactico_general(ventana):
    
    panel = ctk.CTkFrame(ventana, corner_radius=0) 
    panel.pack(fill="both")
    
    label = ctk.CTkLabel(panel, text='Error sintáctico. No se reconoce ninguna fórmula booleana.')
    label.grid(row=1,column=0, padx=10, pady=10)

    label = ctk.CTkLabel(panel, text='Recuerda que, la sintaxis y el léxico a emplear es:\n xi, !xi, (xi v ...) ^ (xi v ...) con i = 1..9, \n donde cada cláusula tiene a lo sumo 3 literales.')
    label.grid(row=2,column=0, padx=10, pady=15)

    boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana.exit())
    boton_aceptar.grid(row=3, column=0,padx=10, pady=10)

    # Imagen aviso
    bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))

    label = ctk.CTkLabel(panel, image=bg_image, text="")
    label.grid(row=0, column=0, padx=10, pady=10)

# Muestra, en caso de que haya un error sintáctico o léxico, por pantalla los errores encontrados en la fórmula
# booleana introducida por el usuario.
def mostrar_mensaje_error(tipo_error, error, formula_booleana, posicion_error):

    nueva_ventana = VentanaPopUp(ventana_padre=None)

    if tipo_error == "lexico":
        nueva_ventana.title("Error léxico")
    else:
        nueva_ventana.title("Error sintáctico")

    nueva_ventana.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        
    # Error léxico
    if tipo_error == "lexico":
        mostrar_mensaje_error_lexico(nueva_ventana,error)

    # Error sintáctico
    else:

        # Error sintáctico en posición concreta
        if error != "":
            mostrar_mensaje_error_sintactico_concreto(nueva_ventana, formula_booleana, posicion_error)

        # Error sintáctico sin saber dónde se ha producido
        else:
            mostrar_error_sintactico_general(nueva_ventana)
            
    nueva_ventana.center()

# Función que se encarga de realizar el análisis léxico y sintáctico de la fórmula que ha introducido el usuario.
def analizador_lexico_sintactico(lexer, parser, formula_booleana,ventana):
    
    # Llamamos al analizador lexico
    tokens = lexer.tokenize(formula_booleana)
    
    # Recorremos los tokens reconocidos en busca de errores léxicos      
    for tok in tokens:
        pass

    # Si encontramos error léxico, lo mostramos por pantalla y devolvemos 1       
    if lexer.error_lexico == True:
        str = ""
        error = str.join(lexer.lista_caracteres_erroneos)
        mostrar_mensaje_error("lexico", error, formula_booleana, -1)
        return 1
    
    # Si no, llamamos al analizador sintáctico
    else: 
        parser.parse(lexer.tokenize(formula_booleana))

        # Si encuentra error sintáctico en un punto dado, lo muestra por pantalla 
        if (parser.error_sintactico_en_pos != -1):
            mostrar_mensaje_error("sintactico", formula_booleana[parser.error_sintactico_en_pos], formula_booleana, parser.error_sintactico_en_pos)
            return 1
        
        # Si encuentra error sintáctico por no haber sido reconocido ningún token, muestra 
        # por pantalla un mensaje de error
        elif parser.error_sintactico_general == True:
            mostrar_mensaje_error("sintactico", "", formula_booleana, -1)
            return 1

        # Si no encontramos error alguno, devolvemos 0
        else:
            return 0


