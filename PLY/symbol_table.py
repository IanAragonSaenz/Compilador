class symbolTable:
    
    def __init__(self):
        self.symbol = {}
        self.dirV = [None] * 1000
    

    #['float', [['prepucio', None]]]
    #['int', [['yes', [10]]]]
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


    
    def addVar(self, id, dim, dtype, gtype):
        if id in self.symbol:
            exit("error variable is already declared")
        
        self.symbol[id] = {}
        self.symbol[id]['dim'] = []
        size = 1
        if dim:
            size = dim[0]
            self.symbol[id]['dim'].append(dim[0])
            if len(dim) == 2:
                size *= dim[1]
                self.symbol[id]['dim'].append(dim[1])

        dirv = self.dirVGet(gtype)

        if dirv == -1:
            exit("error no more memory for variable")
        
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

        #print(self.symbol)
        return dirv
    
    
    def checkVar(self, id):
        if id not in self.symbol:
            exit(f'Error: ID {id} doesnt exist')
        return 1
    
    def assignVal(self, val, id):
       if self.checkVar(id) > 0:
            if self.getValType(val) == self.symbol[id]['type'] or (self.symbol[id]['type'] == 'float' and self.getValType(val) == 'int'):
                self.dirV[self.symbol[id]['dirV']] = val                
            else:
                exit(f"Error: type mismatch {val}")
        
    def getValType(self, val):
        if type(val) is int:
            return "int"
        elif type(val) is float:
            if val.is_integer():
                return "int"
            return "float"
        elif type(val) is bool:
            return "bool"
    
 #   def changeIdType(self, id):
        
    def getRealID(self, id):
        #if type(id) == list:
        #    id = id[0]
        #    if type(id) == list:
        #        id = id[0]
        return id

    def getIdVal(self, id):
        id = self.getRealID(id)
        if id not in self.symbol:
            exit(f'Error: ID {id} doesnt exist, value')
        return self.dirV[self.symbol[id]['dirV']]

    def getIdDirV(self, id):
        id = self.getRealID(id)
        if id not in self.symbol:
            exit(f'Error: ID {id} doesnt exist, dirV')
        return self.symbol[id]['dirV']

    def getIdType(self, id):
        id = self.getRealID(id)
        if id not in self.symbol:
            exit(f'Error: ID {id} doesnt exist, Type')
        if id in self.symbol:
            return self.symbol[id]['type']
        else:
            return -1
        
    def getIdDim(self, id):
        id = self.getRealID(id)
        if id not in self.symbol:
            exit(f'Error: ID {id} doesnt exist, Dim')
        if id in self.symbol:
            return self.symbol[id]['dim']
        else:
            return -1  

    def dirVGet(self, gtype):
        min = 0
        max = 0
        if gtype == 'global':
            min = 0
            max = 250
        elif gtype == 'local':
            min = 250
            max = 500
        elif gtype == 'temporal':
            min = 500
            max = 750
        elif gtype == 'cte':
            min = 750
            max = 1000
        elif gtype == 'tp':
            min = 1000
            max = 1250
        
        for x in range(min, max):
            if self.dirV[x] == None:
                return x

        exit('Error: no more memory')

    def __str__(self):
        return f'Symbol Table is {self.symbol}'
