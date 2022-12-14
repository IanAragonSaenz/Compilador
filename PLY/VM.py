import sys
import ast
import re

symbolTable = {}
cuadruplos = []
countSym = 0
dirFun = {}
dirClasses = {}
dirV = [None] * 10000
pSaltos = []
progName = ''
ip = 0
funName = ['main']
funParamName = []
classNameParams = ''
className = ''
varClassName = ''
tempMin = 4000
cteMin = 6000
tpMin = 8000
tCount = tempMin


# Lee el archivo "ovejota" linea por linea y guarda seccion por seccion la informacion de memoria.
# Recibe una variable con todo lo que contiene el archivo "ovejota"
# Regresa nada
def output(data):
    part = -1
    for line in data:
        if part == -1:
            if line and line.find('.txt') and line[0:5] == '@@@@@':
                progName = line[5:line.find('.txt')]
                part = -2
            else:
                exit(f'File {data[0]} is not an executable file')
        elif line == '@@@@@_SymbolTable\n':
            part = 0
        elif line == '@@@@@_DirFun\n':
            part = 1
        elif line == '@@@@@_Cuadruplos\n':
            part = 2
        elif line == '@@@@@_DirClasses\n':
            part = 3
        elif part == 0:
            saveSymbolTable(line)
        elif part == 1:
            saveDirFun(line)
        elif part == 2:
            saveCuads(line)
        elif part == 3:
            saveMethodClass(line)


