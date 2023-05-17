import re
import codecs
import phi_move_generator
import ntpath

#vaya movida de función esta que voy a hacer. VAYA MOVIDA.
def ponerFormulaEnLatex(formula):
    formulaBonita = '$'
    #formulaBonita = ''
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
            #formulaBonita+= '$'+'\\ '
            formulaBonita+= '\\ '
        else:
            formulaBonita+= letra
        
        index += 1
        if(index > len(formula)-1):
            break
    
    formulaBonita += '$'
    return formulaBonita



#solo si la lista es de strings
def listToStr(list):
    str=''
    for x in range(0,len(list), 1):
        num = list[x][1]
        if(x < len(list)-1):
            str += '$q_'+num+'$, '
        else:
            str += '$q_'+num+'$ '
    
    return str


def transicionABonito(t):
    transicion_bonita = ''
    estado_actual = '$q_' + str(t[0]) +'$'
    simbolo_actual = str(t[2])
    estado_nuevo = '$q_' + str(t[1]) +'$'
    nuevo_simbolo = str(t[3])
    d = str(t[4])

    transicion_bonita = '$\\delta$('+estado_actual+','+simbolo_actual+') = ('+estado_nuevo+','+nuevo_simbolo+','+d+')'
    return transicion_bonita
##################################################################
################ LATEX DEL TABLON ALTERADO #######################
##################################################################

def  crear_eles_tabuladas(n):
    eles = '|'
    for i in range(0,n,1):
        eles+='l|'
    return eles

