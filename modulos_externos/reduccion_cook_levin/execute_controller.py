#def isNonDeterministic(config, tape, transitions):
from distutils.command.config import config
import execute_MT
import execute_MTND

####################################################################################################
#################################    FUNCIONES TABLON :    #########################################
####################################################################################################

"""La tabla tendrá tamño:
    nº filas = nº de transiciones realizadas +1 (o lo longitud de filas tabla)
    nº columnas = tamaño de la fila con mayor longitud + 2 (para añadir los '#')"""
def calcularTamanyoTabla(filas_tabla):
    tamFinal = len(filas_tabla)
    for fila in filas_tabla:
        #Split me separa los elementos de un string en diferentes elementos en una lista, delimitados por espacio
        tamNuevo = len(fila.split())
        if  tamNuevo > tamFinal : 
            tamFinal = tamNuevo
    
    return tamFinal +2  # el +2 contempla los "#"

# TODO: 
# ver si tiene el simbolo "#" y cambiarlo en consecuencia
def crearTabla(filas_tabla, blanco):
    n = calcularTamanyoTabla(filas_tabla) 
    #tabla = [[0] * n for i in range(len(filas_tabla))] #inicializo la tabla
    tabla = [[blanco] * n for i in range(n)] #inicializo la tabla todo a simbolos blancos
    fila=0
    for cinta in filas_tabla:
        #Estoy dentro una configuracion dentro de la tabla
        meter = cinta.split()
        contMeter=0
        filaUltima=[]
        
        for i in range(0, n ,1):
            if (i==0 or i==n-1):
                tabla[fila][i] = '#'
            else:
                if(contMeter < len(meter)):
                    tabla[fila][i] = meter[contMeter]
                    contMeter += 1
                else:
                    tabla[fila][i] = blanco
            filaUltima = tabla[fila]
        fila+=1
        if fila >= n:
            break
    #meto desde donde me he quedao la última fila si la fila no es mayor que n
    if fila < n:
        for fila in range(fila, n, 1):
            tabla[fila] = filaUltima
    return tabla, n


def crearConfiguracionInicial(entrada, estadoInicial, n, blanco):
    filaTabla=[]
    estado = 'q'+estadoInicial 
    tam = len(entrada)+2 #le sumo dos porque la j la posicion 0 y 1 son espacios ocupados
    
    for j in range(0,n,1):
        if(j <tam):
            if(j == 1):
                filaTabla.append(estado)
            elif(j == 0):
                filaTabla.append('#')
            else:
                filaTabla.append(entrada[j-2])
        elif (j == n-1):
            filaTabla.append('#')
        else:
            filaTabla.append(blanco)
    
    return filaTabla

#Crear una fila de la tabla para el algoritmo desde la cinta actual y el setting
def crearFilaTabla(tape, setting):
    filaTabla=""
    cont = 0
    #print(tape)
    for j in tape:
        if(setting.get("head_tape") == cont):
            filaTabla += 'q' +setting.get("current_state")+' '
        filaTabla +=  j+ ' '
        cont = cont + 1
    return filaTabla

def isNonDeterministic(transitions, config):
    #Las transiciones son un diccionario cuya key es el orden de la transicion empezando en uno
    # lo cual me es cómodo porque puedo iterar, pero quiero ver si se repite algo...
    """ En el diccionario (transitions) vamos a tener en value: 
    ['estado_actual', 'estado_nuevo', 'simbolo_Actual', 'Nuevo_Simbolo', 'direccion'] 
    Querremos ver de la key i el valor [0] (estado actual) y el [2] (simbolo actual);
    Si dentro de las transiciones se repite alguno, es una MTND"""
    estado_actual= -1
    simbolo_actual = -1
    blanco = config[3][0]
    
    for i in range(1, len(transitions) + 1, 1):
        estado_actual = transitions[i][0] 
        simbolo_actual = transitions[i][2] 
        
        for j in range(i+1, len(transitions) + 1, 1): #lo comparo con los demas
            if(transitions[j][0] == estado_actual):
                if(transitions[j][2] == simbolo_actual):   
                    return True
    return False

def esStay(transitions):
    # valores de cada transicion: ['estado_actual', 'estado_nuevo', 'simbolo_Actual', 'Nuevo_Simbolo', 'direccion']
    for i in range(1, len(transitions) + 1, 1):
        direccion = transitions[i][4]
        if(direccion == 'S'): 
            return True
    return False


def estadosEnBonito(estados):
    estadosBonitos = []
    for estado in estados:
        estadosBonitos.append('q'+ str(estado))
    return estadosBonitos 

def transicionABointo(transicion):
    t = []
    estado_actual = 'Estado actual = q' + str(transicion[0])
    estado_nuevo = 'Nuevo estado = q' + str(transicion[1])
    simbolo_actual = 'Simbolo actual = ' + str(transicion[2])
    nuevo_simbolo = 'Nuevo simbolo = ' + str(transicion[3])
    direccion =  'Direccion = ' + str(transicion[4])
    t.append(estado_actual)
    t.append(simbolo_actual)
    t.append(estado_nuevo)
    t.append(nuevo_simbolo)
    t.append(direccion)
    return t

def transicionesEnBonito(transiciones):
    transicionesBonitas=[]
    for i in range(1, len(transiciones) , 1):
        t = transicionABointo(transiciones[i])
        transicionesBonitas.append(t)

    return transicionesBonitas

    

####################################################################################################
####################################     CONTROLLER :    ###########################################
####################################################################################################

""" Esta funcion sirve como controlador para ejecutar la MT segun sea no determinista o sí. 
Una vez se ejecute se llamara a la creación de la tabla. """
def controller(config, tape, transitions, noDeterminista):

    filas_tabla = [] #lista donde vamos a guardar las filas de la tabla
    reglas_utilizadas_en_orden = [] #Lista donde se van a guardar las reglas de transicion aplicadas en orden de fila
    codigo = 0
    
    if(noDeterminista):
        #print("se procede a ejecutar la MTND (no determinista)")
        codigo = execute_MTND.execute(config, tape, transitions, filas_tabla, reglas_utilizadas_en_orden)
    else:
        #print("se procede a ejecutar la MTD (determinista)")
        codigo = execute_MT.machine(config, tape, transitions, filas_tabla, reglas_utilizadas_en_orden) 

    if(codigo < 0):
        return None, None, None, codigo
    else:
        blanco = config[3][0]   # simbolo blanco que se va a utilizar
        tabla , n = crearTabla(filas_tabla, blanco)
        
    
        return n, tabla, reglas_utilizadas_en_orden, codigo
    
    