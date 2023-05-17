from os import system, name
import phi_cell_generator
import phi_move_generator
import latex_generator

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

    """ def mainMensaje():
    print(colored(26, 26, 255,'Bienvenido/a/e. Introduce cómo quieres que funcione el programa: '))
    print(colored(102, 255, 102, '1 : Introducir un archivo .jff o .txt junto a una palabra y ejecutar la MT. ( USO: [MT en .txt o .jff] [entrada de la MT] )'))
    print(colored(102, 255, 102,'2 : Introducir un .txt con la tabla formateada correctamente, otro con la información de la MT y la palabra de entrada '))
     """
def mostrarComandosPosibles():
    print(colored(102, 255, 102,'help (h): muestra este mensaje'))
    print(colored(102, 255, 102,'quit (q): termina el programa. '))
    print(colored(102, 255, 102,'ventanas (v) : introduciendo un número de fila i y de columna j se mostrará una ventana y se dirá si es legal o no y el por qué.'))
    print(colored(102, 255, 102,'start (s) : explicación de phi_start.'))
    print(colored(102, 255, 102,'accept (a) : explicación de phi_accept.'))
    print(colored(102, 255, 102,'cell (c) : explicación de phi_cell, introduciendo un numero i (fila) y otro j (columna) de celda.'))
    print(colored(102, 255, 102,'move (m): explicación de phi_move, introduciendo un numero i (fila).'))
    print(colored(102, 255, 102,'alterado (ta): Se genera un Latex con un tablon alterado aleatoriamente, con sus ventanas ilegales y respectivas formulas phi.'))
    print()
    input('Presiona ENTER para continuar.')
    clear()

    
