import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from .parser_sat3cnf import *
from .solver import dpll

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

#############################################################
# Clase que engloba toda la funcionalidad relacionada con la 
# fórmula booleana en formato 3-cnf que introduce el usuario.
#############################################################
class FormulaBooleanaSat3cnf():

    # Constructor.
    def __init__(self, ventana, panel_base, nombre_reduccion):

        self.formula = ""
        self.panel_base = panel_base
        self.formula_correcta = False
        self.ventana = ventana
        self.nombre_reduccion = nombre_reduccion 
        self.panel_datos = None
        self.num_formulas_introducidas = 0

        self.mostrar_formula_booleana()
    
    ### Getters ###

    def get_formula_booleana(self):
        return self.formula.get()

    def get_panel_formula(self):
        return self.panel_formula
    
    def get_panel_datos(self):
        return self.panel_datos
    
    def get_formula_correcta(self):
        return self.formula_correcta
    
    def get_num_formulas_introducidas(self):
        return self.num_formulas_introducidas
    
    def get_cjto_literales(self):
        return self.cjto_literales
    
    def get_num_clausulas(self):
        return self.num_clausulas
    
    def get_clausulas(self):
        return self.clausulas
    
    def get_num_literales(self):
        return self.num_literales

    # Método que muestra el panel de introducción de la fórmula booleana.
    def mostrar_formula_booleana(self):

        self.panel_formula = ctk.CTkFrame(self.panel_base, fg_color=("#98B3D0", "gray20"))
        self.panel_formula.pack(padx=10, pady=(10,10), side='top')
       
        panel_interior = ctk.CTkFrame(self.panel_formula, corner_radius = 0)
        panel_interior.pack(padx=10, pady=10, expand="no")
     
        label = ctk.CTkLabel(panel_interior, text='Ejemplo: (x1 v !x2) ^ (!x1 v x2 v x3) ', font=ctk.CTkFont(size=13, weight="bold"))
        label.grid(row=1,column=1, padx=10, pady=10, columnspan=2)

        label = ctk.CTkLabel(panel_interior, text='Introduce una \nfórmula booleana ϕ \nen forma 3-cnf:', font=ctk.CTkFont(size=13, weight="bold"))
        label.grid(row=2,column=0, padx=10, pady=10)
        
        self.formula = tk.StringVar()
        entry_formula = ctk.CTkEntry(panel_interior, textvariable=self.formula, width=300)
        entry_formula.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        boton_limpiar = ctk.CTkButton(panel_interior, text="Más info", fg_color="#6B8399", hover_color="#7A96B0",
                                            command=lambda:self.mostrar_info_formato_sat3cnf(), width=20)
        boton_limpiar.grid(row=3, column=0, padx=10, pady=10) 

        boton_introducir = ctk.CTkButton(panel_interior, text="Introducir", fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"), 
                                            command=lambda:self.tratar_formula())
        boton_introducir.grid(row=3, column=2, padx=10, pady=10)

        boton_limpiar = ctk.CTkButton(panel_interior, text="Limpiar", fg_color="#D79E12", hover_color="#F0B72D",
                                        command=lambda:self.limpiar_texto())
        boton_limpiar.grid(row=3, column=1, padx=10, pady=10)

    # Muestra al usuario cuál es la estructura de la fórmula que debe 
    # introducir. Está tendrá formato SAT3cnf.
    def mostrar_info_formato_sat3cnf(self):
        
        ventana_info = VentanaPopUp(self.ventana)
        ventana_info.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_info.title("Info")

        panel_nota_aclaratoria= ctk.CTkFrame(ventana_info, corner_radius = 0)
        panel_nota_aclaratoria.pack(fill="both")

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info.png"),size=(50, 50))
        label = ctk.CTkLabel(panel_nota_aclaratoria, image=bg_image, text="")
        label.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_nota_aclaratoria, text="Una fórmula booleana  ϕ está en forma 3-cnf si:")
        label.pack()

        tabview_forma_3cnf = ctk.CTkTabview(panel_nota_aclaratoria, height=200, width=200)
        tabview_forma_3cnf.pack(padx=10, pady=10, fill="both")
        tabview_forma_3cnf.add("1º condición")
        tabview_forma_3cnf.add("2º condición")

        texto = "Es una conjunción (^) de cláusulas, donde una cláusula es una disyunción\n (v) de a lo sumo 3 literales, "\
                "de forma que un literal y su negado no pueden aparecer\n en la misma cláusula. Así:\n\n"\
                "(x1 v !x4) ^ (!x5) ^ (!x2 v x1 v x3) es válida \n" \
                "(x5 v !x5) ^ (x3) no es válida"

        label = ctk.CTkLabel(tabview_forma_3cnf.tab("1º condición"), text = texto)
        label.pack(padx=10, pady=10)

        texto = "\n\nLos literales a emplear son: x1, ..., x9"

        label = ctk.CTkLabel(tabview_forma_3cnf.tab("2º condición"), text = texto)
        label.pack(padx=10, pady=10)

        boton = ctk.CTkButton(panel_nota_aclaratoria, text="Aceptar", command=lambda:ventana_info.exit())
        boton.pack(padx=10, pady=(0,10))

        ventana_info.center()
    
    # Elimina los datos introducidos.
    def limpiar_texto(self):

        # Quitamos/limpiamos datos introducidos
        self.formula.set('')

        self.formula_correcta = False

        if self.panel_datos != None:
                self.panel_datos.pack_forget()

    # SAT3-CNF: https://cs.famaf.unc.edu.ar/~hoffmann/md18/05.html#el-lenguaje-sat

    # Función que se encarga de determinar si la fórmula introducida es correcta o no 
    # a través del uso de un analizador sintáctico y léxico.
    def tratar_formula(self):

        cadena_formula_booleana = f'{self.formula.get()}'

        lexer = FormBoolLexer()
        parser = FormBoolParser()

        # Llamamos al analizador sintáctico. Si devuelve un error, lo mostramos por pantalla
        if analizador_lexico_sintactico(lexer, parser, cadena_formula_booleana, self.ventana) == 1:
            self.formula_correcta = False

            if self.panel_datos != None:
                self.panel_datos.pack_forget()

        # Si no hay error, procedemos a obtener información sobre la formula introducida, como literales,
        # cláusulas, etc
        else:

            cadena_formula_booleana = cadena_formula_booleana.replace(" ", "")
            cadena_formula_booleana = cadena_formula_booleana.split('^')

            # Comprobamos ahora que la fórmula introducida no tiene en sus cláusulas un literal xi y su negado !xi
            cjto_literales, literal, clausula, num_clausula = self.comprobar_clausula(cadena_formula_booleana)

            if len(cjto_literales) == 0:
                self.formula_correcta = False

                if self.panel_datos != None:
                    self.panel_datos.pack_forget()
                    
                self.error_clausula(literal, clausula, num_clausula)

            # Si no tenemos NINGÚN tipo de error, arrancamos, ahora sí, la simulación de la poli-reducción
            else:

                self.formula_correcta = True
                self.num_formulas_introducidas += 1
                self.cjto_literales = cjto_literales

                # Obtenemos las cláusulas y su num
                self.clausulas = cadena_formula_booleana
                self.num_clausulas = len(self.clausulas)

                # Calculamos el nº de literales. Tengamos en cuenta que si tenemos x1 y not x1, es un solo
                # literal, x1
                self.num_literales = len(self.cjto_literales)
            
                if self.panel_datos != None:
                    self.panel_datos.pack_forget()

                # Mostramos datos recabados
                self.panel_datos = ctk.CTkFrame(self.panel_base)
                self.panel_datos.pack(side='top', padx=20, pady=(20,10), fill="both")

                label = ctk.CTkLabel(self.panel_datos, text="Datos de la fórmula ϕ introducida",
                                        font=ctk.CTkFont(size=16, weight="bold"))
                label.pack(side="top", padx=20, pady=10)

                panel_info = ctk.CTkTabview(self.panel_datos, height=50, width=200)
                panel_info.pack(side="top", padx=20, pady=(0,10), fill="both")
                panel_info.add("Fórmula ϕ")
                panel_info.add("Num cláusulas")
                panel_info.add("Literales")
                panel_info.add("Num literales")

                label = ctk.CTkLabel(panel_info.tab("Fórmula ϕ"), text=f'{self.formula.get()}')
                label.pack(fill="both")

                label = ctk.CTkLabel(panel_info.tab("Num cláusulas"), text=str(self.num_clausulas))
                label.pack(fill="both") 

                label = ctk.CTkLabel(panel_info.tab("Literales"), text=str(sorted(self.cjto_literales)))
                label.pack(fill="both")

                label = ctk.CTkLabel(panel_info.tab("Num literales"), text=f'{self.num_literales}')
                label.pack(fill="both")

    # Función que comprueba si en las cláusulas de la fórmula que
    # introduce el usuario, hay alguna de ellas en las que aparece 
    # un literal y su negado, cosa que no puede ocurrir.    
    def comprobar_clausula(self, clausulas):

        # Declaramos como cjto para evitar repeticiones
        cjto_literales = set()

        num_clausula = 1
        # Obtenemos el cjto de literales de la formula booleana y su num
        for clausula in clausulas:
            clausula = clausula.replace("(","")
            clausula = clausula.replace(")","")
            clausula = clausula.replace(" ", "")
            literales = clausula.split('v')

            for literal in literales:
                # Comprobamos que no se introducen literales repetidos en el caso de que 
                # tengamos un literal y su negado
                if "!" in literal:
                    literal = literal.replace("!","")
                        
                    if literal in literales:
                        cjto_literales = set()
                        return cjto_literales, literal, clausula, num_clausula
                    
                cjto_literales.add(literal)

            num_clausula +=1
        
        return cjto_literales, "", "", 0

    # Función que crea una ventana de error indicando que una cláusula
    # de la fórmula contiene un literal y su negado.
    def error_clausula(self, literal, clausula, num_clausula):

        # Creamos ventana
        ventana_error = VentanaPopUp(self.ventana)
        
        ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_error.title("Error en cláusula")

        panel = ctk.CTkFrame(ventana_error, corner_radius = 0)
        panel.pack(fill="both", expand=True)

        # Imagen error
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.grid(row=0, column=0, padx=10, pady=10)

        cadena_clausula = ""
        for char in clausula:
            cadena_clausula += char
            if char.isnumeric() or char =="v":
                cadena_clausula += " "
            
        texto = "Error en la cláusula:"
        label = ctk.CTkLabel(panel,text=texto)
        label.grid(row=1, column=0, padx=10, pady=(10,0))

        panel_clausula = ctk.CTkTabview(panel, height=50)
        panel_clausula.grid(row=2, column=0, padx=10, pady=10)
        panel_clausula.add("Cláusula nº " + str(num_clausula))

        label = ctk.CTkLabel(panel_clausula.tab("Cláusula nº " + str(num_clausula)), text="( " + cadena_clausula + ")")
        label.pack(fill="both")

        texto = " con el literal " + literal + "."\
            "\n\nUna cláusula no puede contener un literal xi y su negado !xi."
        label = ctk.CTkLabel(panel, text=texto)
        label.grid(row=3,column=0, padx=10, pady=10)
        
        # Boton aceptar
        boton = ctk.CTkButton(panel,text="Aceptar", command=lambda:ventana_error.exit(), height=30)
        boton.grid(row=4, column=0, padx=10, pady=10)

        ventana_error.center()

    # Función que llama al solver dpll para comprobar la satisfacibilidad de la 
    # fórmula booleana.
    def es_satisfacible(self):
        
        # Transformaremos la formula booleana recibida en el formato que reclama el solver dpll de
        # https://github.com/safwankdb/SAT-Solver-using-DPLL

        cadena_formula = f'{self.formula.get()}'

        ruta_fichero_entrada = self.formatear_formula_booleana(cadena_formula)

        if (ruta_fichero_entrada != ""):
            satisfacible, lista_valores_literales = dpll(ruta_fichero_entrada)

            lista_valores_literales_formt = []
            # Si la fórmula es satisfacible, pasamos a nuestro formato (xi con i=1,2,3, ..., 9)
            if satisfacible:
                for literal, valor in ((lista_valores_literales)):
                    match literal:
                        case 'A':
                            lista_valores_literales_formt.append(('x1',valor))
                        case 'B':
                            lista_valores_literales_formt.append(('x2',valor))
                        case 'C':
                            lista_valores_literales_formt.append(('x3',valor))
                        case 'D':
                            lista_valores_literales_formt.append(('x4',valor))
                        case 'E':
                            lista_valores_literales_formt.append(('x5',valor))
                        case 'F':
                            lista_valores_literales_formt.append(('x6',valor))
                        case 'G':
                            lista_valores_literales_formt.append(('x7',valor))
                        case 'H':
                            lista_valores_literales_formt.append(('x8',valor))
                        case 'I':
                            lista_valores_literales_formt.append(('x9',valor))

                # El solver dpll puede no devolver valor a todos los literales. Por tanto,
                # a aquellos literales que no tengan valor asignado, le asignaremos True (también 
                # podríamos haberles asignado False, pues su asignación de valor es indiferente para 
                # la satisfacibilidad de la fórmula en base a la solución encontrada por el solver)
                if len(lista_valores_literales_formt) != self.num_literales:
                    for literal in self.cjto_literales:
                        if ((literal, True) not in lista_valores_literales_formt) and ((literal, False) not in lista_valores_literales_formt):
                            lista_valores_literales_formt.append((literal, True))

                return satisfacible, lista_valores_literales_formt
            
            else:
                return satisfacible, lista_valores_literales_formt

        else:
            pass
    
    # Formateamos la fórmula booleana introducida al formato que recibe como entrada el solver dpll.
    def formatear_formula_booleana(self, cadena_formula):

        pos = 0

        # Fichero donde guardaremos la formula formateada
        ruta_fichero = ""

        # Cadena que contiene la fórmula de entrada para el solver DPLL
        input_solver = ""

        # Recorremos la fórmula booleana
        while pos < len(cadena_formula):

            char = cadena_formula[pos]
                        
            # x1 será A, x2 será B y x3 será C, y así hasta x9 y I. En caso de encontrar un literal negado,
            # pondremos !{A,B,C,....,I}.
            match char:

                # Caso negación de literal. Insertamos "!"
                case "!":

                    input_solver += char
                    pos += 1

                # Caso variable/literal "a secas"
                case "x":
                    # Según el literal, insertaremos A, B o C en la entrada del solver
                    literal = cadena_formula[pos+1]
                    match literal:
                        case "1":
                            input_solver += "A "
                        case "2":
                            input_solver += "B "
                        case "3":
                            input_solver += "C "
                        case "4":
                            input_solver += "D "
                        case "5":
                            input_solver += "E "
                        case "6":
                            input_solver += "F "
                        case "7":
                            input_solver += "G "
                        case "8":
                            input_solver += "H "
                        case "9":
                            input_solver += "I " 
                        case _:
                            pass

                    pos += 2
                
                case ")":
                    input_solver += "\n"
                    pos += 1
                    
                case _:
                    pos += 1

        try:
            # Escribimos la formula booleana formateada en un fichero .txt
            f = open("modulos_externos/formula_booleana_sat3cnf/formula_formateada.txt", "w")
            f.write(input_solver)
            ruta_fichero = "modulos_externos/formula_booleana_sat3cnf/formula_formateada.txt"

        except FileNotFoundError:
            ruta_fichero = ""
            messagebox.showerror('Error', 'Error: No se pudo crear el fichero .txt en el que se almacena la fórmula booleana formateada.')
        
        return ruta_fichero