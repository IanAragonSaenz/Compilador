class dirFun:

    def __init__(self):
        self.fun = {}

    #addFun recibe una lista con los elementos de una funcion, y direccion virtual, la funcion agrega
    # los datos de entrada y los introduce al directorio de funciones 
    def addFun(self, fun, dirI, dirClasses = None):
        if fun[1] in self.fun:
            exit("Error: Function is already declared")

        size = 0 
        self.fun[fun[1]] = {}
        self.fun[fun[1]]['type'] = fun[0]
        self.fun[fun[1]]['dirI'] = dirI
        self.fun[fun[1]]['dirV'] = 0

        self.fun[fun[1]]['param'] = []
        self.fun[fun[1]]['vars'] = []
        self.fun[fun[1]]['temp'] = []

        if fun[2]:
            for param in fun[2]:
                self.fun[fun[1]]['param'].append(param[0])
                var = {
                    "id":param[1],
                    "type":param[0],
                    "dirV":self.fun[fun[1]]['dirV'],
                    "dim":[]
                }
                self.fun[fun[1]]['vars'].append(var)
                size = size + 1
                self.fun[fun[1]]['dirV'] += 1

        dtype = ''
        if fun[3]:
            for index in range(len(fun[3])):
                if index%2 == 0:
                    dtype = fun[3][index]
                else:
                    for temp in fun[3][index]:
                        var = {
                            "id":temp[0],
                            "type":dtype,
                            "dirV":self.fun[fun[1]]['dirV'],
                            "dim":[]
                        }
                        count = 1
                        size = 0
                        if dtype != 'bool' and dtype != 'int' and dtype != 'char' and dtype != 'float':
                            var['class'] = dtype
                            dtype = 'id'
                            if temp[1]:
                                exit(f'Error: no arrays with classes {temp[0]}')
                            if fun[1] != 'main':
                                exit('Error: Class init outside of main')
                            if dirClasses and var['class'] not in dirClasses.dir:
                                exit(f'Error: Class doesnt exist with {id}')
                            count = dirClasses.dir[var['class']]['size']
                        else: 
                            
                            if temp[1]:
                                for i in temp[1]:
                                    count = i * count
                                    var['dim'].append(i)
                                size = size + count
                            else:
                                size = size + 1
                        self.fun[fun[1]]['dirV'] += count
                        self.fun[fun[1]]['vars'].append(var)
        self.fun[fun[1]]['size'] = size
    #addTemp recibe un nombre de funcion, y los recursos que usa, la funcion rellena el atributo size dentro del directorio 
    # de funciones usando el nombre de funcion en la entrada        
    def addTemp(self, funName, size):
        self.fun[funName]['size'] = size + self.fun[funName]['size']
        
    #addTempVar recibe un nombre de funcion, un temporal, y tipo, la funcion agrega variables temporales al
    #directorio de funciones bajo el nombre de funcion en la entrada
    def addTempVar(self, funName, temp, dtype, tp=False):
        var = {
            "id":temp,
            "type":dtype,
            "dirV":self.fun[funName]['dirV'],
            "dim":[],
            "gtype":''
        }
        if tp:
            var['gtype'] = 'tp'
        self.fun[funName]['dirV'] += 1
        self.fun[funName]['temp'].append(var)
        self.fun[funName]['size'] = self.fun[funName]['size'] + 1

    #getFunDirI recibe el nombre de una funcion y busca la funcion en el directorio y regresa su direccion virtual
    def getFunDirI(self, funName):
        if funName in self.fun:
            return self.fun[funName]['DirI']
        else:
            exit(f'function {funName} doesn\'t exist, DirI')
    #getFunParams recibe el nombre de una funcion, busca el nombre en el directorio y regresa los parametros
    def getFunParams(self, funName):
        if funName in self.fun:
            return self.fun[funName]['param']
        else:
            exit(f'function {funName} doesn\'t exist, get function params')
    #getFunType recibe el nombre de una funcion, busca el nombre en el directorio y regresa el tipo de la funcion
    def getFunType(self, funName):
        if funName in self.fun:
            return self.fun[funName]['type']
        else:
            exit(f'function {funName} doesn\'t exist, get function type')
    #getIdType recibe el nombre de una funcion y el nombre de una variable, busca el nombre en el directorio
    #busca la variable bajo esa funcion y regresa el tipo
    def getIdType(self, funName, varName): 
        if funName in self.fun:
            for var in self.fun[funName]['vars']:
                if var['id'] == varName:
                    return var['type']
            for var in self.fun[funName]['temp']:
                if var['id'] == varName:
                    return var['type'] 
            return -1
        return -1    

    #getIDDimrecibe el nombre de una funcion y el nombre de una variable, busca el nombre en el directorio
    #busca la variable bajo esa funcion y regresa las dimensiones de esa variable
    def getIdDim(self, funName, varName): 
        if funName in self.fun:
            for var in self.fun[funName]['vars']:
                if var['id'] == varName:
                    return var['dim']
            for var in self.fun[funName]['temp']:
                if var['id'] == varName:
                    return var['dim'] 
            return -1
        return -1   
    #getVarDirV recibe el nombre de una funcion y el nombre de una variable, busca el nombre en el directorio
    #busca la variable bajo esa funcion y regresa las la direccion virtual de esa variable
    def getVarDirV(self, funName, varName): 
        if funName in self.fun:
            for var in self.fun[funName]['vars']:
                if var['id'] == varName:
                    return var['dirV']
            return -1
        return -1        
    #funExists recibe el nombre de una funcion y regresa si existe o no en el directorio de funciones
    def funExists(self, funName):
        if funName in self.fun:
            return True
        else:
            return False
    #closeFun recible el nombre de una funcion y limpia los valores de direccion virtual y direcciones temporales virtuales
    def closeFun(self, funName):
        self.fun[funName]['dirV'] = []
        self.fun[funName]['dirVTemp'] = []
    
    def printSelf(self):
        #for fun in self.fun:
        print("FUN DIR", self.fun)
        
        
        