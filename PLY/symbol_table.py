from DirClass import dirClass

class symbolTable:
    
    def __init__(self, dirClass: dirClass):
        self.symbol = {}
        self.dirV = [None] * 10000
        self.dirClass = dirClass
    


    #idSplit recibe un lista de variables y su tipo, la funcion toma el tipo de las variables y su id y 
    # lo mete a la estructura correspondiente
    def idSplit(self, vars, gtype):
        dtype = ''
        for index in range(len(vars)):
            if index%2 == 0:
                dtype = vars[index]
            else:
                for var in vars[index]:
                    val = self.addVar(var[0], var[1], dtype, gtype)
                    if val < 0:
                        return val


    #addVar recibe id de variable, dimensiones en caso de ser arreglo, tipo de dato, y tipo
    #addVar mete los datos de entrada a la tabla de simbolos y en caso de ser arreglo le agrega informacion como dimensiones
    def addVar(self, id, dim, dtype, gtype):
        if id in self.symbol:
            if gtype == 'cte':
                return
            exit(f'Error: Multiple declarations of variable {id}')
        
        self.symbol[id] = {}
        self.symbol[id]['dim'] = []
        size = 1
        if dtype != 'bool' and dtype != 'int' and dtype != 'char' and dtype != 'float':
            self.symbol[id]['class'] = dtype
            dtype = 'id'
            if len(dim) > 0:
                exit('Error: Unsupported constructor array')
            if gtype != 'global':
                exit('Error: Class found outside of main')
            if self.symbol[id]['class'] not in self.dirClass.dir:
                exit(f'Error: No class definition fount at {id}')
            size = self.dirClass.dir[self.symbol[id]['class']]['size']
        else:
            if dim:
                size = dim[0]
                self.symbol[id]['dim'].append(dim[0])
                if len(dim) == 2:
                    size *= dim[1]
                    self.symbol[id]['dim'].append(dim[1])

        dirv = self.dirVGet(gtype)

        if dirv == -1:
            exit("Error: Out of memory")
        
        for d in range(size):
            if self.dirV[dirv + d]:
                exit('Error: Memory full')
            if dtype == 'char':
                self.dirV[dirv + d] = ''
            elif dtype == 'bool':
                self.dirV[dirv + d] = False
            else:
                self.dirV[dirv + d] = 0

        
        self.symbol[id]['type'] = dtype
        self.symbol[id]['dirV'] = dirv

        return dirv
    
    #checkVar recibe un id de una variable y revisa en la tabla de simbolos si ya existe para comprobar que no 
    #haya multiples declaraciones de una misma variable
    def checkVar(self, id):
        if id not in self.symbol:
            exit(f'Error: Undeclared variable found at {id}')
        return 1
    
    #assignVal recibe el valor de una variable y el id, y lo asigna a memoria
    def assignVal(self, val, id):
       if self.checkVar(id) > 0:
            if self.getValType(val) == self.symbol[id]['type'] or (self.symbol[id]['type'] == 'float' and self.getValType(val) == 'int'):
                self.dirV[self.symbol[id]['dirV']] = val                
            else:
                exit(f"Error: Type mismatch assignation at {val}")
    #getValType recibe un valor y regresa su tipo de dato
    def getValType(self, val):
        if type(val) is int:
            return "int"
        elif type(val) is float:
            if val.is_integer():
                return "int"
            return "float"
        elif type(val) is bool:
            return "bool"

    #getIdVal recibe el id de una variable y regresa su direccion virtual
    def getIdVal(self, id):
        if id not in self.symbol:
            exit(f'Error: Undeclared variable at {id}')
        return self.dirV[self.symbol[id]['dirV']]

    #getIdDirv recibe el id de una variable y regresa su direccion virtual
    def getIdDirV(self, id):
        if id not in self.symbol:
            exit(f'Error: Undeclared variable at {id}')
        return self.symbol[id]['dirV']

    #getIdType recibe el id de una variable y regresa el tipo de esa variable
    def getIdType(self, id):
        if id not in self.symbol:
            exit(f'Error: Undeclared variable at {id}')
        if id in self.symbol:
            return self.symbol[id]['type']
        else:
            return -1
        
    #getIdDim recibe el id de una variable y regresa las dimensiones de esa variable    
    def getIdDim(self, id):
        if id not in self.symbol:
            exit(f'Error: Undeclared variable at {id}')
        if id in self.symbol:
            return self.symbol[id]['dim']
        else:
            return -1  

    #dirVGet recibe el tipo de una variable y regresa la siguiente direccion virtual disponible
    def dirVGet(self, gtype):
        min = 0
        max = 0
        if gtype == 'global':
            min = 0
            max = 2000
        elif gtype == 'local':
            min = 2000
            max = 4000
        elif gtype == 'temporal':
            min = 4000
            max = 6000
        elif gtype == 'cte':
            min = 6000
            max = 8000
        elif gtype == 'tp':
            min = 8000
            max = 10000
        
        for x in range(min, max):
            if self.dirV[x] == None:
                return x

        exit('Error: no more memory')

    def __str__(self):
        return f'Symbol Table is {self.symbol}'
