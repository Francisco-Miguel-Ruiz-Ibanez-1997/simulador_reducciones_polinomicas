import re
import random
from string import ascii_letters
from tkinter import E

####################################################################################################
####################################     PHI_MOVE     ##############################################
####################################################################################################

def generarLaMisma(fila, filaSiguiente, i):
    igual_latex='\\ (\\ '
    igual=" ( "
    igual_valores_latex = '\\ (\\ '
    igual_valores=" ( "
    tam = len(fila)
    esLaMisma = True
    
    esEstado = re.compile("q[0-9]*")
    eshastag= re.compile("#")

    for index in range(0, tam ,1):
        valor = fila[index]
        match = re.fullmatch(esEstado, valor)
        match_hastag = re.fullmatch(eshastag, valor)
        if(index < tam-1):
            if(match):
                num_estado = valor[1]
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_q_"+num_estado+"$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_q_"+num_estado+"$\\ $\\wedge$\\ "
            elif(match_hastag):
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_\\#$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_\\#$\\ $\\wedge$\\ "
            else:
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_"+valor+"$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_"+valor+"$\\ $\\wedge$\\ "

            #fila anterior
            igual += "X_"+str(i)+"_"+str(index+1)+"_"+valor + " AND "
            #la fila siguiente
            igual += "X_"+str(i+1)+"_"+str(index+1)+"_"+valor + " AND "
            if(fila[index] == filaSiguiente[index]):
                igual_valores_latex+= "True $\\wedge$\\ True $\\wedge$\\ "
                igual_valores += "True AND True AND "
            else:
                igual_valores_latex+= "True $\\wedge$\\ False $\\wedge$\\ "
                igual_valores += "True AND False AND "
                esLaMisma = False
        else:
            if(match):
                num_estado = valor[1]
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_q_"+num_estado+"$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_q_"+num_estado+"$\\ )\\ "
            elif(match_hastag):
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_\\#$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_\\#$\\ )\\ "
            else:
                igual_latex += "$X_"+str(i)+",_"+str(index+1)+"\\_"+valor+"$\\ $\\wedge$\\ "
                igual_latex += "$X_"+str(i+1)+",_"+str(index+1)+"\\_"+valor+"$\\ )\\ "

            #fila anterior
            igual += "X_"+str(i)+"_"+str(index+1)+"_"+valor + " AND "
            #la fila siguiente
            igual += "X_"+str(i+1)+"_"+str(index+1)+"_"+valor + " ) "
            
            if(fila[index] == filaSiguiente[index]):
                igual_valores_latex+= "True $\\wedge$\\ True )\\ "
                igual_valores += "True AND True )"
            else:
                igual_valores_latex+= "True $\\wedge$\\ False )\\ "
                igual_valores += "True AND False )"
                esLaMisma = False

    return igual, igual_valores, esLaMisma, igual_latex, igual_valores_latex

#crea la fila tras aplicarle la transicion
# #todo: falla aqui  
def crearFila(fila, estado_nuevo, nuevo_simbolo, direccion, blanco):
    tamano = len(fila)
    filaNueva= ['0'] * tamano
    esEstado = re.compile("q[0-9]*")

    for i in range(0,tamano,1):
        match = re.fullmatch(esEstado, fila[i])
        if(match):
            if(direccion ==  'R'):  #muevo el cabezal a la derecha
                filaNueva[i] = nuevo_simbolo 
                filaNueva[i+1] = estado_nuevo 
                i = i + 2
                for i in range(i,len(fila),1): 
                    filaNueva[i] = fila[i] 
                return filaNueva
            elif(direccion ==  'L'):
                if(i-1 == 0):
                    filaNueva[i] = estado_nuevo
                    filaNueva[i+1] = blanco
                    filaNueva[i+2] = nuevo_simbolo
                    filaNueva[i+3] = fila[i+2]
                    i = i+4
                    for i in range(i,len(fila),1): 
                        filaNueva[i] = fila[i] 
                else:
                    muevo = filaNueva[i-1]
                    filaNueva[i-1] = estado_nuevo  
                    filaNueva[i] = muevo 
                    filaNueva[i+1] = nuevo_simbolo 
                    i = i + 2
                    for i in range(i,len(fila),1): 
                        filaNueva[i] = fila[i] 
                return filaNueva
            else: # stay, me quedo igual
                filaNueva[i] = estado_nuevo 
                filaNueva[i+1] = nuevo_simbolo 
                i = i + 2
                for i in range(i,len(fila),1): 
                    filaNueva[i] = fila[i] 
                return filaNueva
        else:
            filaNueva[i] = fila[i] 

    return filaNueva