def explicacionPhi_start(phi_start, entrada):
    print(colored(26, 26, 255,'La fórmula booleana phi_start quiere representar el que la primera fila del tablón contenga la configuración de inicio con w a la entrada.'))
    print(colored(0, 179, 0, 'En otras palabras, lo que refleja la fórmula es que la primera fila del tablón contenga el estado inicial junto a la palabra de entrada (seguida de tantos símbolos blancos como sea necesario) de manera correcta, y no otra cosa.'))
    print()
    print(colored(0, 179, 0, 'En la reducción después se asignará con valor de verdad (True) aquellos literales de esta fórmula que efectivamente estén en el tablón.'))
    print()
    print(colored(0, 179, 0,'La fórmula genérica es esta: '))
    print()
    print(colored(255, 255, 0, 'phi_ start = x_1_1_# AND x_1_2_q0 AND x_1_3_w1 AND x_1_4_w2 AND [· · ·] AND x_1_(n+2)_wn'))
    print(colored(255, 255, 0, 'AND x_1_(n+3)_B AND x_1_(n+4)_B AND [· · ·] AND x_1_(nk−1)_B AND x_1_(nk)_#'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    print(colored(0, 179, 0,'La fórmula phi_start para esta MT con la palabra \''+entrada+'\' es: '))
    print()
    print(colored(255, 255, 0,phi_start))
    print()
    input('pulsa ENTER para volver al menú principal')
    clear()


def explicacionPhi_accept(phi_accept, estadosFinales, entrada):
    print(colored(26, 26, 255,'La fórmula booleana phi_accept quiere representar el que alguna de las filas del tablón tiene que corresponder a una configuración de aceptación.'))
    print(colored(0, 179, 0, 'En otras palabras, lo que refleja es que se encuentre al menos un estado final en cualquier celda del tablón.'))
    print()
    print(colored(0, 179, 0, 'En la reducción después se asignará con valor de verdad (True) aquellos literales de esta fórmula que efectivamente estén en el tablón.'))
    print()
    print(colored(0, 179, 0,'La fórmula genérica es esta: '))
    print()
    print(colored(255, 255, 0, 'phi_accept = OR[1 ≤ i,j ≤ nk] x_i_j_qAccept'))
    print()
    print(colored(0, 179, 0, 'La fórmula lo que quiere decir es que va a crear un literal X_i_j_qAceptación para cada celda i,j del tablón y los va a unir con OR\'s lógicos.'))
    print(colored(0, 179, 0, 'Si en la tabla hay efectivamente un estado de aceptación, hará que la fórmula tenga valor verdadero (True)'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    estados = " ".join(estadosFinales)
    msj = colored(0, 179, 0, 'Los estados finales de esta MT son : ' + estados)
    print(msj)
    print()
    print(colored(0, 179, 0,'La fórmula phi_accept para esta MT con la palabra \''+entrada+'\' es: '))
    print()
    print(colored(255, 255, 0,phi_accept))
    print()
    input('pulsa ENTER para volver al menú principal')
    clear()

def explicacionPhi_Cell(tabla, estados, alfabetoCinta, i, j):
    print(colored(26, 26, 255,'La fórmula booleana phi_Cell quiere representar el que para cada celda concreta de la fila i y la columna j del tablón, una y sólo una de sus'))
    print(colored(26, 26, 255, 'correspondientes |C| variables puede estar a 1 (True) y las demás tienen que estar a 0 (False).'))
    print()
    print(colored(0, 179, 0, 'En otras palabras, lo que refleja es que por cada celda debe haber uno, y solo uno, de los valores posibles.'))
    print(colored(0, 179, 0, 'Recordemos que \'C \' es un conjunto que consiste en la unión de el alfabeto de la cinta, el conjunto de estados, el símbolo que representa al Blanco (\'B\' u otro) y el símbolo \'#\'.'))
    print(colored(0, 179, 0, 'O de otra manera, C contiene a todos los símbolos que puede contener el tablón.'))
    print()
    print(colored(0, 179, 0,'La fórmula genérica es esta: '))
    print()
    print(colored(255, 255, 0, 'phi_Cell = AND[1≤i,j≤nk] [ (OR[s∈C] x_i_j_s) AND ( AND[s,t∈C;s̸=t] ( NOT(x_i_j_s) OR NOT(x_i_j_t) ) ) ]'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    print(colored(0, 179, 0,'La fórmula genérica es esta: '))
    print(colored(255, 255, 0, 'phi_Cell = AND[1≤i,j≤nk] [ (OR[s∈C] x_i_j_s) AND ( AND[s,t∈C;s̸=t] ( NOT(x_i_j_s) OR NOT(x_i_j_t) ) ) ]'))
    print()
    print(colored(0, 179, 0, 'La fórmula se va a explicar por partes. Lo primero que encontramos es: \'AND[1≤i,j≤nk]\', esto refela que debe cumplirse para todas las celdas de la tabla, es decir que se va a unir la fórmula con un \'AND\' para que se cumplimente esta condición.'))
    print(colored(0, 179, 0, 'Ahora analizamos la fórmula en sí, lo que debe cumplirse por cada celda. La dividiremos en dos partes: '))
    print()
    print(colored(0, 179, 0, 'Primera parte: \' (OR[s∈C] x_i_j_s) \'.'))
    print(colored(0, 179, 0, 'Esta parte representa el que al menos un símbolo \'s\'∈C esté contenido dentro de la celda. Si esto no ocurriera, en la celda hubiera un símbolo que no pertenece a C (o no hubiera símbolo), esta parte daría False.'))
    print()
    print(colored(0, 179, 0, 'Segunda parte: \'( AND[s,t∈C;s̸=t] ( NOT(x_i_j_s) OR NOT(x_i_j_t) ) )\'.'))
    print(colored(0, 179, 0, 'Esta parte representa el que solo haya un símbolo contenido en esa celda, es decir, que una celda no contenga más de un valor.'))
    print(colored(0, 179, 0, 'Para ello se \'comparan\' dos símbolos \'s\' y \'t\', ambos pertenecientes a C y diferentes, y se comprueba que dentro de la celda o no esté contenido s, o no esté contenido t, pero lo que no puede ocurrir es que ambos estén dentro.'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    phi_cell_min, phi_cell_min_valores, primeraParte, segundaParte = phi_cell_generator.generarPhiCell_soloUna(tabla, estados, alfabetoCinta, int(i), int(j))
    print(colored(0, 179, 0,'Ahora mostraremos, para la celda introducida, lo que correspondería a la primera y segunda parte que se acaban de explicar : '))
    print()
    print(colored(0, 179, 0, 'Primera parte: \' (OR[s∈C] x_i_j_s) \'.'))
    print()
    print(colored(255, 255, 0, primeraParte))
    print()
    print(colored(0, 179, 0, 'Segunda parte: \'( AND[s,t∈C;s̸=t] ( NOT(x_i_j_s) OR NOT(x_i_j_t) ) )\'.'))
    print()
    print(colored(255, 255, 0, segundaParte))
    print()
    input('pulsa ENTER para continuar')
    clear()
    print(colored(0, 179, 0,'Ahora mostraremos la fórmula phi_cell completa en esta celda en particular :'))
    print()
    print(colored(255, 255, 0, phi_cell_min))
    print()
    input('pulsa ENTER para volver al menú principal')
    clear()


def explicacionPhi_move(tabla, n, transitions, i, blanco):
    print(colored(26, 26, 255,'La fórmula booleana phi_move quiere representar el que cada configuración de cada fila siga legalmente a la anterior según establece la función de transición de N, δ.'))
    print()
    print(colored(0, 179, 0, 'En otras palabras, lo que refleja es que cada fila sea legal teniendo en cuenta la anterior.'))
    print(colored(0, 179, 0, 'En este caso hemos tenido en cuenta que una fila es legal cuando: 1) es exactamente igual que su anterior (debido a la posibilidad de transiciones Stay), y 2) cuando la fila siguiente corresponde a haber realizado una de las transiciones posibles (contenidas en δ).'))
    print()
    print(colored(0, 179, 0,'La fórmula genérica es esta: '))
    print()
    print(colored(255, 255, 0, 'phi_Move = AND[1≤i,j≤nk] ( OR[a1···a6 is a legal window] ( x_i_j−1_a1 AND x_i_j_a2 AND x_i_j+1_a3 AND x_i+1_j−1_a4 AND x_i+1_j_a5 AND x_i+1_j+1_a6 ))'))
    print()
    print(colored(0, 179, 0,'Lo primero que encontramos es: \'AND[1≤i,j≤nk]\', esto refela que debe cumplirse para todas las celdas de la tabla, es decir que se va a unir la fórmula con un \'AND\' para que se cumplimente esta condición.'))
    print(colored(0, 179, 0,'Lo siguiente que nos encontramos representa que en la fórmula se van a unir todas las posibles ventanas legales mediante OR\'s, teniendo que cumplirse una de ellas.'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    phi_move_min, phi_move_valores_min, igual, posibles = phi_move_generator.generarPhi_move_UnaSolo(tabla, n, transitions, int(i), blanco)
    print(colored(0, 179, 0,'A pesar de que en la teoría se explica con ventanas, nosotros lo vamos a estudiar ahora de manera diferente. Por ello en el menú hay otra opción para ver cuando una ventana es legal o no.'))
    print(colored(0, 179, 0,'Nuestra fórmula va a ser la siguiente: '))
    print(colored(255, 255, 0, 'phi_Move = AND[1≤i,j≤nk] ( OR[fila \'i\' es una fila legal] ( (que sean iguales las filas i e i+1)|(que la fila i+1 se haya creado con una funcion de transicion a partir de la fila i) ) )'))
    print()
    print(colored(0, 179, 0,'Para la fila i seleccionada, el caso en el que sean iguales la fila i y su siguiente es: '))
    print(colored(255, 255, 0, igual))
    print()
    print(colored(0, 179, 0,'Las otras posibles filas legales (creadas a través de una función de transición) serían:'))
    if(posibles == ""):
        print(colored(255, 255, 0,'En este caso concreto no existen otras filas posibles, debe ser igual que la anterior.'))
    else:
        print(colored(255, 255, 0, posibles))
    print()
    input('pulsa ENTER para continuar')
    clear()
    print(colored(0, 179, 0,'Nuestra fórmula va a ser la siguiente: '))
    print(colored(255, 255, 0, 'phi_Move = AND[1≤i,j≤nk] ( OR[fila \'i\' es una fila legal] ( (que sean iguales las filas i e i+1)|(que la fila i+1 se haya creado con una funcion de transicion a partir de la fila i) ) )'))
    print()
    print(colored(0, 179, 0, 'Para esta fila, su parte en la fórmula phi_move en este caso concreto sería:'))
    print()
    print(colored(255, 255, 0,phi_move_min))
    print()
    input('pulsa ENTER para volver al menú principal')
    clear()




#TODO: REVISAR el esLegal de ventanas (que solo me devuelva un mensaje es mas comodo)
def explicacionVentanas(tabla, transiciones, i, j, blanco, simbolosPosibles):
    print(colored(26, 26, 255,'Vamos a analizar la ventana seleccionada.'))
    _, ventana = phi_move_generator.cogerVentana(tabla, i,j)
    fila_1 = ventana[0]
    fila_2 = ventana[1]
    print()
    print(colored(255, 255, 0, fila_1))
    print(colored(255, 255, 0, fila_2))
    print()
    print(colored(0, 179, 0, 'Ahora procedemos a estudiar si es legal o no y por qué.'))
    print()
    input('pulsa ENTER para continuar')
    clear()
    print(colored(255, 255, 0, fila_1))
    print(colored(255, 255, 0, fila_2))
    print()

    mensaje, esLegal = phi_move_generator.esLegal(tabla, transiciones, i, j, blanco, simbolosPosibles)

    print(colored(0, 179, 0, mensaje))

    print()
    input('pulsa ENTER para volver al menú principal')
    clear()


def mainloop(phi_start, phi_accept, phi_cell, phi_move, tabla, n, estadosFinales, entrada, estados, alfabetoCinta, transitions, blanco, simbolosPosibles, nombreDeMT, tablon_alterado, transiciones):
    quit = False
    print(colored(0, 179, 0, "Bienvenido/a/e, introduce lo que quieres hacer."))
    print(colored(0, 179, 0, "Para ver las posibles opciones, introduce 'h' (de help): "))

    while(not quit):
        print(colored(0,0,255,'¡Bienvenida/o/e al menú principal!'))
        print(colored(0,0,255, "Introduce el comando correspondiente a lo que quieres hacer."))
        print(colored(0,0,255, "Para ver las posibles opciones, introduce 'h' (de help)"))
        comando = input()
        clear()
        if(comando == 'h' or comando == 'help'):
            mostrarComandosPosibles()
        elif(comando == 'q' or comando == 'quit'):
            print(colored(0,0,255,'¡Adiós!'))
            exit(1)
        elif(comando == 'v' or comando == 'ventanas'):
            print(colored(255, 255, 0, 'EXPLICACIÓN VENTANAS'))
            # j debe ser mayor que 1 y menor que n
            # i debe ser menor que n
            print(colored(0, 179, 0, 'Se van a analizar ventanas, recuerda que una ventana era así: '))
            print(colored(0, 179, 0, 'a1 a2 a3'))
            print(colored(0, 179, 0, 'a4 a5 a6'))
            print(colored(0, 179, 0, 'Una ventana se localiza por la celda a2 (central).'))
            i = input('introduce el número de fila de la ventana: ')
            j = input('introduce el número de columna de la ventana: ')
            correct = False
            while(not correct):
                if( int(j) <= 1 or ( int(i) >= n or int(j) >= n)):
                    print(colored(255,0,0, 'Has introducido un valor de celda incorrecto, la columna debe ser mayor que 1 y tanto la fila como la columna deben ser menor que n (siendo n el tamaño del tablón).'))
                    print(colored(255,0,0, 'El tamaño del tablón actual es de '+ str(n) + " X "+ str(n)))
                    print(colored(255,0,0, 'Intentalo de nuevo.'))
                else:
                    correct = True
            clear()
            explicacionVentanas(tabla, transitions, int(i), int(j), blanco, simbolosPosibles)
        elif(comando == 's' or comando == 'start'):
            print(colored(255, 255, 0, 'EXPLICACIÓN PHI_START'))
            explicacionPhi_start(phi_start, entrada)
        elif(comando == 'a' or comando == 'accept'):
            print(colored(255, 255, 0, 'EXPLICACIÓN PHI_ACCEPT'))
            explicacionPhi_accept(phi_accept, estadosFinales, entrada)
        elif(comando == 'c' or comando == 'cell'):
            print(colored(255, 255, 0, 'EXPLICACIÓN PHI_CELL'))
            correct = False

            while(not correct):
                i = input('introduce el número de fila de la celda a analizar: ')
                j = input('introduce el número de columna de la celda a analizar: ')
                if((i == '0' or j== '0') or ( int(i) > n-1 or int(j) > n-1)):
                    print(colored(255,0,0, 'Has introducido un valor de celda incorrecto, debe ser de 1 hasta n-1 (siendo n el tamaño del tablón).'))
                    print(colored(255,0,0, 'El tamaño del tablón actual es de '+ str(n) + " X "+ str(n)))
                    print(colored(255,0,0, 'Intentalo de nuevo.'))
                else: 
                    correct = True

            clear()
            explicacionPhi_Cell(tabla, estados, alfabetoCinta, i, j)
        elif(comando == 'm' or comando == 'move'):
            print(colored(255, 255, 0, 'EXPLICACIÓN PHI_MOVE'))
            correct = False

            while(not correct):
                i = input('introduce el número de fila a analizar: ')
                if((i == '0' ) or ( int(i) > n-1)):
                    print(colored(255,0,0, 'Has introducido un valor de fila incorrecto, debe ser de 1 hasta n-1 (siendo n el tamaño del tablón).'))
                    print(colored(255,0,0, 'El tamaño del tablón actual es de '+ str(n) + " X "+ str(n)))
                    print(colored(255,0,0, 'Intentalo de nuevo.'))
                else: 
                    correct = True

            explicacionPhi_move(tabla, n, transitions, i, blanco)
        elif(comando == 'ta' or comando == 'alterado'):
            print(colored(255, 255, 0, 'CREACION DEL LATEX CON TABLÓN ALTERADO.\n'))
            print(colored(0, 179, 0, 'El Latex tendrá el nombre de la MT introducida más \'_tablonAlterado\'.'))
            latex_generator.tablonAlterado(nombreDeMT, tablon_alterado, n, transiciones, blanco, simbolosPosibles)
            print()
            input('pulsa ENTER para volver al menú principal')
            clear()
        else:
            print(colored(255,0,0,'Has introducido un comando invalido, si necesitas ayuda introduce h (help)'))