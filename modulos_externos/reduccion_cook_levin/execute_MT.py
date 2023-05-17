# QUE HACE: ejecuta una maquina de turing traducida a texto
# QUÉ QUIERO DE AQUÍ: sacar las transiciones para hacer la tabla

import execute_controller

# Rellena las cintas con los valores del archivo
def get_tapes(tapes, config):
    valide_value = config[1]
    valide_value = valide_value + config[3]
    for i in tapes:
        if i not in valide_value:
            print ("Valor insertado en la cinta incorreto")
            print('Valores de entrada válidos: ')
            print(valide_value)
            return -3
    return tapes

def machine(config, tapes, transitions, filas_tabla, reglas_utilizadas_en_orden):
    # Crea una cola para el control de flujo
    q = []
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
    
    # Insertar elemento al final de la fila
    q.append(setting)
    tape = setting['tape']
    
###################################################################################################
###################################################################################################
    while True:
        tape = setting['tape']
        
        # Se ha encontrado el estado final
        if (q[0]['current_state'] in config[6]):
            print ("Computación terminada y aceptada.")
            #Hay que introducir la fila de aceptación
            filaTabla = execute_controller.crearFilaTabla(tape, setting)
            filas_tabla.append(filaTabla)
            return 0
            
        # La máquina se ha quedado en un bucle
        if (q[0]['counter'] == 0):
            while True:
                x = input("Máquina alcanzo 500 transiciones. Desea continuar? (s - Si | n - No): ")
                
                if(x == 'n'):
                    print ("Computacion no terminada. (interrumpida por looping)")
                    return -2
                
                elif(x == 's'):
                    q[0]['counter'] = 5000
                    break

        # Obtiene la posición de la cinta en la configuración actual
        head = q[0]['head_tape']

        # Encontrar posibles transiciones
        # no se puede romper el for, parará cuando no hayan más transiciones posibles
        for i in range(1, len(transitions) + 1, 1):
            # Si estado_atual_maquina == estado_atual_cinta y letra_cinta == letra_transicion
            if ((q[0]['current_state'] == transitions[i][0]) and (tape[head] == transitions[i][2])):
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
                    "counter": q[0]['counter'] - 1
                }

                q.append(new_setting) # Se inserta al final de la cinta
                filaTabla = execute_controller.crearFilaTabla(tape, setting)
                filas_tabla.append(filaTabla)
                reglas_utilizadas_en_orden.append(transitions[i])
            
           
        
        # Cerró todas las opciones posibles y no encontró ningún estado final
        if (len(q) == 1): # q solo tiene q[0]
            print ("Computación terminada y rechazada.")
            return -1
        
        # Configura máquina para próximo estado
        setting['tape'] = q[1]['tape']
        setting['current_state'] = q[1]['current_state']
        setting['head_tape'] = q[1]['head_tape']
        setting['counter'] = q[1]['counter']
        q.pop(0) # Tira estado atual da fila