def queHay(fila):
    estadoFila=""
    headFila=""
    esEstado = re.compile("q[0-9]*")
    for i in range(0,len(fila),1):
        match = re.fullmatch(esEstado, fila[i])
        if(match):
            estadoFila = fila[i]
            headFila = fila[i+1]
            return estadoFila, headFila
    
    return estadoFila, headFila

#valores de transitions:
#    ['estado_actual', 'estado_nuevo', 'simbolo_Actual', 'Nuevo_Simbolo', 'direccion']
def generarFilas(fila, transitions, blanco):
    filas = []
    transiciones_usadas = []
    estadoFila, headFila = queHay(fila)
    tam = len(transitions)
    for i in range(1, tam + 1, 1):
        t=transitions[i]
        estado_actual = "q" +  str(t[0]) 
        simbolo_actual = str(t[2])
        if (estado_actual == estadoFila) and (headFila == simbolo_actual):
            estado_nuevo = "q" + str(t[1])
            nuevo_simbolo = str(t[3])
            direccion = str(t[4])
            f = crearFila(fila, estado_nuevo, nuevo_simbolo, direccion, blanco)
            filas.append(f)
            transiciones_usadas.append(t)

    return filas, transiciones_usadas


def generarPosibles(fila, filaSiguiente, transitions, i, j, blanco):
    valoresFila_latex = ''
    valoresFila_valores_latex = ''
    valoresFila=""
    valoresFila_valores = ""

    posibles_latex=''
    posibles_valores_latex = ''
    posibles = ""
    posibles_valores = ""
    siHayPosible = False

    esEstado = re.compile("q[0-9]*")
    eshastag= re.compile("#")

    #Los valores de la fila padre (siempre iguales)
    #termina en AND porque se va a unir con los valores posibles que puede tener la otra fila
    for c in range(0,len(fila),1):
        valor = fila[c]
        match = re.fullmatch(esEstado, valor)
        match_hastag = re.fullmatch(eshastag, valor)
        
        if(match):
            num_estado = valor[1]
            valoresFila_latex += "$X_"+str(i)+",_"+str(c+1)+"\\_q_"+num_estado+"$\\ $\\wedge$\\ "
        elif(match_hastag):
            valoresFila_latex += "$X_"+str(i)+",_"+str(c+1)+"\\_\\#$\\ $\\wedge$\\ "
        else:
            valoresFila_latex += "$X_"+str(i)+",_"+str(c+1)+"\\_"+valor+"$\\ $\\wedge$\\ "
            
        valoresFila += "X_"+str(i)+"_"+str(c+1)+"_"+valor+ " AND " 
        valoresFila_valores_latex+= "True\\ $\\wedge$\\ "
        valoresFila_valores += "True AND "   #siempre tienen valor verdad

    filasPosibles, _ = generarFilas(fila, transitions, blanco)
    tam = len(filasPosibles)

    if(tam != 0):
        for x in range(0,tam,1):
            hay = True
            f = filasPosibles[x]
            posible_actual_latex = ''
            posible_actual=""
            posible_actual_valores_latex = ''
            posible_actual_valores=""
            #comparo la fila siguiente con la posible segun la formula
            tamano = len(f)

            for c in range(0, tamano,1):
                valor = f[c]
                valorSiguiente = filaSiguiente[c]

                match = re.fullmatch(esEstado, valor)
                match_hastag = re.fullmatch(eshastag, valor)
        
                if(c < tamano -1):

                    if(match):
                        num_estado = valor[1]
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_q_"+num_estado+"$\\ $\\wedge$\\ "
                    elif(match_hastag):
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_\\#$\\ $\\wedge$\\ "
                    else:
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_"+valor+"$\\ $\\wedge$\\ "

                    posible_actual += "X_"+str(j)+"_"+str(c+1)+"_"+valor+ " AND " 

                    if(valor == valorSiguiente):
                        posible_actual_valores_latex += "True\\ $\\wedge$\\ "
                        posible_actual_valores += "True AND "
                    else:
                        posible_actual_valores_latex += "False\\ $\\wedge$\\ "
                        posible_actual_valores += "False AND "
                        hay = False
                else:
                    if(match):
                        num_estado = valor[1]
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_q_"+num_estado+"$\\ "
                    elif(match_hastag):
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_\\#$\\ "
                    else:
                        posible_actual_latex += "$X_"+str(j)+",_"+str(c+1)+"\\_"+valor+"$\\ "

                    posible_actual += "X_"+str(j)+"_"+str(c+1)+"_"+valor + " "
                    if(valor == valorSiguiente):
                        posible_actual_valores_latex += "True\\ "
                        posible_actual_valores += "True "
                    else:
                        posible_actual_valores_latex += "False\\ "
                        posible_actual_valores += "False  "
                        hay = False
        
            if(x < tam-1 ):
                posibles_latex += "\\ ( " + valoresFila_latex + posible_actual_latex + " )\\ $\\vee$\\ "
                posibles += " ( " + valoresFila + posible_actual + " ) OR "
                posibles_valores_latex+= "\\ ( " + valoresFila_valores_latex + posible_actual_valores_latex + " )\\ $\\vee$\\ "
                posibles_valores += " ( " + valoresFila_valores + posible_actual_valores + " ) OR "
            else:
                posibles_latex += "\\ ( " + valoresFila_latex + posible_actual_latex + " )\\ )\\ "
                posibles +=  " ( " + valoresFila + posible_actual + " ) )"
                posibles_valores_latex+= "\\ ( " + valoresFila_valores_latex + posible_actual_valores_latex + " )\\ )\\ "
                posibles_valores +=  " ( " + valoresFila_valores + posible_actual_valores + " ) )" 
            
            if(hay):
                siHayPosible = True

    else:
        posibles_latex = ''
        posibles = ""
        posibles_valores_latex=''
        posibles_valores = ""
    
    return posibles, posibles_valores, siHayPosible, posibles_latex, posibles_valores_latex

