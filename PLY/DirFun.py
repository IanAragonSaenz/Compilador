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

    def addFun(self, fun):
        if fun[1] in self.fun:
            # "error variable is already declared"
            return -1

        size = 0

        self.fun[fun[1]] = {}
        self.fun[fun[1]]['type'] = fun[0]
        #self.fun[fun[1]]['dirI'] = 2

        self.fun[fun[1]]['param'] = []
        self.fun[fun[1]]['vars'] = {}
        for param in fun[2]:
            self.fun[fun[1]]['param'].append(param[0])
            print('paraaaaaaaam', param)
            var = {
                "id":param[1],
                "type":param[0],
                "dirV":"",
                "dim":[]
            }
            self.fun[fun[1]]['vars'].append(var)
            size = size + 1
        
        for vars in fun[3]:
            dtype = ''
            for index in range(len(vars)):
                if index%2 == 0:
                    dtype = vars[index]
                else:
                    for var in vars[index]: 
                        var = {
                            "id":var[0],
                            "type":dtype,
                            "dirV":"",
                            "dim":[]
                        }
                        if var[1]:
                            count = 1
                            for i in var[1]:
                                count = i * count
                                var['dim'].append(i)
                            size = size + count
                        else:
                            size = size + 1
                        self.fun[fun[1]]['vars'].append(var)

        self.fun[fun[1]]['size'] = size
        print(self.fun)
            



        
        
        