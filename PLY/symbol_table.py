class symbolTable:
    
    def __init__(self):
        self.symbol = {}
        self.dirV = [None] * 1000
    

    def idSplit(self, vars, gtype):
        dtype = ''
        for index in range(len(vars)):
            if index%2 == 0:
                dtype = vars[index]
            else:
                for var in vars[index]:
                    val = self.addVar(var[0], dtype, gtype)
                    if val < 0:
                        return val
        return 1


    
    def addVar(self, id, dtype, gtype):
        if id in self.symbol:
            # "error variable is already declared"
            return -1
        
        dirv = self.dirVGet(gtype)

        if dirv == -1:
            # "error no more memory for variable"
            return -2


        if dtype == 'char':
            self.dirV[dirv] = ''
        else:
            self.dirV[dirv] = 0

        self.symbol[id] = {}
        self.symbol[id]['type'] = dtype
        self.symbol[id]['dirV'] = dirv

        return dirv
    
    
    def checkVar(self, id):
        if id not in self.symbol:
            # "error variable no declarada"
            return -1
        return 1
    
    def assignVal(self, val, id):
       if self.checkVar(id) > 0:
            if self.getValType(val) == self.symbol[id]['type'] or (self.symbol[id]['type'] == 'float' and self.getValType(val) == 'int'):
                self.dirV[self.symbol[id]['dirV']] = val                
            else:
                print("Error type mismatch", val)
        
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
        

    def getIdVal(self, id):
        return self.dirV[self.symbol[id]['dirV']]

    def getIdType(self, id):
        return self.symbol[id]['type']

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
        
        for x in range(min, max):
            if self.dirV[x] == None:
                return x

        return 0

    def __str__(self):
        return f'Symbol Table is {self.symbol}'