""" def valoresFila(fila, i):
    tam = len(fila)
    igual = ""
    igual_valores = ""
    for index in range(0, tam ,1):
        valor = fila[index]
        igual += "X_"+str(i)+"_"+str(index+1)+"_"+valor + " AND "
        igual_valores += "True AND  "


    return igual, igual_valores """


####################################################################################################
########################################     MAIN :       ##########################################
####################################################################################################

def generarPhiMove(tabla, n, transitions, blanco):
    #IDEA: ir fila por fila viendo que es legal.
    #Una fila es legal cuando: tiene un unico estado y cuando es igual que la anterior o se ha llegado a ella a través de una regla de transicion
    #Se hace así porque la MT admite el estado "STAY" y complica las cosas. De esta manera es muy facil.
    #Se ha adaptado la fórmula pero es igual, en vez de ventanas de tamaño 2x3 son de tamaño filax2
    phi_move_latex='(\\ '
    phi_move=" ( "
    phi_move_valores_latex ='(\\ '
    phi_move_valores=" ( "
    valorTotal = True
    for i in range(0,n-1,1):
        #comparamos la fila "i" con su siguiente
        igual, igual_valores, esLaMisma, igual_latex, igual_valores_latex = generarLaMisma(tabla[i], tabla[i+1], i+1)  #en caso de que no se haga transicion


        posibles, posibles_valores, hayPosible, posibles_latex, posibles_valores_latex = generarPosibles(tabla[i], tabla[i+1], transitions, i+1, i+2, blanco)


        if((not esLaMisma) and (not hayPosible)):
            valorTotal = False
        # el primer caso siempre va a ser el de si las dos filas son iguales
        phi_move_latex += '(\\ '+ igual_latex
        phi_move += " ( " + igual
        phi_move_valores_latex+= '(\\ '+ igual_valores_latex
        phi_move_valores += " ( " +  igual_valores  
        
        #¿hay transiciones posibles?
        if(posibles == ""): # si no, solo pongo el caso de que sean iguales, lo unico que la hace legal
            if(i < n-2): # porque recorremos las filas dos a dos
                phi_move_latex += '\\ )\\ $\\wedge$\\ '
                phi_move += " ) AND "
                phi_move_valores_latex += '\\ )\\ $\\wedge$\\ '
                phi_move_valores +=  " ) AND "
            else:
                phi_move_latex += '\\ )\\ '
                phi_move +=  " ) "
                phi_move_valores_latex += '\\ )\\ '
                phi_move_valores +=  " ) "
        else: # si hay transiciones posibles; pongo la fila actual + la posible
            if(i < n-2):
                phi_move_latex += '\\ $\\vee$\\ ' + posibles_latex+ '\\ $\\wedge$\\ '
                phi_move += " OR " + posibles + " AND "
                phi_move_valores_latex += '\\ $\\vee$\\ ' + posibles_valores_latex+ '\\ $\\wedge$\\ '
                phi_move_valores += " OR " + posibles_valores + " AND "
            else:
                phi_move_latex += '\\ $\\vee$\\ ' + posibles_latex+ '\\ '
                phi_move += " OR " + posibles + " "
                phi_move_valores_latex += '\\ $\\vee$\\ ' + posibles_valores_latex+ '\\ '
                phi_move_valores += " OR " + posibles_valores + " "

    phi_move_latex += '\\ )\\ '
    phi_move += " ) "
    phi_move_valores_latex  += '\\ )\\ '
    phi_move_valores += " ) "

    return phi_move, phi_move_valores, valorTotal, phi_move_latex, phi_move_valores_latex


