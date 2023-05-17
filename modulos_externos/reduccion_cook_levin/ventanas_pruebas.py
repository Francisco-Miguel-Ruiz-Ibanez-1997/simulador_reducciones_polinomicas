import re
import phi_move_generator
import codecs

""" 
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

def esLegal(tabla, transiciones, i, j, blanco):
    fila, ventana = cogerVentana(tabla, i, j)
    mensaje = ''
    code = 0

    #  = 1 si es igual
    es, mensaje = phi_move_generator.ventanaEsIgual(ventana)
    if (not es):
        code = 1
        return mensaje, code

    #-6 si es del primer tipo, -7 si es del segundo
    mensaje, code = phi_move_generator.incumpleHastag(ventana)
    if(mensaje != ""):
        return mensaje, code

    #  = -1 tiene mas de un estado en la primera fila
    #  = -2 si es en la segunda
    #  = -3 si es en las dos
    seCumple, code, mensaje = phi_move_generator.ventanaTieneMasDeUno(ventana)
    if(seCumple):
        return mensaje, code
     
        
    #  = -4 tiene estado en el medio de la primera fila y en la segunda no (no esta ni a su derecha ni a su izq ni en la misma posicion)
    tieneSentido, mensaje = phi_move_generator.ventanaNoSentido(ventana)
    if(not tieneSentido):
        code = -4
        return mensaje, code
    #  = 2 si por transicion es congruente
    #  = -5 es incongruente por transicion
    code, mensaje = phi_move_generator.ventanaTransicion(ventana, transiciones, fila, j, blanco)

    return mensaje, code
 """
def  crear_eles_tabuladas(n):
    eles = '|'
    for i in range(0,n,1):
        eles+='l|'
    return eles

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

""" 
    print('tabla alterada: ')
    for fila in tabla_alterada:
        print(fila)
    print('\n\n')

    for i in range(0,n-1,1):
        for j in range(1,n-1,1):
            _, ventana = cogerVentana(tabla_alterada, i+1, j+1)

            mensaje, code = incumpleHastag(ventana)

            if( mensaje != ""):
                for fila in ventana:
                    print(fila)
                print()
                print(mensaje)
                print('\n\n') """

def ventanaTransicion(ventana, transiciones, fila, j, blanco): 
    filasPosibles, transiciones_utilizadas = phi_move_generator.generarFilas(fila, transiciones, blanco)
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
    fila, ventana = phi_move_generator.cogerVentana(tabla, i, j)
    legal = True
    mensaje = ''

    #si es igual
    es, mensaje = phi_move_generator.ventanaEsIgual(ventana)
    if (es):
        return mensaje, legal

    #ver si tiene un simbolo que no pertenece al tablon.
    mensaje, tiene = phi_move_generator.simboloProhibido(ventana, simbolosPosibles)
    if(tiene):
        legal = False
        return mensaje, legal

    #hay varios dos tipos
    mensaje, loIncumple = phi_move_generator.incumpleHastag(ventana)
    if(loIncumple):
        legal = False
        return mensaje, legal

    #  tiene mas de un estado en la primera fila
    #  si es en la segunda
    #  si es en las dos
    seCumple,  mensaje = phi_move_generator.ventanaTieneMasDeUno(ventana)
    if(seCumple):
        legal = False
        return mensaje, legal
        
    #tiene estado en el medio de la primera fila y en la segunda no (no esta ni a su derecha ni a su izq ni en la misma posicion)
    tieneSentido, mensaje = phi_move_generator.ventanaNoSentido(ventana)
    if(not tieneSentido):
        legal = False
        return mensaje, legal
    #si por transicion es congruente
    #es incongruente por transicion
    mensaje, legal = ventanaTransicion(ventana, transiciones, fila, j-1, blanco)

    return mensaje, legal



def ponerFormulaEnLatex(formula):
    formulaBonita = '$'
    #$X_1_1_\_\#$ AND $X_1_2_\_q_0$ AND $X_1_3_0 AND X_1_4_1 AND X_1_5_#$
    index = 0
    for l in range(0,len(formula),1):
        letra = formula[index]
        if(letra =='X'):
            for i in range(index,index+6,1):
                formulaBonita += formula[i]
            formulaBonita += '\_'
            index = index+5
        elif(letra == '#'):
            formulaBonita += '\\#'
        elif(letra == 'q'):
            formulaBonita += 'q_'
        elif(letra == ' '):
            formulaBonita+= '$'+'\\ '
        else:
            formulaBonita+= letra
        
        index += 1
        if(index > len(formula)-1):
            break
    
    formulaBonita += '$'
    return formulaBonita

def main():
    """ tabla_alterada = [['#', '0', 'q4', '1', '#'],
    ['#', 'B', 'q2', '1', '#'],
    ['#', '#', 'q4', '1', '#'],
    ['#', 'q0', 'q1', '1', '#'],
    ['#', '0', 'q4', '1', '0']] 

    tabla = [['#', 'q0', '0', '1', '#'],
    ['#', '0', 'q2', '1', '#'],
    ['#', '0', 'q4', '1', '#'],
    ['#', '0', 'q4', '1', '#'],
    ['#', '0', 'q4', '1', '#']]
    n = 5
    blanco = 'B'
    simbolosPosibles = ['0', '1', 'B', '#', 'q0', 'q1', 'q2', 'q3', 'q4']

    transiciones = {1: ['0', '1', '0', '0', 'L'], 2: ['0', '2', '0', '0', 'R'], 3: ['0', '3', '0', '0', 'S'], 4: ['1', '1', '0', '0', 'L'], 5: ['1', '4', '1', '1', 'S'], 6: ['2', '2', '0', '0', 'R'], 7: ['2', '4', '1', '1', 'S'], 8: ['3', '3', '0', '0', 'S'], 9: ['3', '4', '1', '1', 'S']}

    for i in range(0,n-1,1):
        for j in range(1,n-1,1):
            mensaje, _ = esLegal(tabla, transiciones, i+1, j+1, blanco, simbolosPosibles)
            _, ventana = cogerVentana(tabla, i+1,j+1)
            for f in ventana:
                print(f)
            print()
            print(mensaje)
            print() """
            
    """ formula = 'X_1_1_# AND X_1_2_q0 AND $X_1_3_0 AND X_1_4_1 AND X_1_5_#'
    nueva = ponerFormulaEnLatex(formula)
    print(nueva)
    print() """
    q = 'q0'
    print(q[1])

main()
