import execute_controller

class Nodo(object):
    def __init__(self):
        self.nivel = 0
        self.setting = None
        self.tape = None
        self.transition = None
        self.NodoPadre = None
        self.NodoHermano = None
        self.NodosHijos = [] 

    def __init__(self, setting, tape, transition):
        self.nivel = 0
        self.setting = setting
        self.tape = tape
        self.transition = transition
        self.NodoPadre = None
        self.NodoHermano = None
        self.NodosHijos = [] 
    
    def setNivel(self, nivel):
        self.nivel = nivel
    
    def setHijos(self, hijos):
        self.NodosHijos = hijos

    def addHijo(self, hijo):
        self.NodosHijos.append(hijo)
    
    def setPadre(self, padre):
        self.NodoPadre = padre

    def setHermano(self, hermano):
        self.NodoHermano = hermano    


# Rellena las cintas con los valores del archivo
def get_tapes(tapes, config):
    valide_value = config[1]
    valide_value = valide_value + config[3]
    for i in tapes:
        if i not in valide_value:
            print ("-3: Valor insertado en la cinta incorreto")
            print('Valores de entrada válidos: ')
            print(valide_value)
            return -3
    return tapes

def getList(nodoActual, filas_tabla, reglas_utilizadas_en_orden):
    while(True):
        f = execute_controller.crearFilaTabla(nodoActual.tape, nodoActual.setting)
        filas_tabla.append(f)
        if(nodoActual.transition is not None):  #el nodo padre su transicion es None
            reglas_utilizadas_en_orden.append(nodoActual.transition)
        
        if(nodoActual.NodoPadre is None):   #Estamos en el nodo Inicial y recorremos del reves, paramos.
            return 
        
        nodoActual = nodoActual.NodoPadre   #vamos recorriendo los nodos de abajo a arriba

def isTheEnd(nodo, config, filas_tabla, reglas_utilizadas_en_orden):
    s = nodo.setting
    # Se ha encontrado el estado final:
    if (s['current_state'] in config[6]):
        print ("0: Computación terminada y aceptada.")
        getList(nodo, filas_tabla, reglas_utilizadas_en_orden)
        return True
        
    # La máquina se ha quedado en un bucle:
    if (s['counter'] == 0):
        print ("1: Computación terminada de manera forzosa; Se ha quedado en bucle (no aceptación).")
        return -2
        #getList(nodo, filas_tabla, reglas_utilizadas_en_orden)
        #return True

    return False

def bucarNodosNivel(nodosTot, nivelActual, nodosNivel):
    nodosNivel=[]
    
    for n in nodosTot:
        if(n.nivel == nivelActual):
            nodosNivel.append(n)
    
    return nodosNivel
    

def createChildren(nodoActual, transitions, config, nodosTot):
    #VARIABLES A USAR:
    #lista de hijos
    nodosHijos = []
    setting = nodoActual.setting    #EL SETTING ACTUAL
    head = setting['head_tape']     #CABEZAL DE LA CINTA
    tape = nodoActual.tape          #LA CINTA EN SÍ