###################################################
############# para la explicación: ################
###################################################

def generarPhi_move_UnaSolo(tabla, n, transitions, i, blanco):
    phi_move_min=" ( "
    phi_move_valores_min=" ( "
    
    #comparamos la fila "i" con su siguiente
    igual, igual_valores, _, _, _ = generarLaMisma(tabla[i-1], tabla[i], i)  #en caso de que no se haga transicion
    posibles, posibles_valores, _, _, _ = generarPosibles(tabla[i-1], tabla[i], transitions, i, i+1, blanco)
    # el primer caso siempre va a ser el de si las dos filas son iguales
    phi_move_min += " ( " + igual
    phi_move_valores_min += " ( " +  igual_valores  
    
    #¿hay transiciones posibles?
    if(posibles == ""): # si no, solo pongo el caso de que sean iguales, lo unico que la hace legal
            phi_move_min +=  " ) "
            phi_move_valores_min +=  " ) "
    else: # si hay transiciones posibles; pongo la fila actual + la posible
            phi_move_min += " OR " + posibles + " "
            phi_move_valores_min += " OR " + posibles_valores + " "

    phi_move_min += " ) "
    phi_move_valores_min += " ) "

    return phi_move_min, phi_move_valores_min, igual, posibles 


####################################################################################################
####################################     FUNCIONES VENTANAS :    ###################################
####################################################################################################


def cogerVentana(tabla, i,j):
    i = i-1
    j = j-1
    #las ventanas son 
    # a1 a2 a3
    # a4 a5 a6
    # j debe ser mayor que 1 y menor que n
    # i debe ser menor que n
    a2 = tabla[i][j]
    a1 = tabla[i][j-1]
    a3 = tabla[i][j+1]
    a5 = tabla[i+1][j]
    a4 = tabla[i+1][j-1]
    a6 = tabla[i+1][j+1]
    ventana = [[a1,a2,a3],[a4,a5,a6]]
    fila = tabla[i]

    return fila, ventana


def ventanaEsIgual(ventana):
    es = True
    mensaje = "La ventana es legal porque la primera fila es igual a la segunda."
    fila_1= ventana[0]
    fila_2= ventana[1]
    
    for i in range(0,len(fila_1),1):
        if(fila_1[i] != fila_2[i]):
            es = False
            mensaje = ''
    return es, mensaje

