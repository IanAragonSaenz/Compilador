import sys
import ast
import re

symbolTable = {}
cuadruplos = []
countSym = 0
dirFun = {}
dirV = [None] * 10000
pSaltos = []
progName = ''
ip = 0
funName = ['main']
funParamName = []
tempMin = 4000
cteMin = 6000
tpMin = 8000
tCount = tempMin


def output(data):
    part = -1
    for line in data:
        if part == -1:
            if line and line.find('.txt') and line[0:5] == '@@@@@':
                progName = line[5:line.find('.txt')]
                part = -2
            else:
                exit('File is not object')
        elif line == '@@@@@_SymbolTable\n':
            part = 0
        elif line == '@@@@@_DirFun\n':
            part = 1
        elif line == '@@@@@_Cuadruplos\n':
            part = 2
        elif part == 0:
            saveSymbolTable(line)
        elif part == 1:
            saveDirFun(line)
        elif part == 2:
            saveCuads(line)

def getDirV(id):
    if type(id) != str:
        id = str(id)
    if len(funName) > 0:
        if len(dirFun[funName[-1]]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Function {funName[-1]} didn\'t get initialized')
        for vars in dirFun[funName[-1]]['vars']: #check vars in the function
            if vars['id'] == id:
                return int(vars['dirV'] + dirFun[funName[-1]]['dirV'][-1])
        for temp in dirFun[funName[-1]]['temp']: #
            if temp['id'] == id:                                                     #check for TP
                return int(temp['dirV'] + dirFun[funName[-1]]['dirV'][-1])
    
    if id in symbolTable:
        return int(symbolTable[id]['dirV'])
    else:
        exit(f'Value {id} was not declared on {funName[-1]}')

def getDirVParam(id, par):
    if len(funName) > 0:
        if len(dirFun[funName[-1]]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Function {funName[-1]} didn\'t get initialized')
        param = dirFun[funName[-1]]['param'] #get 
        paramSize = len(param)
        if par > paramSize:
             exit(f'Function {id} doesnt have {par} params')
        
        return dirFun[funName[-1]]['vars'][par-1] + dirFun[funName[-1]]['dirV'][-1]
    else:
        exit(f'Function {id} wasnt initialized')

def execCuad(cuad):
    global ip
    if cuad['accion'] == 'goto':
        print("Goto")
        ip = dirV[getDirV(cuad['final'])]
        ip -= 1
        
    elif cuad['accion'] == 'gotoF':
        if not dirV[getDirV(cuad['val1'])]:
            print("GotoFalso")
            ip = dirV[getDirV(cuad['final'])]
            ip -=1
    elif cuad['accion'] == '+':
        print("Suma")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] + dirV[getDirV(cuad['val2'])]
    elif cuad['accion'] == '-':
        print("Resta", type(dirV[getDirV(cuad['val1'])]), dirV[getDirV(cuad['val1'])], type(dirV[getDirV(cuad['val2'])]), dirV[getDirV(cuad['val2'])])
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] - dirV[getDirV(cuad['val2'])]
        #{'accion': '-', 'val1': 'num', 'val2': 2, 'final': 't1'}
    elif cuad['accion'] == '*':
        print("Multiplicacion")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] * dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '/':
        print("Division")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] / dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '<':
        print("Menor que")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] < dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '>':
        print("Mayor que")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] > dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == '=':
        print("Asigna")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])]
        
    elif cuad['accion'] == '==':
        print("Compara")
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] == dirV[getDirV(cuad['val2'])]
        
    elif cuad['accion'] == 'outco':
        print(dirV[getDirV(cuad['val1'])])
        print("Imprimido")
    elif cuad['accion'] == 'inco':
        dirV[getDirV(cuad['val1'])] = input()
        print("Input")
    elif cuad['accion'] == 'ver':
        if(dirV[getDirV(cuad['val1'])]) < dirV[getDirV(cuad['val2'])] or (dirV[getDirV(cuad['val1'])]) > dirV[getDirV(cuad['final'])]:
            exit("Indice fuera de rango")
        print('Verficacion')
    elif cuad['accion'] == 'ERA':
        createRecord(cuad['final'])
        funParamName.append(cuad['final'])
        print("ERA")
    elif cuad['accion'] == 'return':
        createReturn(cuad['final'])
        print("Return")
        ip -= 1
    elif cuad['accion'] == 'param':
        #{'accion': 'param', 'val1': 3, 'val2': '', 'final': 'par1'}
        if len(funParamName) < 1:
            exit('Sending param to no function')
        par = cuad['final'][3:]
        dirV[getDirVParam(funParamName[-1], par)] = dirV[getDirV(cuad['val1'])]
        print("S")
    elif cuad['accion'] == 'Gosub':
        #{'accion': 'Gosub', 'val1': '', 'val2': '', 'final': 'fib'}
        funName.append(cuad['final'])
        funParamName.pop()
        pSaltos.append(ip+1)
        ip = dirFun[cuad['final']]['dirI']
        print("S")
        ip -= 1
    elif cuad['accion'] == 'EndProc':
        EndProc()
        print("S")
        ip -= 1
    elif cuad['accion'] == 'END':
        print("END")
        ip = -10
    ip += 1

def createReturn(final):
    if len(funName) < 2:
        exit('Return found outside of a function')
    dtype = dirFun[funName[-1]]['type']
    if dtype != 'void':
        dirV[getDirV(funName[-1])] = dirV[getDirV(final)]
    EndProc()
    

def createRecord(id):
    global tCount
    size = dirFun[id]['size']
    dirFun[id]['dirV'].append(tCount)
    tCount += size
    if tCount >= 6000:
        exit('Error: temporal memory full')

def EndProc():
    global tCount
    funName.pop()
    size = dirFun[id]['size']
    dirFun[id]['dirV'].pop()
    tCount -= size
    ip = pSaltos.pop()
    if tCount < 4000:
        exit('Error: temporal memory count was not right')



def saveSymbolTable(data):
    id = data[0:data.find(":")-1]
    if id in symbolTable:
        exit(f'Multiples declaraciones de {id}')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    if res['dirV'] >= cteMin and res['dirV'] < tpMin:
        if id.replace('.','',1).replace('-','',1).isdigit():
            if id.replace('-','',1).isdigit():
                print('int  ', id)
                dirV[res['dirV']] = int(id)
            else:
                print('float  ', id)
                dirV[res['dirV']] = float(id)
                
        else:
            dirV[res['dirV']] = id
    symbolTable[id] = res
    
    
def saveDirFun(data):
    id = data[0:data.find(":")-1]
    if id in dirFun:
        exit(f'Multiples declaraciones de funcion {id}')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
    dirFun[id] = res 
    dirFun[id]['dirV'] = []
        
def saveCuads(data):
    i = data[0:data.find(":")-1]
    i = int(i)
    if len(cuadruplos) > i:
        exit('repeating cuadruplos')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
    cuadruplos.append(res)




if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            output(f)
            print('\n\nSymbol Table', symbolTable)
            print('\nDirFun', dirFun)
            print('\nCuadruplos', cuadruplos)
            
            f.close()
            createRecord('main')
            
            print('\nDirFun', dirFun)
            while ip >= 0:
                execCuad(cuadruplos[ip])
        except EOFError:
            print(EOFError)
    else:
        print("No hay archivo")