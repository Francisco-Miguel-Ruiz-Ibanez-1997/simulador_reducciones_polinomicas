import re

####################################################################################################
####################################     PHI_CELL     ##############################################
####################################################################################################

def generarPrimeraParte(i,j,valor,valoresPosibles):
    #como minimo cada celda debe tener un valor.
    primeraParte_latex='[\\ (\\ '
    primeraParteValor_latex='[\\ (\\ '
    primeraParte = "[ ("
    primeraParteValor = "[ ("
    estaBien = False
    tam = len(valoresPosibles)
    esEstado = re.compile("q[0-9]*")
    eshastag= re.compile("#")
    
        
  

    for e in range(0,tam,1):
        valorP = valoresPosibles[e]
        match = re.fullmatch(esEstado, valorP)
        match_hastag = re.fullmatch(eshastag, valorP)
        if(e < tam-1):
            if(match):
                num_estado = valorP[1]
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_q_"+num_estado+"$\\ $\\vee$\\ "
            elif(match_hastag):
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_\\#$\\ $\\vee$\\ "
            else:
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_"+valorP+"$\\ $\\vee$\\ "

            primeraParte += "X_" + str(i) +"_" + str(j) + "_" + valoresPosibles[e] + " OR " 
            if(valoresPosibles[e] == valor):
                estaBien = True
                primeraParteValor_latex +='True\\ $\\vee$\\ '
                primeraParteValor += "True OR "
            else:
                primeraParteValor_latex +='False\\ $\\vee$\\ '
                primeraParteValor += "False OR "
        else:
            if(match):
                num_estado = valorP[1]
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_q_"+num_estado+"$\\ )\\ "
            elif(match_hastag):
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_\\#$\\ )\\ "
            else:
                primeraParte_latex += "$X_"+ str(i) +",_" + str(j) +"\\_"+valorP+"$\\ )\\ "

            primeraParte += "X_" + str(i) +"_" + str(j) + "_" + valoresPosibles[e] + " ) "
            if(valoresPosibles[e] == valor):
                estaBien = True
                primeraParteValor_latex +='True\\ )\\ '
                primeraParteValor += "True ) "
            else:
                primeraParteValor_latex +='False\\ )\\ '
                primeraParteValor += "False ) "

    return primeraParte, primeraParteValor, estaBien, primeraParte_latex, primeraParteValor_latex

def generarSegundaParte(i,j,valor,valoresPosibles):
    segundaParteValor_latex = '(\\ '
    segundaParte_latex = '(\\ '
    segundaParte = "( " 
    segundaParteValor = "( " 
    estaBien = True

    esEstado = re.compile("q[0-9]*")
    eshastag= re.compile("#")
    
    #no pueden haber dos valores simultaneamente
    tam = len(valoresPosibles)
    for index in range(0, tam-1, 1):
        numNext = index + 1
        s = valoresPosibles[index]
        for numNext in range(numNext, tam, 1):
            t = valoresPosibles[numNext]
            #print("s = " +s+ " t =" + t + " index = "+ str(index) + " numNext = "+ str(numNext))
            if(t != s):
                if(s == valor):
                    valorS ='True'
                else:
                    valorS ='False'

                if(t == valor):
                    valorT ='True'
                else:
                    valorT ='False'

                if(valorS == valorT == True):
                    #print("Segunda parte: falla con valores i="+str(i)+" j="+str(j)+" valor en la tabla="+valor)
                    #print("valor de s = "+ s + "valor de t = "+ t)
                    estaBien = False
                
                match = re.fullmatch(esEstado, s)
                match_hastag = re.fullmatch(eshastag, s)
                s_latex = s
                if(match):
                    num_estado = s[1]
                    s_latex = 'q_'+num_estado
                elif(match_hastag):
                    s_latex = '\\#'

                match = re.fullmatch(esEstado, t)
                match_hastag = re.fullmatch(eshastag, t)
                t_latex = t
                if(match):
                    num_estado = t[1]
                    t_latex = 'q_'+num_estado
                elif(match_hastag):
                    t_latex = '\\#'

                if index < tam-2:
                    segundaParte_latex += '\\ $\\neg$\\ $(X_'+ str(i)+",_"+str(j)+"\\_"+s_latex+')$\\ $\\vee$\\ $\\neg$\\ $(X_'+ str(i)+",_"+str(j)+"\\_"+t_latex+')$\\ )\\ $\\wedge$\\ (\\ '
                    segundaParte += " NOT ("+ "X_"+ str(i)+"_"+str(j)+"_"+s + ") OR  NOT ( " + "X_"+ str(i)+"_"+str(j)+"_"+ t +")  ) AND ( "
                    segundaParteValor_latex += " $\\neg$\\ "+ str(valorS) + " $\\vee$\\  $\\neg$\\ " + str(valorT) +")\\ $\\wedge$\\ (\\ "
                    segundaParteValor += " NOT ("+ str(valorS) + ") OR  NOT ( " + str(valorT) +")  ) AND ( "
                else:
                    segundaParte_latex += '\\ $\\neg$ $(X_'+ str(i)+",_"+str(j)+"\\_"+s_latex+')$\\ $\\vee$\\ $\\neg$ $(X_'+ str(i)+",_"+str(j)+"\\_"+t_latex+')$\\ )\\ ]\\ '
                    segundaParte += " NOT ("+ "X_"+ str(i)+"_"+str(j)+"_"+s + ") OR  NOT ( " + "X_"+ str(i)+"_"+str(j)+"_"+ t +")  ) ]"
                    segundaParteValor_latex += " $\\neg$\\ "+ str(valorS) + " $\\vee$\\  $\\neg$\\ " + str(valorT) +")\\ )\\ ]\\ "
                    segundaParteValor += " NOT ("+ str(valorS) + ") OR  NOT ( " + str(valorT) +")  ) ]"
    
    return segundaParte, segundaParteValor, estaBien, segundaParte_latex, segundaParteValor_latex