def simboloProhibido(ventana, simbolosPosibles):
    mensaje = ''
    tiene = False
    
    for fila in ventana:
        for celda in fila:
            if(celda not in simbolosPosibles):
                tiene = True
                mensaje = 'Esta ventana es ilegal porque contiene un símbolo ( '+celda+' ) que no pertenece al conjunto C, el de los símbolos permitidos.\n'
                break
        if(tiene):
            break

    return mensaje, tiene


def incumpleHastag(ventana):
    mensaje = ''
    loIncumple = False
    fila_1= ventana[0]
    fila_2= ventana[1]
    
    #el hastag va a siempre estar en los bordes de la ventana
    if(fila_1[0] == '#'):
        if(fila_2[0] != '#'):
            mensaje = "En la primera fila, primera columna, hay un hastag y en la segunda fila no está debajo de él."
            loIncumple = True
    elif(fila_1[2] == '#'):
        if(fila_2[2] != '#'):
            mensaje = "En la primera fila, tercera columna,  hay un hastag y en la segunda fila no está debajo de él."
            loIncumple = True
    elif(fila_2[0] == '#'):
        if(fila_1[0] != '#'):
            mensaje = "En la segunda fila, primera columna, hay un hastag y en la primera fila no está por encima de él."
            loIncumple = True
    elif(fila_2[2] == '#'):
        if(fila_1[2] != '#'):
            mensaje = "En la segunda fila, tercera columna, hay un hastag y en la primera fila no está por encima de él."
            loIncumple = True

    #si tiene el hastag en medio ya te digo yo a ti que es ilegal
    if(fila_1[1] == '#') and (fila_2[1] == '#'):
        mensaje = 'No tiene sentido que haya un hastag en las columnas centrales de la primera y senguda fila'
        loIncumple = True
    elif(fila_1[1] == '#'):
        mensaje = 'No tiene sentido que haya un hastag en la columna central de la primera fila'
        loIncumple = True
    elif(fila_2[1] == '#'):
        mensaje = 'No tiene sentido que haya un hastag en la columna central de la segunda fila'
        loIncumple = True
        

    return mensaje, loIncumple


def ventanaTieneMasDeUno(ventana):
    cont_1 = 0
    cont_2 = 0
    seCumple = False
    mensaje = ''
    esEstado = re.compile("q[0-9]*")
    fila_1= ventana[0]
    fila_2= ventana[1]
    for i in range(0,3,1):
        match = re.fullmatch(esEstado, fila_1[i])
        if(match):
            cont_1 += 1
        match = re.fullmatch(esEstado, fila_2[i])
        if(match):
            cont_2 += 1

    if(cont_1 > 1):
        if(cont_2 > 1):
            seCumple = True
            mensaje = "La ventana es ilegal porque hay más de un estado en ambas filas."
            return seCumple, mensaje
        else:
            seCumple = True
            mensaje = "La ventana es ilegal porque hay más de un estado en la primera fila."
            return seCumple, mensaje
    elif(cont_2 > 1):
        seCumple = True
        mensaje = "La ventana es ilegal porque hay más de un estado en la segunda fila."
        return seCumple, mensaje
    
    seCumple = False
    return seCumple,  mensaje


def ventanaNoSentido(ventana):
    # tiene estado en el medio de la primera fila y en la segunda no (no esta ni a su derecha ni a su izq ni en la misma posicion)
    mensaje = ''
    tieneSentido = False
    fila_1= ventana[0]
    fila_2= ventana[1]
    
    esEstado = re.compile("q[0-9]*")
    match_1 = re.fullmatch(esEstado, fila_1[1])
    match_2 = re.fullmatch(esEstado, fila_2[1])
    if(match_1):
        for a in fila_2:    
            match = re.fullmatch(esEstado, a)
            if(match):
                tieneSentido = True
        if(not tieneSentido):
            mensaje = "La ventana es ilegal porque hay un estado en la celda principal de la primera fila y no hay estado en la segunda."
    elif(match_2): 
        for a in fila_1:    
            match = re.fullmatch(esEstado, a)
            if(match):
                tieneSentido = True
        if(not tieneSentido):
            mensaje = "La ventana es ilegal porque hay un estado en la celda principal de la segunda fila y no hay estado en la primera."
    else:
        tieneSentido = True
    
    return tieneSentido, mensaje


