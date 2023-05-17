import re
import phi_star_generator
import phi_accept_generator
import phi_cell_generator
import phi_move_generator

#import informationToTxt

####################################################################################################
##################################      FUNCIONES :     ############################################
####################################################################################################


def generarProposicionesPotenciales(tabla, estados, alfabetoCinta):
    #se genera a partir de cada casilla del tablón
    #alfabetoCinta = alfabetoCinta
    posiblesValores = estados + alfabetoCinta
    posiblesValores.append('#')
    proposicionesPotenciales = [] 
    #A cada fila y celda le corresponden |C| valores
    i=1 #contador de filas
    j=1 #contador de columnas
    for fila in tabla:
        for celda in fila:
            proposicionesFila = []
            for valor in posiblesValores:
                proposicion = 'X' +  "_" +str(i) + "_" + str(j) + "_" + valor
                proposicionesFila.append(proposicion)
            proposicionesPotenciales.append(proposicionesFila)
            j += 1

        i += 1
        j = 0 #reiniciamos las columnas
    
    return proposicionesPotenciales



####################################################################################################
####################################     APLICACION:  ##############################################
####################################################################################################

def apply(n, tabla, estados, alfabetoCinta, configuracionInicial, estadosFinales, reglas_en_orden, transitions, blanco):
    
    #print(configuracionInicial)
    #Pongo los estados en el formato adecuado:
    estados = estados 
    proposicionesPotenciales = generarProposicionesPotenciales(tabla, estados, alfabetoCinta)
    #print(proposicionesPotenciales)
    phi_start, phi_start_valores, valorTotal_phi_start, phi_start_latex, phi_start_valores_latex = phi_star_generator.generarPhiStart(n, tabla, proposicionesPotenciales, configuracionInicial)
    """  print()
    print("PHI_START:")
    print(phi_start)
    print()
    print("PHI_START_VALORES ASIGNADOS:")
    print(phi_start_valores)  """
    
    phi_accept, phi_accept_valores, valorTotal_phi_accept, phi_accept_latex, phi_accept_valores_latex = phi_accept_generator.generarPhiAccept(tabla, estadosFinales, n)
    """ print()
    print("PHI_ACCEPT:")
    print(phi_accept)
    print()
    print("PHI_ACCEPT_VALORES ASIGNADOS:")
    print(phi_accept_valores)  """
    #  if(loCumpleAccept):
    #       print('SI tiene un estado final')
    #   else:
    #       print('NO tiene un estado final')
    #   
    #   print(estadosFinales)

    phi_cell, phi_cell_valores, valorTotal_phi_cell, phi_cell_latex, phi_cell_valores_latex= phi_cell_generator.generarPhiCell(tabla, n, estados, alfabetoCinta)
    """ print()
    print("PHI_CELL:")
    print(phi_cell)
    print()
    print("PHI_CELL_VALORES ASIGNADOS:")
    print(phi_cell_valores)   """
    
    phi_move, phi_move_valores, valorTotal_phi_move,  phi_move_latex, phi_move_valores_latex= phi_move_generator.generarPhiMove(tabla, n, transitions, blanco)
    #informationToTxt.depuracion(txt)
    """ print()
    print("PHI_MOVE:")
    print(phi_move)
    print()
    print("PHI_MOVE_VALORES ASIGNADOS:")
    print(phi_move_valores)  """
    #de las proposiciones de arriba se genera un AND que contiene sólo algunas 
    #de las variables generadas por la fila 1
    #phi_start = generarPhiStart(tabla, proposicionesPotenciales, configuracionInicial)   

    phi = phi_start + " AND " + phi_accept + " AND " + phi_cell + " AND " + phi_move
    valorTotal_phi = valorTotal_phi_start and valorTotal_phi_accept and valorTotal_phi_cell and valorTotal_phi_move
    return phi, phi_start, phi_accept, phi_cell, phi_move, phi_start_valores, phi_accept_valores, phi_cell_valores, phi_move_valores , valorTotal_phi, valorTotal_phi_start, valorTotal_phi_accept, valorTotal_phi_cell, valorTotal_phi_move, phi_start_latex, phi_accept_latex, phi_cell_latex,  phi_move_latex , phi_start_valores_latex, phi_accept_valores_latex, phi_cell_valores_latex, phi_move_valores_latex

