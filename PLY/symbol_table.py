class symbolTable:

    def __init__(self):
        self.symbol = {}
        self.dirV = [None] * 1000
    

    def addVar(self, id, dtype, type):
        if id in self.symbol:
            return "error variable is already declared"
        
        dirv = self.dirVGet(type)

        if dirv == -1:
            return "error no more memory for variable"

        if dtype == 'char':
            self.dirV[dirv] = ''
        else:
            self.dirV[dirv] = 0

        self.symbol[id] = {
            'type': dtype,
            'dirV': dirv
        }

    def dirVGet(self, type):
        min = 0
        max = 0
        if type == 'global':
            min = 0
            max = 250
        elif self.type == 'local':
            min = 250
            max = 500
        elif type == 'temporal':
            min = 500
            max = 750
        elif type == 'cte':
            min = 750
            max = 1000
        
        for x in range(min, max):
            if self.dirV[x] == None:
                return x

        return -1

    def __str__(self):
        return f'Symbol Table is {self.symbol}'