def ventanaTransicion(ventana, transiciones, fila, j, blanco): 
    filasPosibles, transiciones_utilizadas = generarFilas(fila, transiciones, blanco)
    fila_2 = ventana[1]
    mensaje = ''
    legal = True
    numPosibles=0
    for fila in filasPosibles:
        es = True
        cont=0
        
        for i in range(j,j+3,1):
            if(fila_2[cont] != fila[i-1]):
                es = False
            cont += 1
            
        if(es):
            t = transiciones_utilizadas[numPosibles]
            estado_actual = "q" +  str(t[0]) 
            simbolo_actual = str(t[2])
            estado_nuevo = "q" + str(t[1])
            nuevo_simbolo = str(t[3])
            d = str(t[4])
            if(d == 'L'):
                direccion = 'a la izquierda.'
            elif(d == 'R'):
                direccion = 'a la derecha.'
            else:
                direccion = 'de tipo Stay (no se ha movido el cabezal).'

            legal = True
            mensaje = "La ventana es legal porque se ha llegado a la segunda desde una regla de transición.\n Concretamente, con estado " + estado_actual +" y símbolo en el cabezal "+ simbolo_actual + " se ha pasado al estado "+ estado_nuevo + " se ha cambiado el símbolo del cabezal por el símbolo " + nuevo_simbolo + " y se ha hecho un movimiento " + direccion
            break

        else:
            mensaje = "La ventana es ilegal porque, aunque aparentemente pueda parecer legal, no se ha podido llegar a ella desde ninguna transición."
            legal = False

        numPosibles += 1
    
    return mensaje, legal


def esLegal(tabla, transiciones, i, j, blanco, simbolosPosibles):
    """ for i in range(0,n-1,1):
        for j in range(1,n-1,1):
            mensaje, legal = esLegal(tablon_alterado, transiciones, i+1, j+1, blanco, simbolosPosibles) """

    fila, ventana = cogerVentana(tabla, i, j)
    legal = True
    mensaje = ''

    #si es igual
    es, mensaje = ventanaEsIgual(ventana)
    if (es):
        return mensaje, legal

    #ver si tiene un simbolo que no pertenece al tablon.
    mensaje, tiene = simboloProhibido(ventana, simbolosPosibles)
    if(tiene):
        legal = False
        return mensaje, legal

    #hay varios dos tipos
    mensaje, loIncumple = incumpleHastag(ventana)
    if(loIncumple):
        legal = False
        return mensaje, legal

    #  tiene mas de un estado en la primera fila
    #  si es en la segunda
    #  si es en las dos
    seCumple,  mensaje = ventanaTieneMasDeUno(ventana)
    if(seCumple):
        legal = False
        return mensaje, legal
        
    #tiene estado en el medio de la primera fila y en la segunda no (no esta ni a su derecha ni a su izq ni en la misma posicion)
    tieneSentido, mensaje = ventanaNoSentido(ventana)
    if(not tieneSentido):
        legal = False
        return mensaje, legal
    #si por transicion es congruente
    #es incongruente por transicion
    mensaje, legal = ventanaTransicion(ventana, transiciones, fila, j-1, blanco)

    return mensaje, legal
    


####################################################################################################
###############################     FUNCIONES TABLON ILEGAL :    ###################################
####################################################################################################

