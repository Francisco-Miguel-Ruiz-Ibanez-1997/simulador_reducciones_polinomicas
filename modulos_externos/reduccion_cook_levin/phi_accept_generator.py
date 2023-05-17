
####################################################################################################
####################################     PHI_ACCEPT   ##############################################
####################################################################################################

def loContiene(estadosFinales, celda):
    for q in estadosFinales:
        if(q == celda):
            return True
    return False

def crearLiteralesFinales(estadosFinales, n):
    literalesFinales = []
    literalesFinales_latex=[]
    for i in range(1,n-1,1):
        for j in range(1,n-1,1):
            for q in estadosFinales:
                numero = q[1]
                literal_latex = '$X_'+str(i)+',_'+str(j)+'\\_q_'+numero+'$'
                literal = 'X'+str(i)+'_'+str(j)+'_'+q
                literalesFinales.append(literal)
                literalesFinales_latex.append(literal_latex)
    return literalesFinales, literalesFinales_latex

def generarPhiAccept(tabla, estadosFinales, n):
    #asegura que qaccept aparezca
    #en alguna celda. (QUE HAYA ESTADO FINAL EN ALGUNA CELDA, LA QUE SEA)
    literalesFinales, literalesFinales_latex = crearLiteralesFinales(estadosFinales, n) 
    tam = len(literalesFinales)
    loCumple = False
    phi_accept_latex = ''
    phi_accept_valores_latex = ''
    phi_Accept=""
    phi_Accept_valores=""

    for i in range(0,tam,1):
        if(i< tam-1):
            phi_accept_latex += literalesFinales_latex[i]+'\\ $\\vee$\\ '
            phi_Accept += literalesFinales[i] + ' OR '
        else:
            phi_accept_latex += literalesFinales_latex[i]
            phi_Accept += literalesFinales[i]
    
    for i in range(0,n,1):
        for j in range(0,n,1):
            celda = tabla[i][j]
            if((j == i) and (j == n-1)):
                if(loContiene(estadosFinales, celda)):
                    phi_accept_valores_latex += 'True\\ '
                    phi_Accept_valores += 'True '
                    loCumple = True
                else:
                    phi_accept_valores_latex += 'False\\ '
                    phi_Accept_valores += 'False '
            else:
                if(loContiene(estadosFinales, celda)):
                    phi_accept_valores_latex += 'True\\ $\\vee$\\ '
                    phi_Accept_valores += 'True OR '
                    loCumple = True
                else:
                    phi_accept_valores_latex += 'False\\ $\\vee$\\ '
                    phi_Accept_valores += 'False OR '

    return phi_Accept, phi_Accept_valores, loCumple, phi_accept_latex, phi_accept_valores_latex