def tablonAlterado(nombreDeMT, tablon_alterado, n, transiciones, blanco, simbolosPosibles):

    outputFile = nombreDeMT+ "_tablon_alterado.tex"
    #outputFile = "tablon_alterado.tex"
    
    with codecs.open(outputFile, 'w', "utf-8-sig") as f:
        #Cosas que importar de manera genérica
        f.write('\\documentclass[a4paper,10pt]{article}\n')
        f.write('\\usepackage[utf8]{inputenc}\n')
        f.write('\\usepackage[spanish,es-tabla]{babel}\n')
        #márgenes del documento
        f.write('\\usepackage[top=3cm, bottom=2cm, right=1.5cm, left=3cm]{geometry}\n')
        f.write('\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\n')
        # Definimos el título
        f.write('\\title{Tablón Alterado}\n')
        name = ntpath.basename(nombreDeMT)
        f.write('\\author{$'+name+'$}\n')
        f.write('\\date{}\n\n')
        #comienzo del documento:
        f.write('\\begin{document}\n')
        f.write('\\maketitle\n\n')

        #####################################################
        ######  tablon alterado, mostrar la tabla ###########
        #####################################################
        f.write('\\section{Tabla alterada}\n\n')
        f.write('Aquí mostraremos la tabla alterada de manera aleatoria. Lo que se puede encontrar es que:\n')
        f.write('\\begin{enumerate}\n')
        f.write('\\item Se haya introducido un carácter que no pertenece al conjunto C.\n')
        f.write('\\item Se haya cambiado un carácter a otro perteneciente al conjunto C.\n')
        f.write('\\item Se haya cambiado la primera fila por otra aleatoria del tablón.\n')
        f.write('\\item Se haya añadido un estado de más.\n')
        f.write('\\item Eliminar estados para quitar el sentido del tablón, cambiándolos por otro signo.\n')
        f.write('\\end{enumerate}')
        
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        eles = crear_eles_tabuladas(n)
        f.write('\\begin{tabular}{'+eles+'}\n')
        f.write('\\hline\n')
        
        esEstado = re.compile("q[0-9]*")
        esHastag = re.compile("#")
        fila_tabla = '\t'

        for i in range(0,n,1):
            for j in range (0,n,1):
                celda = tablon_alterado[i][j]
                match = re.fullmatch(esEstado, celda)
                match_hastag = re.fullmatch(esHastag, celda)
                if(j < n-1):
                    if(match):
                        cont=0
                        fila_tabla += '$'
                        for l in celda:
                            if(cont==0):
                                fila_tabla += l+'_'
                            else:
                                fila_tabla += l
                            cont +=1
                        fila_tabla += '$  &   '
                    elif(match_hastag):
                        fila_tabla += '\\#' +'  &   '
                    else:
                        fila_tabla += celda +'   &   '
                else:
                    if(match):
                        cont=0
                        fila_tabla += '$'
                        for l in celda:
                            if(cont==0):
                                fila_tabla += l+'_'
                            else:
                                fila_tabla += l
                            cont +=1 
                        fila_tabla += '$\t'
                    elif(match_hastag):
                        fila_tabla += '\\#' + '\t'
                    else:
                        fila_tabla += celda + '\t'

            f.write(fila_tabla + '\\\\ \\hline\n')
            fila_tabla = '\t'
  
        f.write('\\end{tabular}\n')
        f.write('\\end{table}\n')
        

       
        ##########  MOSTRAR LAS VENTANAS ILEGALES ###########

        f.write('\\section{Ventanas ilegales}\n')
        f.write('En este apartado se mostrarán las ventanas ilegales que nacen del tablón alterado.\\newline')
        ilegales = phi_move_generator.encontrarIlegales(tablon_alterado, n, transiciones, blanco, simbolosPosibles)
        ventanas = ilegales['ventana']
        mensajes = ilegales['mensaje']
        posiciones = ilegales['posicion']

        for i in range(0, len(ventanas), 1):
            f.write('\\begin{table}[h!]\n')
            f.write('\\centering\n')
            eles = crear_eles_tabuladas(3)
            f.write('\\begin{tabular}{'+eles+'}\n')
            f.write('\\hline\n')

            esEstado = re.compile("q[0-9]*")
            esHastag = re.compile("#")

            ventana_actual = ventanas[i]
            fila_1 = ventana_actual[0]
            fila_2 = ventana_actual[1]
            mensaje_actual = mensajes[i]
            posicion_actual = posiciones[i]
            fila_tabla_1 = '\t'
            fila_tabla_2 = '\t'

            for i in range(0, len(fila_1), 1):
                celda_1 = fila_1[i]
                celda_2 = fila_2[i]
                match_1 = re.fullmatch(esEstado, celda_1)
                match_2 = re.fullmatch(esEstado, celda_2)
                match_hastag_1 = re.fullmatch(esHastag, celda_1)
                match_hastag_2 = re.fullmatch(esHastag, celda_2)
                if(i < len(fila_1)-1):
                    if(match_1):
                        cont=0
                        fila_tabla_1 += '$'
                        for l in celda_1:
                            if(cont==0):
                                fila_tabla_1 += l+'_'
                            else:
                                fila_tabla_1 += l
                            cont +=1
                        fila_tabla_1 += '$  &   '
                    elif(match_hastag_1):
                        fila_tabla_1 += '\\#' +'  &   '
                    else:
                        fila_tabla_1 += celda_1 +'   &   '
                        
                    if(match_2):
                        cont=0
                        fila_tabla_2 += '$'
                        for l in celda_2:
                            if(cont==0):
                                fila_tabla_2 += l+'_'
                            else:
                                fila_tabla_2 += l
                            cont +=1
                        fila_tabla_2 += '$  &   '
                    elif(match_hastag_2):
                        fila_tabla_2 += '\\#' +'  &   '
                    else:
                        fila_tabla_2 += celda_2 +'   &   '
                else:
                    if(match_1):
                        cont=0
                        fila_tabla_1 += '$'
                        for l in celda_1:
                            if(cont==0):
                                fila_tabla_1 += l+'_'
                            else:
                                fila_tabla_1 += l
                            cont +=1
                        fila_tabla_1 += '$\t'
                    elif(match_hastag_1):
                        fila_tabla_1 += '\\#' + '\t'
                    else:
                        fila_tabla_1 += celda_1 + '\t'
                    
                    if(match_2):
                        cont=0
                        fila_tabla_2 += '$'
                        for l in celda_2:
                            if(cont==0):
                                fila_tabla_2 += l+'_'
                            else:
                                fila_tabla_2 += l
                            cont +=1
                        fila_tabla_2 += '$\t'
                    elif(match_hastag_2):
                        fila_tabla_2 += '\\#' + '\t'
                    else:
                        fila_tabla_2 += celda_2 + '\t'

            fila_tabla_1 += '\\\\ \\hline\n'
            fila_tabla_2 += '\\\\ \\hline\n'
        
            f.write(fila_tabla_1)
            f.write(fila_tabla_2)
            f.write('\\end{tabular}\n')
            f.write('\\end{table}\n')
            f.write('\n')
            f.write('Se trata de la ventana cuya casilla central superior es la celda de la fila '+ str(posicion_actual[0])+ ' y columna ' + str(posicion_actual[1])+'\\newline\n')
            f.write(mensaje_actual+'\\newline\n')



        #fin del documento:
        f.write('\\end{document}\n')

    f.close()