def generarPhiCell(tabla, n, estados, alfabetoCinta):
    phi_cell_latex=''
    phi_cell_valores_latex=''
    phi_cell=""
    phi_cell_valores = ""
    valoresPosibles = estados + alfabetoCinta + ["#"]    #conjunto de valores posibles (en la nomenclatura de la asignatura se llama "C")
    valorTotal = True

    for i in range(0,n,1):
        for j in range(0,n,1):
            primeraParte, primeraParteValor, estaBien, primeraParte_latex, primeraParteValor_latex = generarPrimeraParte(i+1,j+1,tabla[i][j],valoresPosibles)
            valorTotal = estaBien
            #print("PRIMERA PARTE DE LA FORMULA, ESTABIEN = " + str(estaBien))
            phi_cell_latex += primeraParte_latex + '\\ $\\wedge$ \\ '
            phi_cell += primeraParte + " AND "
            phi_cell_valores_latex+= primeraParteValor_latex + '\\ $\\wedge$ \\ '
            phi_cell_valores += primeraParteValor + " AND "

            segundaParte, segundaParteValor, estaBien, segundaParte_latex, segundaParteValor_latex = generarSegundaParte(i+1,j+1,tabla[i][j],valoresPosibles)
            valorTotal = estaBien
            #print("SEGUNDA PARTE DE LA FORMULA, ESTABIEN = " + str(estaBien))
            if( j == n-1 and i == n-1): #Estoy en el ultimo caso
                phi_cell_latex += segundaParte_latex 
                phi_cell += segundaParte 
                phi_cell_valores_latex+= segundaParteValor_latex
                phi_cell_valores += segundaParteValor 
                
            else:
                phi_cell_latex += segundaParte_latex + '\\ $\\wedge$ \\ '
                phi_cell += segundaParte + " AND "
                phi_cell_valores_latex+= segundaParteValor_latex+ '\\ $\\wedge$ \\ '
                phi_cell_valores += segundaParteValor + " AND "

    return  phi_cell, phi_cell_valores, valorTotal, phi_cell_latex, phi_cell_valores_latex

#funcion para la explicacion de phi_cell
def generarPhiCell_soloUna(tabla, estados, alfabetoCinta, i, j):
    #por como pido los datos al usuario:
    i = i-1
    j = j-1
    phi_cell_min="[ "
    phi_cell_min_valores = "[ "
    valoresPosibles = estados + alfabetoCinta + ["#"]    #conjunto de valores posibles (en la nomenclatura de la asignatura se llama "C")
    
    primeraParte, primeraParteValor, _, _, _ = generarPrimeraParte(i+1,j+1,tabla[i][j],valoresPosibles)
    #print("PRIMERA PARTE DE LA FORMULA, ESTABIEN = " + str(estaBien))
    phi_cell_min += primeraParte + " AND "
    phi_cell_min_valores += primeraParteValor + " AND "

    segundaParte, segundaParteValor, _, _, _= generarSegundaParte(i+1,j+1,tabla[i][j],valoresPosibles)
    #print("SEGUNDA PARTE DE LA FORMULA, ESTABIEN = " + str(estaBien))

    phi_cell_min += segundaParte  + " ]"
    phi_cell_min_valores += segundaParteValor + " ]"


    return  phi_cell_min, phi_cell_min_valores, primeraParte, segundaParte