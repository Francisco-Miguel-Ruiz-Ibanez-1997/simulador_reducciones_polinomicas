import sys
from os import system, name
import re
import execute_controller
import cookLevin
import turing2utf
import time
import explicaciones
import phi_move_generator
import latex_generator


####################################################################################################
####################################     FUNCIONES :  ##############################################
####################################################################################################

#FUNCION PARA LEER LA MT EN TXT
def read_file(file_name):
    config = {}
    transition = {}
    aux = 0

    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        print('El archivo introducido en la entrada no existe')
        exit()
    
    for i in range(1, 8):
        content = file.readline().strip('\n').split(' ')
        config[i] = content
    for i in file:
        aux = aux + 1
        transition[aux] = i.strip('\n').split(' ')
    return config, transition

# LEE LA ENTRADA
def read_tapes():
    tape = sys.argv[2]
    return tape

# poner color en el texto para imprimir por pantalla
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

# borrar la pantalla
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


####################################################################################################
####################################     MAIN :    #################################################
####################################################################################################

# main MT.jff tape o 
# main MT.txt tape
def main(): 
    # veo si la entrada es correcta
    if (len(sys.argv) != 3):
        print("Parámetros insuficientes. USO: [MT en .txt o .jff] [entrada de la MT]")
        sys.exit(1)
       
    #ver que tipo de entrada se trata:
    #si debo, pasar de MT en jflap a texto 
    c=str(sys.argv[1])
    esMT = re.compile("(.*)(\.jff)")
    validez = re.compile("(.*)(\.jff|\.txt)")
    esValido = re.fullmatch(validez, c)
    match = re.fullmatch(esMT, c)
    nombreMT = ""

    if(esValido):
        nombreMT = esValido.group(1)
    else:
        print("El archivo introducido no tiene una extension válida debe ser un .txt o un .jff")
        sys.exit(1)

    # en la variable "name" va a estar la máquina de Turing en texto
    if(match):
       name = match.group(1) + ".txt"
       converter = turing2utf.Jflap2Utfpr()
       converter.convert(sys.argv[1], name)
    else: 
        name = str(sys.argv[1])


    # ejecutarla para sacar la tabla
    config = {}
    transitions = {}
    tape = []
    config, transitions = read_file(name)
    tape = read_tapes()

    # volcar cada configuración intermedia desde la inicial hasta la final en el tablón.
    #CARACTERISTICAS DE LA MT: 
    # nombre, determinista o no, stay o no, estadoInicial, Blanco, estadosTot, estadosFinales y la entrada
    noDeterminista = execute_controller.isNonDeterministic(transitions, config)
    esStay = execute_controller.esStay(transitions)
    estadoInicial = 'q' + str(config[5][0]) 
    blanco = config[3][0]
    estadosTotales = execute_controller.estadosEnBonito(config[4])
    estadosFinales = execute_controller.estadosEnBonito(config[6])
    entrada = sys.argv[2]

    # ejecutar la maquina
    n, tabla, reglas_en_orden, codigo = execute_controller.controller(config, tape, transitions, noDeterminista)

    if(codigo == -2):
        print("No se ha podido realizar la reducción, ejecución interrumpida por looping.")
        exit()
    elif(codigo == -3):
        print("No se ha podido realizar la reducción, entrada incorrecta.")
        exit()


    inicio = time.time()
    #  aplicar algoritmo de Cook-Levin
    configuracionInicial = execute_controller.crearConfiguracionInicial(sys.argv[2], config[5][0], n, config[3][0])
    alfabetoCinta = config[2]

    phi, phi_start, phi_accept, phi_cell, phi_move, phi_start_valores, phi_accept_valores, phi_cell_valores, phi_move_valores , valorTotal_phi, valorTotal_phi_start, valorTotal_phi_accept, valorTotal_phi_cell, valorTotal_phi_move, phi_start_latex, phi_accept_latex, phi_cell_latex,  phi_move_latex,  phi_start_valores_latex, phi_accept_valores_latex, phi_cell_valores_latex, phi_move_valores_latex = cookLevin.apply(n, tabla, estadosTotales, alfabetoCinta, configuracionInicial, estadosFinales, reglas_en_orden, transitions, blanco)
    

    fin = time.time()
    print("\nTIEMPO DE EJECUCIÓN TOTAL: ")
    print(fin - inicio)
    
    

    simbolosPosibles = alfabetoCinta + ["#"] + estadosTotales
    
    tablon_alterado = phi_move_generator.tablonAlterado(tabla, n, blanco, simbolosPosibles, estadosTotales)
    
    #latex_generator.tablonAlterado(nombreMT, tablon_alterado, n, transitions, blanco, simbolosPosibles)
    latex_generator.generarLatexInfo(nombreMT, noDeterminista, esStay, estadoInicial, blanco, estadosTotales, 
    estadosFinales, entrada, transitions, reglas_en_orden, tabla, n, 
    valorTotal_phi_start, valorTotal_phi_accept, valorTotal_phi_cell, valorTotal_phi_move, valorTotal_phi,
    phi_start_latex, phi_accept_latex, phi_cell_latex,  phi_move_latex,  
    phi_start_valores_latex, phi_accept_valores_latex, phi_cell_valores_latex, phi_move_valores_latex )

    explicaciones.mainloop(phi_start, phi_accept, phi_cell, phi_move, tabla, n, estadosFinales, entrada, estadosTotales, alfabetoCinta, 
    transitions, blanco, simbolosPosibles , nombreMT, tablon_alterado, transitions)
   
main()