##################################################################
################### LATEX CON TODA LA INFO #######################
##################################################################

def generarLatexInfo(nombreDeMT, noDeterministic, stay, estadoInicial, blanco, estadosTot, estadosFinales, 
                    entrada, transitions, reglasEnOrden,tabla, n, 
                    valorTotal_phi_start,  valorTotal_phi_accept, valorTotal_phi_cell, valorTotal_phi_move, valorTotal_phi,
                    phi_start_latex, phi_accept_latex, phi_cell_latex,  phi_move_latex,
                    phi_start_valores_latex, phi_accept_valores_latex, phi_cell_valores_latex, phi_move_valores_latex ):
    
    
    outputFile = nombreDeMT+'_'+entrada+"_Informacion_total.tex"
    #outputFile = "tablon_alterado.tex"
    
    with codecs.open(outputFile, 'w', "utf-8-sig") as f:
        #Cosas que importar de manera genérica
        f.write('\\documentclass[a4paper,10pt]{article}\n')
        f.write('\\usepackage[utf8]{inputenc}\n')
        f.write('\\usepackage[spanish,es-tabla]{babel}\n')
        #márgenes del documento
        f.write('\\usepackage[top=3cm, bottom=2cm, right=1.5cm, left=3cm]{geometry}\n')
        f.write('\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\n')
        # Definimos el título
        name = ntpath.basename(nombreDeMT)
        f.write('\\title{$'+name+'$}\n')
        f.write('\\author{}\n')
        f.write('\\date{}\n\n')
        #comienzo del documento:
        f.write('\\begin{document}\n')
        f.write('\\maketitle\n\n')

        ####################  CARACTERISTICAS #####################
        f.write('\\section{Características de la MT}\n')
        f.write('En esta sección se analizará las características inherentes de la máquina de Turing introducida. \\newline\n')
        f.write('\\begin{itemize}\n')

        if(noDeterministic):
            f.write('\\item Tipo de MT =  MT no determinista (MTND). \n')
        else:
           f.write('\\item Tipo de MT =  MT determinista (MTD). \n')
        
        if(stay):
            f.write('\\item Es una MT con transiciones Stay. Esto quiere decir que a parte de las transiciones a la derecha o a la izquierda, esta MT puede quedarse inmovil.\n')
        else: 
            f.write('\\item Es una MT sin transiciones Stay. Esto quiere decir solo dispone de las transiciones a la derecha o a la izquierda. \n')

        f.write('\\item Estado Inicial =' + estadoInicial+'\n')
        f.write('\\item Símbolo blanco = ' + blanco + '\n')
        f.write('\\item La entrada/palabra que se ha introducido al ejecutar la MT es = \\emph' + entrada + ' \n')
        f.write('\\item Los estados totales son = \\{' + listToStr(estadosTot) +'\\} \n')
        f.write('\\item Los estados finales son = \\{' + listToStr(estadosFinales)+'\\} \n')

        f.write('\\end{itemize}\n\n')

        ####################  TABLON ###############################
        f.write('\\section{Tablón final y reglas aplicadas}\n')
        f.write('\\subsection{Sobre las transiciones o reglas}\n')
        f.write('En este apartado se mostrarán la función de transición total de la MT junto a las reglas de la función de transición de la MT aplicadas para la creación de la tabla, ordenadas por orden. El formato de cada refla es el siguiente: \\newline\\par \n')
        f.write('\\fbox{$\\delta$([\\textit{estado actual}],[\\textit{símbolo en el cabezal}]) = ([\\textit{nuevo estado}],[\\textit{nuevo símbolo}],[\\textit{dirección}])} \\newline\\par \n')
        f.write('La función de transición $\\delta$ está compuesta por las reglas siguientes.\\newline\\newline \n')
        
        f.write('\\begin{flushright}')
        f.write('$\\delta$ = \\{')
        for t in range(1,len(transitions),1):
            tran = transicionABonito(transitions[t])
            if(t< len(transitions)-1):
                f.write(tran + ', \\newline\n')
            else:
                f.write(tran + '\\}\\newline\n')
        f.write('\\end{flushright}')    

        f.write('\\par \nLas reglas que han sido utilizadas para la creación del tablón son las siguientes.\\newline\\newline \n')
        f.write('\\begin{flushright}')
        for t in reglasEnOrden:
            tran = transicionABonito(t)
            f.write(tran + '\\newline\n')
        f.write('\\end{flushright}')    

        f.write('\\subsection{Tablón final}\n')
        f.write('Una vez aplicadas las reglas expuestas en el apartado anterior, ahora se puede ver el tablón creado a partir de la palabra de entrada '+ entrada+'.\n')
        f.write('El tablón final en cuestión tiene un tamaño de '+str(n)+'*'+str(n)+'\\newline\\par\n')
        
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        eles = crear_eles_tabuladas(n)
        f.write('\\begin{tabular}{'+eles+'}\n')
        f.write('\\hline\n')
        
        esEstado = re.compile("q[0-9]*")
        esHastag = re.compile("#")
        fila_tabla = '\t'

        for i in range(0,n,1):
            for j in range (0,n,1):
                celda = tabla[i][j]
                match = re.fullmatch(esEstado, celda)
                match_hastag = re.fullmatch(esHastag, celda)
                if(j < n-1):
                    if(match):
                        cont=0
                        fila_tabla += '$'
                        for l in celda:
                            if(cont==0):
                                fila_tabla += l+'_'
                            else:
                                fila_tabla += l
                            cont +=1
                        fila_tabla += '$  &   '
                    elif(match_hastag):
                        fila_tabla += '\\#' +'  &   '
                    else:
                        fila_tabla += celda +'   &   '
                else:
                    if(match):
                        cont=0
                        fila_tabla += '$'
                        for l in celda:
                            if(cont==0):
                                fila_tabla += l+'_'
                            else:
                                fila_tabla += l
                            cont +=1 
                        fila_tabla += '$\t'
                    elif(match_hastag):
                        fila_tabla += '\\#' + '\t'
                    else:
                        fila_tabla += celda + '\t'

            f.write(fila_tabla + '\\\\ \\hline\n')
            fila_tabla = '\t'
  
        f.write('\\end{tabular}\n')
        f.write('\\end{table}\n')
        
        ####################  PHI START ############################
        f.write('\\section{$\\Phi$ Start}\n')
        f.write('El valor total de la fórmula $\\Phi$ Start es ')
        if(valorTotal_phi_start):
            f.write('\\emph{Verdadero}. Es decir, se cumple el que el estado inicial esté justo a la izquierda de la cadena indicando que el cabezal de lectura/escritura está apuntando al primer símbolo. \\newline \\newline \n')
        else:
            f.write('\\emph{Falso}. Es decir, no se cumple el que el estado inicial esté justo a la izquierda de la cadena indicando que el cabezal de lectura/escritura está apuntando al primer símbolo. \\newline \\newline \n')

        f.write('La fórmula $\\Phi$ Start generada con la palabra '+ entrada + 'es: \\newline \\newline \n')
        f.write(phi_start_latex + ' \\newline \\newline \n')
        f.write('La fórmula $\\Phi$ Start con los valores de verdad asignados es: \\newline \\newline \n')
        f.write(phi_start_valores_latex+' \\newline \\newline \n')

        ####################  PHI ACCEPT ############################
        f.write('\\section{$\\Phi$ Accept}\n')
        f.write('El valor total de la fórmula $\\Phi$ Accept es ')
        if(valorTotal_phi_accept):
            f.write('\\emph{Verdadero}. Es decir, se trata de un tablón de aceptación, ya que se encuentra un estado final o de aceptación en el tablón. \\newline \\newline \n')
        else:
            f.write('\\emph{Falso}. Es decir, la entrada no ha sido aceptada, no es un tablón de aceptación, no hay estado de aceptación en el tablón. \\newline \\newline \n')

        f.write('La fórmula $\\Phi$ Accept generada con la palabra '+ entrada + 'es: \\newline \\newline \n')
        f.write(phi_accept_latex + ' \\newline \\newline \n')
        f.write('La fórmula $\\Phi$ Accept con los valores de verdad asignados es: \\newline \\newline \n')
        f.write(phi_accept_valores_latex+' \\newline \\newline \n')

        ####################  PHI CELL ##############################
        f.write('\\section{$\\Phi$ Cell}\n')
        f.write('El valor total de la fórmula $\\Phi$ Cell es ')
        if(valorTotal_phi_cell):
            f.write('\\emph{Verdadero}. Es decir, En el tablón no hay celdas sin contenido o con símbolos no permitidos ni una celda contiene más de un mismo símbolo a la vez. \\newline \\newline \n')
        else:
            f.write('\\emph{Falso}. Es decir, En el tablón hay al menos una celda que no es un símbolo del conjunto C, o una celda no contiene ningún valor o una celda contiene más de uun símbolo. \\newline \\newline \n')

        f.write('La fórmula $\\Phi$ Cell generada con la palabra '+ entrada + 'es: \\newline \\newline \n')
        f.write( phi_cell_latex + ' \\newline \\newline \n')
        f.write('La fórmula $\\Phi$ Cell con los valores de verdad asignados es: \\newline \\newline \n')
        f.write(phi_cell_valores_latex+' \\newline \\newline \n')

        ####################  PHI MOVE ##############################
        f.write('\\section{$\\Phi$ Move}\n')
        f.write('El valor total de la fórmula $\\Phi$ Move es ')
        if(valorTotal_phi_move):
            f.write('\\emph{Verdadero}. Es decir, En el tablón todas las ventanas son legales. \\newline \\newline \n')
        else:
            f.write('\\emph{Falso}. Es decir, En el tablón hay al menos una ventana ilegal. \\newline \\newline \n')

        f.write('La fórmula $\\Phi$ Move generada con la palabra '+ entrada + 'es: \\newline \\newline \n')
        f.write(phi_move_latex + ' \\newline \\newline \n')
        f.write('La fórmula $\\Phi$ Move con los valores de verdad asignados es: \\newline \\newline \n')
        f.write(phi_move_valores_latex+' \\newline \\newline \n')

        ####################  PHI MOVE ##############################
        f.write('\\section{Fórmula $\\Phi$ final}\n')
        f.write('El valor total de la fórmula $\\Phi$ es ')
        if(valorTotal_phi):
            f.write('\\emph{Verdadero}. Es decir, Todas las subfórmulas ($\\Phi$ Start, Accept, Cell y Move) tienen valor verdadero.\n')
            f.write('Se trata de un tablón correcto y de aceptación. \\newline \\newline \n')
        else:
            f.write('\\emph{Falso}. Es decir, Alguna/s (o todas) las subfórmulas ($\\Phi$ Start, Accept, Cell y Move) tienen valor Falso. \\newline \\newline \n')

        f.write('La fórmula $\\Phi$ generada con la palabra '+ entrada + 'es: \\newline \\newline \n')
        f.write('[\t'+phi_start_latex + '\t]\\newline \\newline \n')
        f.write('AND \\newline \\newline \n')
        f.write('[\t'+phi_accept_latex + '\t]\\newline \\newline \n')
        f.write('AND \\newline \\newline \n')
        f.write('[\t'+phi_cell_latex + '\t]\\newline \\newline \n')
        f.write('AND \\newline \\newline \n')
        f.write('[\t'+phi_move_latex + '\t]\\newline \\newline \n')

        #fin del documento:
        f.write('\\end{document}\n')
    
    f.close()
