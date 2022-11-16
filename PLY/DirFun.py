class dirFun:

    def __init__(self):
        self.fun = {#"fib":{
            #"type":"int",
            #"dirI":"2",
            #"dirV":"12001"
            #"size":"",
            #"param":['int','int']
            #}
            #"vars":[
            #   {
            #    "id":"count",
            #    "type":"int",
            #    "dirV":"1000"
            #    "dim":""
            #   }
            # ]
        }
       #function ['int', 'fib', 
       #[['int', 'param1'], ['int', 'param2']], 
       #['float', [['prepucio', None]]], 
       #[['condition', [3], [['assign', 'param1', ['param2']]], None]], 
       #[3]]

    def addFun(self, fun, dirI):
        if fun[1] in self.fun:
            # "error variable is already declared"
            return -1

        size = 0 

        self.fun[fun[1]] = {}
        self.fun[fun[1]]['type'] = fun[0]
        self.fun[fun[1]]['dirI'] = dirI

        self.fun[fun[1]]['param'] = []
        self.fun[fun[1]]['vars'] = []
        self.fun[fun[1]]['temp'] = []

        for param in fun[2]:
            self.fun[fun[1]]['param'].append(param[0])
            var = {
                "id":param[1],
                "type":param[0],
                "dirV":"",
                "dim":[]
            }
            self.fun[fun[1]]['vars'].append(var)
            size = size + 1

        #['float', [['prepucio', None]]]
        dtype = ''
        for index in range(len(fun[3])):
            if index%2 == 0:
                dtype = fun[3][index]
            else:
                for temp in fun[3][index]:
                    var = {
                        "id":temp[0],
                        "type":dtype,
                        "dirV":"",
                        "dim":[]
                    }
                    if temp[1]:
                        count = 1
                        for i in temp[1]:
                            count = i * count
                            var['dim'].append(i)
                        size = size + count
                    else:
                        size = size + 1
                    self.fun[fun[1]]['vars'].append(var)

        self.fun[fun[1]]['size'] = size
            
    def addTemp(self, funName, size):
        self.fun[funName]['size'] = size + self.fun[funName]['size']
    
    def addTempVar(self, funName, temp, dtype):
        var = {
            "id":temp,
            "type":dtype,
            "dirV":"",
            "dim":[]
        }
        self.fun[funName]['temp'].append(var)

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

    def printSelf(self):
        #for fun in self.fun:
        print("FUN DIR", self.fun)
        
        
        