import sys
import ast
symbolTable = {}
cuadruplos = []
countSym = 0
dirFun = {}
dirV = [None] * 10000
pSaltos = []
progName = ''
ip = 0

funName = ['main']

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
    if len(funName) > 0:
        if len(dirFun[funName[-1]]['dirV']) == 0: #we are inside of a function with no memory
            exit(f'Function {funName[-1]} didn\'t get initialized')
        for vars in dirFun[funName[-1]]['vars']: #check vars in the function
            if vars['id'] == id:
                return vars['dirV'] + dirFun[funName[-1]]['dirV'][-1]
        for temp in dirFun[funName[-1]]['temp']: #
            if temp['id'] == id:
                return temp['dirV'] + dirFun[funName[-1]]['dirV'][-1]
    
    if id in symbolTable:
        return symbolTable[id]['dirV']
    else:
        exit(f'Value {id} was not declared')



def execCuad(cuad):
    if cuad['accion'] == 'goto':
        print("S")
        ip -= 1
    elif cuad['accion'] == 'gotoF':
        print("S")
        ip -= 1
    elif cuad['accion'] == '+':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] + dirV[getDirV(cuad['val2'])]
        print("S")
    elif cuad['accion'] == '-':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] - dirV[getDirV(cuad['val2'])]
        print("S")
        #{'accion': '-', 'val1': 'count', 'val2': 1, 'final': 't4'}
    elif cuad['accion'] == '*':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] * dirV[getDirV(cuad['val2'])]
        print("Multiplicacion")
    elif cuad['accion'] == '/':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] / dirV[getDirV(cuad['val2'])]
        print("Division")
    elif cuad['accion'] == '<':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] < dirV[getDirV(cuad['val2'])]
        print("Menor que")
    elif cuad['accion'] == '>':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] > dirV[getDirV(cuad['val2'])]
        print("Mayor que")
    elif cuad['accion'] == '=':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])]
        print("Asigna")
    elif cuad['accion'] == '==':
        dirV[getDirV(cuad['final'])] = dirV[getDirV(cuad['val1'])] == dirV[getDirV(cuad['val2'])]
        print("Compara")
    elif cuad['accion'] == 'outco':
        print(dirV[getDirV(cuad['val1'])])
        print("Imprimido")
    elif cuad['accion'] == 'inco':
        dirV[getDirV(cuad['val1'])] = input()
        print("S")
    elif cuad['accion'] == 'ver':
        print("S")
    elif cuad['accion'] == 'ERA':
        print("S")
    elif cuad['accion'] == 'return':
        print("S")
        ip -= 1
    elif cuad['accion'] == 'param':
        print("S")
    elif cuad['accion'] == 'Gosub':
        print("S")
        ip -= 1
    ip += 1


def saveSymbolTable(data):
    id = data[0:data.find(":")-1]
    if id in symbolTable:
        exit(f'Multiples declaraciones de {id}')
       
    start = data.find(":") + 2
    sub = data[start:] 
    res = ast.literal_eval(sub)
    
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
            print('Symbol Table', symbolTable)
            print('\nDirFun', dirFun)
            print('\nCuadruplos', cuadruplos)
            f.close()

            while ip >= 0:
                execCuad(cuadruplos[ip])
        except EOFError:
            print(EOFError)
    else:
        print("No hay archivo")