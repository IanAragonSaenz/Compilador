from DirFun import dirFun


class dirClass:
    def __init__(self):
        self.dir = {}


    def saveClass(self, id, inherit, prVars, prFun, pubVars, pubFun, dirI):
        if id in self.dir:
            exit('Error: Class has already been declared')
        if inherit and inherit not in self.dir:
            exit('Error: Class being inherited does not exist')
        
        self.dir[id] = {}
        self.dir[id]['size'] = 0
        self.dir[id]['dirI'] = dirI
        self.dir[id]['dirV'] = 0

        if inherit:
            self.dir[id]['inherit'] = inherit
        else:
            self.dir[id]['inherit'] = ''

        self.dir[id]['prFun'] = dirFun()
        self.dir[id]['pubFun'] = dirFun()

        self.dir[id]['prVars'] = []
        self.addVars(id, prVars, 'prVars')

        self.dir[id]['pubVars'] = []
        self.addVars(id, pubVars, 'pubVars')
        
        

    def closeClass(self, id):
        size = 0
        for f in self.dir[id]['prFun'].fun:
            size += self.dir[id]['prFun'].fun[f]['size']
        for f in self.dir[id]['pubFun'].fun:
            size += self.dir[id]['pubFun'].fun[f]['size']
        self.dir[id]['size'] += size

        self.dir[id]['prFun'] = self.dir[id]['prFun'].fun
        self.dir[id]['pubFun'] = self.dir[id]['pubFun'].fun

        self.dir[id]['dirV'] = {}


    def addVars(self, id, vars, typeP):
        size = 0
        dtype = ''
        if vars:
            for index in range(len(vars)):
                if index%2 == 0:
                    dtype = vars[index]
                else:
                    for temp in vars[index]:
                        var = {
                            "id":temp[0],
                            "type":dtype,
                            "dirV":self.dir[id]['dirV'],
                            "dim":[]
                        }
                        count = 1
                        if temp[1]:
                            for i in temp[1]:
                                count = i * count
                                var['dim'].append(i)
                            size = size + count
                        else:
                            size = size + 1
                        self.dir[id]['dirV'] += count
                        self.dir[id][typeP].append(var)
        self.dir[id]['size'] = size + self.dir[id]['size']

    def findFunType(self, classID, funID):
        if classID not in self.dir:
            exit('Error: Class was not declared')
        if funID in self.dir[classID]['prFun'].fun:
            return self.dir[classID]['prFun'].getFunType(funID)
        elif funID in self.dir[classID]['pubFun'].fun:
            return self.dir[classID]['pubFun'].getFunType(funID)
        elif self.dir[classID]['inherit'] != '':
            inheritID = self.dir[classID]['inherit']

            if funID in self.dir[inheritID]['prFun'].fun:
                return self.dir[inheritID]['prFun'].getFunType(funID)
            elif funID in self.dir[inheritID]['pubFun'].fun:
                return self.dir[inheritID]['pubFun'].getFunType(funID)
        
        exit(f'Error: Function {funID} does not exist in class {classID}')


    def getClassFunParam(self, className, funName):
        if className not in self.dir:
            exit('Error: Class was not declared')
        
        if funName in self.dir[className]['prFun'].fun:
            return self.dir[className]['prFun'].getFunParams(funName)
        elif funName in self.dir[className]['pubFun'].fun:
            return self.dir[className]['pubFun'].getFunParams(funName)
        else:
            exit(f'Error: Function {funName} does not exist')

    def getVarType(self, className, funName, id):
        for var in self.dir[className]['prVars'] + self.dir[className]['pubVars']:
            if var['id'] == id:
                return var['type']
        
        prFuns = self.dir[className]['prFun'].getIdType(funName, id)
        pubFuns = self.dir[className]['pubFun'].getIdType(funName, id)

        if prFuns != -1:
            return prFuns
        if pubFuns != -1:
            return pubFuns

        return -1

    def addTemp(self, className, funName, id, dtype, tp=False):
        if className not in self.dir:
            exit('Error: Class was not declared')
        
        if funName in self.dir[className]['prFun'].fun:
            self.dir[className]['prFun'].addTempVar(funName, id, dtype, tp)
        elif funName in self.dir[className]['pubFun'].fun:
            self.dir[className]['pubFun'].addTempVar(funName, id, dtype, tp)
        else:
            exit(f'Error: Function {funName} does not exist')
        