def tablonAlterado(tabla, n, blanco, simbolosPosibles, estadosPosibles):
    tabla_alterada = [[blanco] * n for i in range(n)] #inicializo la tabla todo a simbolos blancos
    
    for i in range(0,n,1):  #hago una copia exacta fila a fila
        tabla_alterada[i] = tabla[i].copy()

    for i in range(0,3,1):

        seed = random.randint(0,4)

        if(seed == 0):  #me cargo phi_start
            #cambiar primera fila por otra
            primera_fila = tabla[0]
            index = random.randint(1,n-1)
            fila_aleatoria = tabla[index]
            tabla_alterada[0] = fila_aleatoria
            tabla_alterada[index] = primera_fila

        elif(seed == 1):   #me cargo phi_cell
            #poner un simbolo que no es del alfabeto
            i = random.randint(0,n-1)   #fila celda
            j = random.randint(0,n-1)   #columna celda

            tabla_alterada = cambiarSimboloNoAlfabeto(tabla_alterada, i, j, simbolosPosibles)
            
        elif(seed == 2):
            #coger una celda y ponerle un simbolo diferente del alfabeto
            i = random.randint(0,n-1)   #fila celda
            j = random.randint(0,n-1)   #columna celda
            
            tabla_alterada = cambiarSimbolo(tabla_alterada, i, j, simbolosPosibles)

        elif(seed == 3):
            # quitar un estado que cumpla lo de vantana no tiene sentido
            tabla_alterada = quitarSentido(tabla_alterada, n, simbolosPosibles)

        else:
            #poner dos estados juntos
            tabla_alterada = ponerDosEstados(tabla_alterada, n, estadosPosibles)

    return tabla_alterada

def ponerDosEstados(tabla_alterada, n, estadosPosibles):
    esEstado = re.compile("q[0-9]*")
    salir = False

    for i in range(0, n, 1):
        for celda in range(0, n, 1):
            match = re.fullmatch(esEstado, tabla_alterada[i][celda])
            if(match) and (tabla_alterada[i][celda+1] not in estadosPosibles):
                for e in estadosPosibles:
                    if(e != tabla_alterada[i][celda]):
                        tabla_alterada[i][celda+1] = e
                        salir = True
                        break
            if(salir): 
                break
        if(salir):
            break
    return tabla_alterada

def quitarSentido(tabla_alterada, n, simbolosPosibles):
    # tiene estado en el medio de la primera fila y en la segunda no (no esta ni a su derecha ni a su izq ni en la misma posicion)
    esEstado = re.compile("q[0-9]*")
    salir = False
    for i in range(0, n-1, 1):
        fila_1 = tabla_alterada[i]
        fila_2 = tabla_alterada[i+1]

        for celda in range(0, n, 1):
            match = re.fullmatch(esEstado, fila_1[celda])
            if(match):
                match_2 = re.fullmatch(esEstado, fila_2[celda])
                if(match_2):
                    cambiarSimbolo(tabla_alterada, i+1, celda, simbolosPosibles)
                    salir = True
                    break
                match_2 = re.fullmatch(esEstado, fila_2[celda+1])
                if(match_2):
                    cambiarSimbolo(tabla_alterada, i+1, celda, simbolosPosibles)
                    salir = True
                    break
                match_2 = re.fullmatch(esEstado, fila_2[celda-1])
                if(match_2):
                    cambiarSimbolo(tabla_alterada, i+1, celda, simbolosPosibles)
                    salir = True
                    break
        
        if(salir):
            break
    
    return tabla_alterada

def cambiarSimboloNoAlfabeto(tabla_alterada, i, j, simbolosPosibles):
    for letra in ascii_letters:
        if letra not in simbolosPosibles:
            tabla_alterada[i][j] = letra
            break
    
    return tabla_alterada
            
def cambiarSimbolo(tabla_alterada, i, j, simbolosPosibles):
    for letra in ascii_letters:
        if letra in simbolosPosibles and tabla_alterada[i][j] != letra:
            tabla_alterada[i][j] = letra
            break
    
    return tabla_alterada
		

def encontrarIlegales(tablon_alterado, n, transiciones, blanco, simbolosPosibles):
    ilegales = {'ventana':[], 'mensaje':[], 'posicion':[]}
    for i in range(0,n-1,1):
        for j in range(1,n-1,1):
            mensaje, legal = esLegal(tablon_alterado, transiciones, i+1, j+1, blanco, simbolosPosibles)
            
            if(not legal):
                _, ventana = cogerVentana(tablon_alterado, i+1,j+1)
                ilegales['ventana'].append(ventana)
                ilegales['mensaje'].append(mensaje)
                ilegales['posicion'].append((i+1,j+1))
    
    return ilegales