############################################################################################################
############################################################################################################
#Recorremos todas las transiciones y hacemos todas las disponibles:
    for i in range(1, len(transitions) + 1, 1):
        # Si estado_atual_maquina == estado_atual_cinta y letra_cinta == letra_transicion
        if ((setting['current_state'] == transitions[i][0]) and (tape[head] == transitions[i][2])):
            # Nueva disposición de la cinta
            new_tape = tape

            # -> cambia letra_cinta por nueva_letra_transicion
            if (head > 0):
                new_tape = (tape[0:head] + transitions[i][3]) + tape[head + 1:]
            else:
                new_tape = transitions[i][3] + tape[head + 1:]
            # nueva posicion de la cabeza de la cinta
            new_head_tape = head
            if (transitions[i][4] == 'R'):
                # Añade espacios en blanco al final de la cinta
                if (new_head_tape == len(new_tape) - 1):
                    new_tape = (new_tape) + config[3][0]
                
                new_head_tape = new_head_tape + 1 # mover para la derecha
            elif (transitions[i][4] == 'L'):
                # Añadir espacios en blanco al principio de la cinta
                if (new_head_tape == 0):
                    new_tape = config[3][0] + (new_tape)
                    new_head_tape += 1
                
                new_head_tape = new_head_tape - 1 # mover para la izq
            else: # no hay movimiento, sería transitions[i][4] == 'S'
                new_head_tape = new_head_tape # mantener en la misma posicion
            
            new_setting = {
                "tape": new_tape,
                "current_state": transitions[i][1],
                "head_tape": new_head_tape,
                "counter": setting['counter'] - 1
            }

            
            #CREAMOS UN NUEVO NODO HIJO!!
            nodoHijo = Nodo(new_setting, new_tape, transitions[i])  #los demas atributos se comienzan en vacio
            nodoHijo.setPadre(nodoActual) #le introduzco su nodo padre
            nodoHijo.setNivel(nodoActual.nivel + 1) #el nivel del hijo va a ser uno mas que el del padre
            nodosTot.append(nodoHijo)
            nodosHijos.append(nodoHijo)

    #Salimos del for; vemos cositas:
    numHijos = len(nodosHijos)
    if(numHijos == 0):
        #Muere esta rama de ejecución
        return False #No hay hijos, devuelvo false
    else:
        nodoActual.setHijos(nodosHijos) #Meto los hijos dentro del padre
        return True #Ha habido hijos, devuelvo true

def execute(config, tapes, transitions, filas_tabla, reglas_utilizadas_en_orden):
    #PREPARACION:
    nodosTot = []
    tape = get_tapes(tapes, config)

    if (tape == -3): # Valores inválidos de cinta
        return -3
    
    # Configuraciones de la MT
    setting = {
        "tape": tape,
        "current_state": config[5][0],
        "head_tape": 0,
        "counter": 5000 # Contador que 'verifica' looping
    }

    nodoInicial = Nodo(setting, tape, None)     #No hace falta meter el nivel porque empieza en 0
    nodosTot.append(nodoInicial)
    nodoActual = nodoInicial

    #TODO: PRIMERO: caso en que el nodo Incial acepta la palabra; Estado final= estado inicial
    hayHijos = createChildren(nodoActual, transitions, config, nodosTot)

    #Si en la primera vuelta no hay hijos y el nodo Inicial no acepta: se rechaza
    if(not hayHijos):
        print ("-1: Computación terminada y rechazada. No hay mas hijos")
        getList(nodoActual, filas_tabla, reglas_utilizadas_en_orden)
        return -1

    nivelActual = 1 #Empieza la fiesta
############################################################################################################
############################### BUSQUEDA PRIMERO EN ANCHURA ################################################
############################################################################################################
    while(True):
        contMuerte = 0
        nodosNivel = []
        nodosNivel = bucarNodosNivel(nodosTot, nivelActual, nodosNivel)

        for nodo in nodosNivel:
            nodoActual = nodo
            #1) ver si es nodo de aceptacion o que se ha quedao colgao
            end = isTheEnd(nodo, config, filas_tabla, reglas_utilizadas_en_orden)

            if(end == -2):  #computación interrumpida por looping
                return -2
            if (end):   #Cuando devuelve true
                filas_tabla.reverse()
                reglas_utilizadas_en_orden.reverse()
                return 1
            #2) creo sus hijos
            hayHijos = createChildren(nodoActual, transitions, config, nodosTot)

            if(not hayHijos):
                contMuerte = contMuerte + 1
        
 
        if(contMuerte == len(nodosNivel)):
            #Todas las posibles ramas estan muertas: rechazo
            print ("-1: Computación terminada y rechazada.")
            print ("muerte en el nivel: " + str(nivelActual))
            getList(nodoActual, filas_tabla, reglas_utilizadas_en_orden)
            return -1
        
        nivelActual = nivelActual + 1