# Busca la direccion virtual de una variable dentro de directorio de classes, de funciones y de variables (asi como tambien cehcando en caso de que sea una variable tp)
# Recibe un id de la variable a buscar y un booleano para un caso especifico con variables tp.
# Regresa la direccion virtual
def getDirV(id, left = False):
    if type(id) != str:
        id = str(id)

    if className != '':
        for var in dirClasses[className]['pubVars']:
            if var['id'] == id:
                for v in dirFun['main']['vars']:
                    if v['id'] == varClassName:
                        return var['dirV'] + v['dirV']
                
        for var in dirClasses[className]['prVars']:
            if var['id'] == id:
                for v in dirFun['main']['vars']:
                    if v['id'] == varClassName:
                        return var['dirV'] + v['dirV']

        if funName[-1] in dirClasses[className]['pubFun']:
            for var in dirClasses[className]['pubFun'][funName[-1]]['vars']:
                if var['id'] == id:
                    return var['dirV'] + dirClasses[className]['pubFun'][funName[-1]]['dirV'][-1]
            for var in dirClasses[className]['pubFun'][funName[-1]]['temp']:
                if var['id'] == id:
                    if var['gtype'] == 'tp':   
                        if left:
                            return var['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]
                        else:
                            return dirV[temp['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]]  + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]
                    return var['dirV'] + dirClasses[className]['pubFun'][funName[-1]]['dirV'][-1]

        if funName[-1] in dirClasses[className]['prFun']:
            for var in dirClasses[className]['prFun'][funName[-1]]['vars']:
                if var['id'] == id:
                    return var['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]
            for var in dirClasses[className]['prFun'][funName[-1]]['temp']:
                if var['id'] == id:
                    if var['gtype'] == 'tp':
                        if left:
                            return var['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]
                        else:
                            return dirV[temp['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]]  + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]     
                    return var['dirV'] + dirClasses[className]['prFun'][funName[-1]]['dirV'][-1]

    elif len(funName) > 0:
        if len(dirFun[funName[-1]]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Error: Function {funName[-1]} has no declaration')
        for vars in dirFun[funName[-1]]['vars']: #check vars in the function
            if vars['id'] == id:
                return int(vars['dirV'] + dirFun[funName[-1]]['dirV'][-1])
        for temp in dirFun[funName[-1]]['temp']: #
            if temp['id'] == id:
                if temp['gtype'] == 'tp':      
                    if left:
                        return temp['dirV'] + dirFun[funName[-1]]['dirV'][-1]
                    else:
                        return dirV[temp['dirV'] + dirFun[funName[-1]]['dirV'][-1]]  + dirFun[funName[-1]]['dirV'][-1]                                              
                return int(temp['dirV'] + dirFun[funName[-1]]['dirV'][-1])
    
    if id in symbolTable:
        return int(symbolTable[id]['dirV'])
    else:
        exit(f'Error: Variable {id} was not declared on {funName[-1]}')


# Regresa el tipo de una variable.
# Recibe un id de la variable.
# Regresa el tipo de la variable.
def getType(id):
    if type(id) != str:
        id = str(id)

    if className != '':
        for var in dirClasses[className]['pubVars']:
            if var['id'] == id:
                return var['type']
        for var in dirClasses[className]['prVars']:
            if var['id'] == id:
                return var['type']

        if funName[-1] in dirClasses[className]['pubFun']:
            for var in dirClasses[className]['pubFun'][funName[-1]]['vars']:
                if var['id'] == id:
                    return var['type']
            for var in dirClasses[className]['pubFun'][funName[-1]]['temp']:
                if var['id'] == id:
                    return var['type']

        if funName[-1] in dirClasses[className]['prFun']:
            for var in dirClasses[className]['prFun'][funName[-1]]['vars']:
                if var['id'] == id:
                    return var['type']
            for var in dirClasses[className]['prFun'][funName[-1]]['temp']:
                if var['id'] == id:
                    return var['type']

    elif len(funName) > 0:
        if len(dirFun[funName[-1]]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Function {funName[-1]} didn\'t get initialized')
        for vars in dirFun[funName[-1]]['vars']: #check vars in the function
            if vars['id'] == id:
                return vars['type']
        for temp in dirFun[funName[-1]]['temp']: #
            if temp['id'] == id:                                                     #check for TP
                return temp['type']
    
    if id in symbolTable:
        return symbolTable[id]['type']
    else:
        exit(f'Error: Variable {id} was not declared on {funName[-1]}')

# Consigue la direccion virtual de un parametro en una funcion.
# Recibe un id de la funcion y el parametro que es.
# Regresa la direccion virtual del parametro.
def getDirVParam(id, par):
    if len(funParamName) > 0:
        if len(dirFun[id]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Function {id} didn\'t get initialized')
        param = dirFun[id]['param'] #get 
        paramSize = len(param)
        if par > paramSize:
             exit(f'Error: Function {id} doesnt have {par} parameters, but has {paramSize} parameters')
        return dirFun[id]['vars'][par-1]['dirV'] + dirFun[id]['dirV'][-1]
    else:
        exit(f'Function {id} has no declaration')

# Ejecuta un cuadruplo, con su accion hasta llegar a la accion de END donde termina
# Recibe el cuadruplo a leer
# Regresa nada
def execCuad(cuad):
    global ip, dirV, classNameParams, className, varClassName
    if cuad['accion'] == 'goto':
        ip = dirV[getDirV(cuad['final'])]
        ip -= 1
        
    elif cuad['accion'] == 'gotoF':
        if not dirV[getDirV(cuad['val1'])]:
            ip = dirV[getDirV(cuad['final'])]
            ip -=1
    elif cuad['accion'] == 'gotoV':
        if dirV[getDirV(cuad['val1'])]:
            ip = dirV[getDirV(cuad['final'])]
            ip -=1
    elif cuad['accion'] == '+':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] + dirV[getDirV(cuad['val2'])]

        new = dirV[getDirV(cuad['final'], True)]
    elif cuad['accion'] == '-':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] - dirV[getDirV(cuad['val2'])]
    elif cuad['accion'] == '*':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] * dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '/':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] / dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '<':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] < dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '>':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] > dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '=':
        rigth = cuad['val1']
        left = cuad['final']
        valRigth = dirV[getDirV(rigth)]
        if getType(left) == 'int' and getType(rigth) == 'float' and not valRigth.is_integer():
            exit(f'Error: Assigining an int variable:{left} a float value')

        dirV[getDirV(left)] = valRigth

    elif cuad['accion'] == '==':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] == dirV[getDirV(cuad['val2'])]

    elif cuad['accion'] == '<>':
        dirV[getDirV(cuad['final'], True)] = dirV[getDirV(cuad['val1'])] != dirV[getDirV(cuad['val2'])]
    elif cuad['accion'] == '||':
        left = dirV[getDirV(cuad['val1'])]
        rigth = dirV[getDirV(cuad['val2'])]
        if type(left) != bool  or type(rigth) != bool:
            exit('Error: OR found at non boolean expression')
        dirV[getDirV(cuad['final'], True)] = left or rigth

    elif cuad['accion'] == '&&':
        left = dirV[getDirV(cuad['val1'])]
        rigth = dirV[getDirV(cuad['val2'])]
        if type(left) != bool  or type(rigth) != bool:
            exit('Error: AND found at non boolean expression')
        dirV[getDirV(cuad['final'], True)] = left and rigth
        
    elif cuad['accion'] == 'outco':
        print(dirV[getDirV(cuad['val1'])])
    elif cuad['accion'] == 'inco':
        rigth = input()
        left = cuad['val1']
        dtype = ''

        if rigth.replace('.','',1).replace('-','',1).isdigit():
            if rigth.replace('-','',1).isdigit():
                rigth = int(rigth)
                dtype = 'int'
            else:
                rigth = float(rigth)
                dtype = 'int'
                if rigth.is_integer():
                    rigth = int(rigth)
                    dtype = 'int'
        elif len(rigth) == 3 and rigth[0] == '"' and rigth[2] == '"':
            dtype = 'char'
        elif rigth == 'True':
            rigth = True
            dtype = 'bool'
        elif rigth == 'False':
            rigth = False
            dtype = 'bool'

        if getType(left) != dtype:
            exit(f'Error: giving wrong type to {left} with {rigth}: {dtype}')

        dirV[getDirV(left)] = rigth
    elif cuad['accion'] == 'ver':
        if(dirV[getDirV(cuad['val1'])]) < dirV[getDirV(cuad['val2'])] or (dirV[getDirV(cuad['val1'])]) > dirV[getDirV(cuad['final'])]:
            exit("Error: Index out of range")
    elif cuad['accion'] == 'ERA':
        createRecord(cuad['final'])
    elif cuad['accion'] == 'return':
        createReturn(cuad['final'])
        ip -= 1
    elif cuad['accion'] == 'param':
        if len(funParamName) < 1:
            exit('Sending param to no function')
        par = int(cuad['final'][3:])
        rigth = dirV[getDirV(cuad['val1'])]
        
        if className != '':
            V = -1
            ftype = ''
            if funParamName[-1] in dirClasses[className]['pubFun']:
                if len(dirClasses[className]['pubFun'][funParamName[-1]]['dirVTemp']) > 0:
                    V = dirClasses[className]['pubFun'][funParamName[-1]]['dirVTemp'].pop()
                    dirClasses[className]['pubFun'][funParamName[-1]]['dirV'].append(V)
                    ftype = 'pubFun'
            
            if funParamName[-1] in dirClasses[className]['prFun']:
                if len(dirClasses[className]['prFun'][funParamName[-1]]['dirVTemp']) > 0:
                    V = dirClasses[className]['prFun'][funParamName[-1]]['dirVTemp'].pop()
                    dirClasses[className]['prFun'][funParamName[-1]]['dirV'].append(V)
                    ftype = 'prFun'

            dirV[V+par-1] = rigth

            if V != -1:
                dirClasses[className][ftype][funParamName[-1]]['dirVTemp'].append(V)
                dirClasses[className][ftype][funParamName[-1]]['dirV'].pop()
        else:
            V = -1
            if len(dirFun[funParamName[-1]]['dirVTemp']) > 0:
                V = dirFun[funParamName[-1]]['dirVTemp'].pop()
                dirFun[funParamName[-1]]['dirV'].append(V)

            dirV[getDirVParam(funParamName[-1], par)] = rigth

            if V != -1:
                dirFun[funParamName[-1]]['dirV'].pop()
                dirFun[funParamName[-1]]['dirVTemp'].append(V)
    elif cuad['accion'] == 'Gosub':
        V = -1
        if className != '':
            ftype = ''
            if funParamName[-1] in dirClasses[className]['pubFun']:
                if len(dirClasses[className]['pubFun'][funParamName[-1]]['dirVTemp']) > 0:
                    V = dirClasses[className]['pubFun'][funParamName[-1]]['dirVTemp'].pop()
                    dirClasses[className]['pubFun'][funParamName[-1]]['dirV'].append(V)
                    ftype = 'pubFun'
            
            if funParamName[-1] in dirClasses[className]['prFun']:
                if len(dirClasses[className]['prFun'][funParamName[-1]]['dirVTemp']) > 0:
                    V = dirClasses[className]['prFun'][funParamName[-1]]['dirVTemp'].pop()
                    dirClasses[className]['prFun'][funParamName[-1]]['dirV'].append(V)
                    ftype = 'prFun'
        else:
            if len(dirFun[cuad['final']]['dirVTemp']) > 0:
                V = dirFun[cuad['final']]['dirVTemp'].pop()
                dirFun[cuad['final']]['dirV'].append(V)

        funName.append(cuad['final'])
        funParamName.pop()
        pSaltos.append(ip+1)
        if className != '':
            ip = dirClasses[className][ftype][funName[-1]]['dirI']
        else:
            ip = dirFun[cuad['final']]['dirI']
        ip -= 1
    elif cuad['accion'] == 'EndProc':
        EndProc()
        ip -= 1
    elif cuad['accion'] == 'ERAP':
        createRecordMethod(cuad['val1'], cuad['final'])
    elif cuad['accion'] == 'GosubP':
        
        className = classNameParams
        varClassName = cuad['val1']
        classNameParams = ''
        funName.append(cuad['final'])
        pSaltos.append(ip+1)
        ip = dirClasses[className]['pubFun'][cuad['final']]['dirI']

        ip -= 1
    elif cuad['accion'] == 'paramP':
        createParamP(cuad['val1'], cuad['val2'], cuad['final'])
    elif cuad['accion'] == 'END':
        ip = -10
    ip += 1


# Guarda un valor en cierto parametro de una funcion dentro de una clase
# Recibe el valor a guardar, la funcion y el parametro a llenar.
# Regresa nada
def createParamP(val, f, param):
    if classNameParams == '':
        exit('Sending param to no function')
    par = int(param[3:])
    rigth = dirV[getDirV(val)]
    
    V = -1
    if len(dirClasses[classNameParams]['pubFun'][f]['dirV']) > 0:
        V = dirClasses[classNameParams]['pubFun'][f]['dirV'][-1]
    else:
        exit('Error: no memory for function in class')

    dirV[V + par-1] = rigth


# Ejecuta el return de una funcion y guarda el valor a regresar dentro de la varaible global para la funcion
# Recibe el valor a regresar
# Regresa nada
def createReturn(final):
    global className, varClassName
    if len(funName) < 2:
        exit('Return found outside of a function')
    
    dtype = ''
    if className != '':
        if len(funName) == 2:
            dtype = dirClasses[className]['pubFun'][funName[-1]]['type']
            if dtype != 'void':
                dirV[getDirV(funName[-1])] = dirV[getDirV(final)]
        else:
            if funName[-1] in dirClasses[className]['pubFun']:
                dtype = dirClasses[className]['pubFun'][funName[-1]]['type']
            
            if funName[-1] in dirClasses[className]['prFun']:
                dtype = dirClasses[className]['prFun'][funName[-1]]['type']
            if dtype != 'void':
                dirV[getDirV(funName[-1])] = dirV[getDirV(final)]

    else:
        dtype = dirFun[funName[-1]]['type']
        if dtype != 'void':
            dirV[getDirV(funName[-1])] = dirV[getDirV(final)]
    
    if dtype != 'void' and dtype != getType(final):
        exit(f'Error: Return value is not the same type as function')
    EndProc()
    

# Reserva la memoria que necesitara una funcion y se la asigna
# Recibe el id de la funcion
# Regresa nada
def createRecord(id):
    global tCount, className, funParamName
    if className != '':
        if id in dirClasses[className]['pubFun']:
            size = dirClasses[className]['pubFun'][id]['size']
            funParamName.append(id)
            dirClasses[className]['pubFun'][id]['dirVTemp'].append(tCount)

        elif id in dirClasses[className]['prFun']:
            size = dirClasses[className]['prFun'][id]['size']
            funParamName.append(id)
            dirClasses[className]['prFun'][id]['dirVTemp'].append(tCount)
        else:
            exit('Error: Function is not in this class')
    else:
        size = dirFun[id]['size']
        if id != 'main':
            funParamName.append(id)
            dirFun[id]['dirVTemp'].append(tCount)
        else:
            dirFun[id]['dirV'].append(tCount) 
    tCount += size
    if tCount >= cteMin:
        exit(f'Error: temporal memory full')


# Reserva la memoria para una funcion de una clase y le asigna su direccion virtual
# Recibe la variable (la que es de tipo clase) y el id de la funcion
# Regresa nada
def createRecordMethod(var, funID):
    global tCount, classNameParams


    for v in dirFun['main']['vars']:
        if v['id'] == var:
            dtype = v['type']

    classNameParams = dtype

    if funID in dirClasses[dtype]['pubFun']:
        dirClasses[dtype]['pubFun'][funID]['dirV'].append(tCount) 
    else:
        exit('Error: Fun is not un public from class')
    size = dirClasses[dtype]['pubFun'][funID]['size']
    tCount += size
    
    if tCount >= cteMin:
        exit('Error: temporal memory full')


# Termina con la ejecucion de una fucnion y nos regresa al ultimo salto que se hizo, se borra/limpia la memoria de la funcion.
# Recibe nada
# Regresa nada
def EndProc():
    global tCount, ip, pSaltos, className, varClassName, funName
    id = funName.pop()

    if className != '':

        if len(funName) == 1:
            size = dirClasses[className]['pubFun'][id]['size']
            dirClasses[className]['pubFun'][id]['dirV'].pop()
            className = ''
            varClassName = ''
        else:
            if id in dirClasses[className]['pubFun']:
                size = dirClasses[className]['pubFun'][id]['size']
                dirClasses[className]['pubFun'][id]['dirV'].pop()
            
            if id in dirClasses[className]['prFun']:
                size = dirClasses[className]['prFun'][id]['size']
                dirClasses[className]['prFun'][id]['dirV'].pop()
    else:
        size = dirFun[id]['size']
        dirFun[id]['dirV'].pop()

    fin = tCount
    tCount -= size
    ip = pSaltos.pop()

    for i in range(tCount, fin):
        dirV[i] = None
    if tCount < tempMin:
        exit(f'Error: temporal memory count was not right')


# Guarda un valor en la tabla de simbolos de lo leido del archivo
# Recibe un string con un valor de la tabla de simbolos
# Regresa nada
def saveSymbolTable(data):
    id = data[0:data.find(":")-1]
    if id in symbolTable:
        exit(f'Error: Multiple declaration found at {id}')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    if res['dirV'] >= cteMin and res['dirV'] < tpMin:
        if id.replace('.','',1).replace('-','',1).isdigit():
            if id.replace('-','',1).isdigit():
                dirV[res['dirV']] = int(id)
            else:
                dirV[res['dirV']] = float(id)
                
        else:
            dirV[res['dirV']] = id
    symbolTable[id] = res
    

# Guarda un valor en el directorio de funciones, de lo leido del archivo
# Recibe un string con un valor del directorio de funciones
# Regresa nada
def saveDirFun(data):
    id = data[0:data.find(":")-1]
    if id in dirFun:
        exit(f'Error: Multiple declaration found at {id}')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
    dirFun[id] = res 
    dirFun[id]['dirV'] = []
    dirFun[id]['dirVTemp'] = []


# Guarda un valor en la lista de cuadruplos de lo leido del archivo
# Recibe un string con un valor de cuadruplos
# Regresa nada
def saveCuads(data):
    i = data[0:data.find(":")-1]
    i = int(i)
    if len(cuadruplos) > i:
        exit('repeating cuadruplos')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
    cuadruplos.append(res)

# Guarda un valor en el directorio de clases de lo leido del archivo
# Recibe un string con un valor de el directorio de clases
# Regresa nada
def saveMethodClass(data):
    i = data[0:data.find(":")-1]
    if i in dirClasses:
        exit('Error: Saving same class twice')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
    dirClasses[i] = res



if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            output(f)
            f.close()
            createRecord('main')
            
            while ip >= 0:
                execCuad(cuadruplos[ip])
        except EOFError:
            print(EOFError)
    else:
        print("No hay archivo")