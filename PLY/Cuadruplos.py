from symbol_table import symbolTable
from DirFun import dirFun
from SCube import sCube
from DirClass import dirClass

class cuadruplos:
    def __init__(self, table: symbolTable, dirFuns: dirFun, dirClass: dirClass):
        self.cube = sCube()
        self.dirClasses = dirClass
        self.vp = []
        self.pOper = []
        self.pSalto = []
        self.pTipos = []
        self.operators = ["+", "-", "*", "/", "<", ">", "==", "<>", "(", ")", "&&", "||"]
        self.plusMinus = ["+", "-"]
        self.multDiv = ["*", "/"]
        self.comparison = ["<", ">", "==", "<>"]
        self.andOr = ["&&", "||"]
        self.t = 1
        self.tp = 1
        self.count = 0
        self.cuad = []
        self.table = table
        self.dirFuns = dirFuns
        self.funName = ''
        self.className = ''
        self.returns = 0
        #{'accion' : '*', 'val1' : '1', 'val2' : 'count', 'final' : 't3'}
        
    #function ['int', 'fib', 
    #[['int', 'param1'], ['int', 'param2']], 
    #['float', [['prepucio', None]]], 
    #[['condition', [3], [['assign', 'param1', ['param2']]], None]], 
    #[3]]

    def saveClassCuads(self, c):
        id = c[0]
        inherit = c[1]
        prVars = c[2]
        prFun = c[3]
        pubVars = c[4]
        pubFun = c[5]
        self.className = id

        self.dirClasses.saveClass(id, inherit, prVars, prFun, pubVars, pubFun, self.count)
        if prFun:
            for f in prFun:
                self.saveClassFunCuads(id, 'prFun', f)
        if pubFun:
            for f in pubFun:
                self.saveClassFunCuads(id, 'pubFun', f)
        self.dirClasses.closeClass(id)
        self.className = ''

    def saveClassFunCuads(self, id, typeP, fun):
        self.funName = fun[1]
        self.returns = 0

        self.dirClasses.dir[id][typeP].addFun(fun, self.count)
        if fun[4]:
            for block in fun[4]:
                self.blockHandle(block)

        if fun[0] != 'void' and self.returns == 0:
            exit(f'Error: function type {fun[0]} has no returns, function name: {fun[1]}')

        cuadruplo =  {'accion': 'EndProc', 'val1': '', 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.table.addVar(fun[1], [], fun[0], 'global')

        self.dirClasses.dir[id][typeP].closeFun(self.funName)
        self.funName = ''
        self.clearTemp()
        self.returns = 0

    def goToMain(self):
        cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.pSalto.append(0)
    
    def fillGoToMain(self):
        goto = self.pSalto.pop()
        self.cuad[goto]['final'] = self.count
        self.table.addVar(self.count, [], 'int', 'cte')

    def saveCuads(self, progName):
        f = open(f"{progName}.txt", "w")
        f.write(f"@@@@@{progName}.txt\r")
        f.close()

        f = open(f"{progName}.txt", "a")
        f.write('@@@@@_SymbolTable\n')
        for element in self.table.symbol:
            f.write(f'{element} : {self.table.symbol[element]}\n')

        f.write('@@@@@_DirFun\n')
        for element in self.dirFuns.fun:
            f.write(f'{element} : {self.dirFuns.fun[element]}\n')
        
        f.write('@@@@@_Cuadruplos\n')
        for i in range(len(self.cuad)):
            f.write(f'{i} : {self.cuad[i]}\n')

        f.write('@@@@@_DirClasses\n')
        for i in self.dirClasses.dir:
            f.write(f'{i} : {self.dirClasses.dir[i]}\n')
        f.close()


    def saveFunCuads(self, fun):
        self.funName = fun[1]
        self.returns = 0
        self.dirFuns.addFun(fun, self.count, self.dirClasses)
        if fun[4]:
            for block in fun[4]:
                self.blockHandle(block)

        if fun[0] != 'void' and self.returns == 0:
            exit(f'Error: function type {fun[0]} has no returns, function name: {fun[1]}')

        if fun[1] == 'main':
            cuadruplo =  {'accion': 'END', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
        else:
            cuadruplo =  {'accion': 'EndProc', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
            if fun[0] != 'void':
                self.table.addVar(fun[1], [], fun[0], 'global')
        self.dirFuns.closeFun(self.funName)
        self.funName = ''
        self.clearTemp()
        self.returns = 0

    def saveReturnCuads(self, code):
        if self.funName == '':
            exit('Error: return used outside of a function')

        if self.className != '':
            funType = self.dirClasses.findFunType(self.className, self.funName)
        else:
            funType = self.dirFuns.getFunType(self.funName)
        if funType != 'void' and not code[1]:
            exit(f'Error: Function type {funType} has no return function name: {self.funName[-1]}')
        elif funType == 'void' and code[1]:
            exit(f'Error: Function type void has return, function name: {self.funName[-1]}')
        elif funType != 'void' and code[1]:
            ret = self.saveExpCuads(code[1])
            cuadruplo =  {'accion': 'return', 'val1': '', 'val2': '', 'final': ret}
            self.addCuad(cuadruplo)
        else:
            cuadruplo =  {'accion': 'return', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
        
        self.returns += 1
    
    def saveArrayCuads(self, code):
        address = -1
        if self.className != '':
            address = self.dirClasses.findFunType(self.className, self.funName, code[1])
        elif self.funName != '':
            address = self.dirFuns.getVarDirV(self.funName, code[1])
            self.table.addVar(address, [], 'int', 'cte')
        if address == -1:
            address = self.table.getIdDirV(code[1])


        dimMin = 0
        dimMax = self.getArrayDim(code[1])
        if len(dimMax) != len(code[2]) and len(dimMax) != 0:
            exit(f'Error: Missing index at array {code[1]}')

        dtype = self.getType(code[1])
        exp = code[2][0]
        if type(exp) != list:
            exp = [exp] 
        val = self.saveExpCuads(exp)
        cuadruplo = {'accion': 'ver', 'val1': val, 'val2': dimMin, 'final': dimMax[0]}
        self.addCuad(cuadruplo)

        if len(dimMax) == 2:
            cuadruplo = {'accion': '*', 'val1': val, 'val2': dimMax[1], 'final': 't{}'.format(self.t)}
            self.addCuad(cuadruplo)
            if self.funName == '':
                self.table.addVar('t{}'.format(self.t), [], dtype, 'temporal')
            else:
                self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), dtype)
            t = self.t
            self.t += 1

            
            exp = code[2][1]
            if type(exp) != list:
                exp = [exp] 
            val = self.saveExpCuads(exp)
            cuadruplo = {'accion': 'ver', 'val1': val, 'val2': dimMin, 'final': dimMax[1]}
            self.addCuad(cuadruplo)
            cuadruplo = {'accion': '+', 'val1': val, 'val2': 't{}'.format(t), 'final': 't{}'.format(self.t)}
            self.addCuad(cuadruplo)
            if self.funName == '':
                self.table.addVar('t{}'.format(self.t), [], dtype, 'temporal')
            else:
                self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), dtype)
            self.t += 1

            cuadruplo = {'accion': '+', 'val1': 't{}'.format(self.t-1), 'val2': address, 'final': 'tp{}'.format(self.tp)}
        else:
            cuadruplo = {'accion': '+', 'val1': val, 'val2': address, 'final': 'tp{}'.format(self.tp)}
        
        self.addCuad(cuadruplo)
        if self.funName == '':
            self.table.addVar('tp{}'.format(self.tp), [], dtype, 'tp')
        else:
            self.dirFuns.addTempVar(self.funName, 'tp{}'.format(self.tp), dtype, True)
        self.tp += 1
        return 'tp{}'.format(self.tp-1)

    def saveCallCuads(self, call):
        # ['call', 'fib', [[3, '+', 1], ['op', '+', 2]]]
        cuadruplo =  {'accion': 'ERA', 'val1': '', 'val2': '', 'final': call[1]}
        self.addCuad(cuadruplo)

        if self.className != '':
            params = self.dirClasses.getClassFunParam(self.className, self.funName)
        else:
            params = self.dirFuns.getFunParams(call[1])
        

        if len(params) != len(call[2]):
            exit(f'Error: Parameters mismatch at {call[1]} function call')
        
        p = 1
        for param in call[2]:
            val = self.saveExpCuads(param)
            
            dtype = self.checkType(val)

            if dtype != params[p-1]:
                exit(f'Error: Parameter type mismatch at {param} in function {call[1]} call')

            cuadruplo =  {'accion': 'param', 'val1': val, 'val2': '', 'final': f'par{p}'}
            self.addCuad(cuadruplo)
            p += 1

        cuadruplo =  {'accion': 'Gosub', 'val1': '', 'val2': '', 'final': call[1]}
        self.addCuad(cuadruplo)
        if self.className != '':
            funType = self.dirClasses.findFunType(self.className, call[1])
        else:
            funType = self.dirFuns.getFunType(call[1])
        
        if funType != 'void':
            if self.className != '':
                self.dirClasses.addTemp(self.className, self.funName, 't{}'.format(self.t), funType)
            elif self.funName == '':
                self.table.addVar('t{}'.format(self.t), funType, 'temporal')
            else:
                self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), funType)
            
            cuadruplo =  {'accion': '=', 'val1': call[1], 'val2': '', 'final': 't{}'.format(self.t)}
            self.addCuad(cuadruplo)
            self.t = self.t + 1
            return 't{}'.format(self.t-1)
        return False

    def saveExpCuads(self, exp):
        self.readEXP(exp)
        val = self.expCuads()
        self.clearCache()
        return val

    
    def saveOutcoCuads(self, code):
        for x in code[1]:
            if type(x) is str:
                if x[0] == '"':
                    self.table.addVar(x, [], 'char', 'cte')
                    val = x
                else:
                    val = self.saveExpCuads([x])
            else:
                val= self.saveExpCuads(x)
            cuadruplo =  {'accion': 'outco', 'val1': val, 'val2': '', 'final': ''} 
            self.addCuad(cuadruplo)

           
        
    def saveIncoCuads(self, code):
        val = code[1]
        if type(code[1]) == list and code[1][0] == 'array':
            val = self.saveArrayCuads(code[1])
        cuadruplo =  {'accion': 'inco', 'val1': val, 'val2': '', 'final': ''} 
        self.addCuad(cuadruplo)

        
    def getType(self, index):
        if self.className != '':
            fun = self.dirClasses.getVarType(self.className, self.funName, index)
            if fun == -1:
                dtype = self.table.getIdType(index)
                if dtype == -1:
                    exit('Error: Undeclared variable at {}'.format(index))
                else:
                    return dtype
            else:
                return fun
        elif self.funName != '':
            fun = self.dirFuns.getIdType(self.funName, index)
            if fun == -1:
                dtype = self.table.getIdType(index)
                if dtype == -1:
                    exit('Error: Undeclared variable at {}'.format(index))
                else:
                    return dtype
            else:
                return fun
        else:
            dtype = self.table.getIdType(index)
            if dtype == -1:
                exit('Error: Undeclared variable at {}'.format(index))
            else:
                return dtype

    def getArrayDim(self, index):
        if self.className != '':
            return self.dirClasses.getVarDim(self.className, self.funName, index)
        elif len(self.funName) > 0:
            fun = self.dirFuns.getIdDim(self.funName, index)
            if fun == -1:
                dtype = self.table.getIdDim(index)
                if dtype == -1:
                    exit('Error: Undeclared variable at {}'.format(index))
                else:
                    return dtype
            else:
                return fun
        else:
            dtype = self.table.getIdDim(index)
            if dtype == -1:
                exit('Error: Undeclared variable at {}'.format(index))
            else:
                return dtype

        return -1

    def checkType(self, val):
        if type(val) is str and val[0] == '"' and len(val) == 3:
            dtype = 'char'
        elif type(val) is str:
            dtype = self.getType(val)
        else:
            dtype = self.table.getValType(val)
        return dtype

    def saveAssignCuads(self, code):
        if type(code[1]) == list and code[1][0] == 'array':
            tp = self.saveArrayCuads(code[1])
            left = self.getType(code[1][1])
            code[1] = tp
        else:
            left = self.getType(code[1])

        val = self.saveExpCuads(code[2])
        if type(val) == list:
            if type(code[1]) != list and self.getArrayDim(code[1]) != []:
                dim = self.getArrayDim(code[1])
                if len(dim) == 2 and dim[0] == dim[1]:
                    if dim[0]*dim[1] == len(val):
                        n = 0
                        for i in range(dim[0]):
                            for j in range(dim[1]):
                                self.saveAssignCuads(['assign', ['array', code[1], [i, j]], [val[n]]])
                                n += 1
                        
                        return 

                    else:
                        exit('Error: Assigning an array of different size')
                else:
                    exit('Error: Trying to use array in an expr without accessing with an index')
            else:
                exit('Error: Assigning matrix to a single value')
        right = self.getType(val)
        

        typeCheck = self.cube.typeCheck(left, right, '=')
        if typeCheck == 'x':
            exit(f'Error: Type mismatch assignation at {code[1]}')
        #elif typeCheck != left and left == 'int' and typeCheck == 'float':


        cuadruplo =  {'accion': '=', 'val1': val, 'val2': '', 'final': code[1]}
        self.addCuad(cuadruplo)
        
    def saveConditionCuads(self, code):
        val = self.saveExpCuads(code[1])
        cuadruplo =  {'accion': 'gotoF', 'val1': val, 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.pSalto.append(self.count-1)
        
        for block in code[2]:
            self.blockHandle(block)

        # check for else
        if code[3]:
            falso = self.pSalto.pop()
            cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
            self.pSalto.append(self.count-1)
            self.cuad[falso]['final'] = self.count
            self.table.addVar(self.count, [], 'int', 'cte')
            for block in code[3]:
                self.blockHandle(block)

        salto = self.pSalto.pop()
        self.cuad[salto]['final'] = self.count
        self.table.addVar(self.count, [], 'int', 'cte')
        
    def saveWhileCuads(self, code):
        self.pSalto.append(self.count) #Revaluar 3
        val = self.saveExpCuads(code[1])
        cuadruplo =  {'accion': 'gotoF', 'val1': val, 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.pSalto.append(self.count-1) #guardar donde va el gotoF, para ponerle a donde saltar
        
        for block in code[2]:
            self.blockHandle(block)
        
        falso = self.pSalto.pop()
        retorno = self.pSalto.pop()
        cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': retorno}
        self.addCuad(cuadruplo)
        self.cuad[falso]['final'] = self.count
        self.table.addVar(self.count, [], 'int', 'cte')
        self.table.addVar(retorno, [], 'int', 'cte')

    def saveMethodCuads(self, code):
        #'''dec_method : ID DOT ID LEFTPAREN dec_exp_method RIGHTPAREN SEMICOLON'''
        #p[0] = ['method', p[1], p[3], p[5]]
        if self.funName != 'main':
            exit('Error: Class declaration unsupported at main')
        dtype = self.dirFuns.getIdType(self.funName, code[1])
        if dtype not in self.dirClasses.dir and self.dirClasses.dir[dtype]['pubFun'][code[2]]:
            exit(f'Error: No class declaration found for variable {code[1]}')
        
        cuadruplo =  {'accion': 'ERAP', 'val1': code[1], 'val2': '', 'final': code[2]}
        self.addCuad(cuadruplo)
        
        if self.className != '':
            params = self.dirClasses.getClassFunParam(dtype, code[2])
        else:
            params = self.dirClasses.getClassFunParam(dtype, code[2], True)

        if len(params) != len(code[3]):
            exit(f'Error: Parameters mismatch at {code[2]} function call')
        
        p = 1
        for param in code[3]:
            if type(param) is not list:
                param = [param]
            val = self.saveExpCuads(param)
            dtype = self.checkType(val)

            if dtype != params[p-1]:
                exit(f'Error: Parameter type mismatch at {param} in function {code[2]} call')
            cuadruplo =  {'accion': 'paramP', 'val1': val, 'val2': code[2], 'final': f'par{p}'}
            self.addCuad(cuadruplo)
            p += 1

        cuadruplo =  {'accion': 'GosubP', 'val1': code[1], 'val2': '', 'final': code[2]}
        self.addCuad(cuadruplo)
        dtype = self.dirFuns.getIdType(self.funName, code[1])
        funType = self.dirClasses.findFunType(dtype, code[2], True)

        if funType != 'void':
            if self.funName == '':
                self.table.addVar('t{}'.format(self.t), funType, 'temporal')
            else:
                self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), funType)
            
            cuadruplo =  {'accion': '=', 'val1': code[2], 'val2': '', 'final': 't{}'.format(self.t)}
            self.addCuad(cuadruplo)
            self.t = self.t + 1
            return 't{}'.format(self.t-1)
        return False
        

    def blockHandle(self, code):
        if code[0] == 'condition':
            self.saveConditionCuads(code)
        elif code[0] == 'assign':
            self.saveAssignCuads(code)
        elif code[0] == 'while':
            self.saveWhileCuads(code)
        elif code[0] == 'outco':
            self.saveOutcoCuads(code)
        elif code[0] == 'inco':
            self.saveIncoCuads(code)
        elif code[0] == 'call':
            self.saveCallCuads(code)
        elif code[0] == 'return':
            self.saveReturnCuads(code)
        elif code[0] == 'array':
            self.saveArrayCuads(code)
        elif code[0] == 'method':
            self.saveMethodCuads(code)
        else:
            exit(f"Error: statement {code[0]} non existant")

    def addCuad(self, cuadruplo):
        self.cuad.append(cuadruplo)
        self.count = self.count + 1

    def clearTemp(self):
        self.t = 1

    def expCuads(self):
        operandStack = []
        tokenList = self.vp
        typeList = self.pTipos
        self.vp = []
        self.pTipos = []

        for token in tokenList:
            if token in self.operators:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                # Do cuads for call or an array in case a function is being used in an exp
                if type(operand1) == list:
                    if operand1[0] == 'call':
                        operand1 = self.saveCallCuads(operand1)
                    elif operand1[0] == 'array':
                        operand1 = self.saveArrayCuads(operand1)
                    elif operand1[0] == 'multM':
                        if type(operand2) == list and operand2[0] == 'multM':
                            if operand2[2] == operand1[2]:
                                if token == '*':
                                    if len(operandStack) == 0:
                                        retTemp = []
                                        for row in range(operand1[2][0]):
                                            for col in range(operand1[2][0]):
                                                multTemp = []
                                                for mult in range(operand1[2][0]):
                                                    val1 = self.saveArrayCuads(['array', operand1[1], [row, mult]])
                                                    val2 = self.saveArrayCuads(['array', operand2[1], [mult, col]])
                                                    final = self.saveExpCuads([val1, '*', val2])
                                                    multTemp.append(final)

                                                hold = multTemp[0]
                                                for sum in range(1, operand1[2][0]):
                                                    final = self.saveExpCuads([hold, '+', multTemp[sum]])
                                                    hold = final
                                                retTemp.append(hold)
                                        print(retTemp)
                                        return retTemp

                                    else:
                                        exit('Error: Unsupported operation for matrix')
                                else:
                                    exit('Error: Only matrix multiplication supported')
                            else:
                                exit('Error: Unsupported non square matrix multiplication')
                        else:
                            exit('Error: Trying to multiply a matrix with a value')


                # Do cuads for call or an array in case a function is being used in an exp    
                if type(operand2) == list:
                    if operand2[0] == 'call':
                        operand2 = self.saveCallCuads(operand2)
                    elif operand2[0] == 'array':
                        operand2 = self.saveArrayCuads(operand2)
                    elif operand2[0] == 'multM':
                        if not (type(operand1) == list and operand1[0] == 'multM'):
                            exit('Error: Trying to multiply a matrix with a value')

                type2 = self.getType(operand2)
                type1 = self.getType(operand1)
                
                typeResult = self.cube.typeCheck(type1, type2, token)
                if typeResult == 'x':
                    exit('Error: Type mismatch between {} : {} and {} : {}'.format(operand1, type1, operand2, type2))
                else:
                    typeList.append(typeResult)
                    if self.className != '':
                        self.dirClasses.addTemp(self.className, self.funName, 't{}'.format(self.t), typeResult)
                    elif self.funName != '':
                        self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), typeResult)
                    else:
                        self.table.addVar('t{}'.format(self.t), [], typeResult, 'temporal')
                                    
                cuadruplo =  {'accion': token, 'val1': operand1, 'val2': operand2, 'final': 't{}'.format(self.t)}
                self.addCuad(cuadruplo)
                operandStack.append('t{}'.format(self.t))
                self.t = self.t + 1
            else:
                if type(token) == list:
                    if token[0] == 'call':
                        token = self.saveCallCuads(token)
                    elif token[0] == 'array':
                        token = self.saveArrayCuads(token)
                    elif token[0] == 'method':
                        token = self.saveMethodCuads(token)
                elif self.getArrayDim(token) != [] and self.getArrayDim(token) != -1:
                        dim = self.getArrayDim(token)
                        if len(dim) == 2 and dim[0] == dim[1]:
                            token = ['multM', token, dim]
                        else:
                            exit(f'Error: Trying to use array in an expr without accessing with an index')

                operandStack.append(token)
        if len(operandStack) < 1:
            return ''
        else:
            return operandStack.pop()
        
    def readEXP(self, exp):
        for index in exp:
            if index not in self.operators:                                     # non operators
                if type(index) is list:
                    if index[0] == 'array':                                     #for arrays
                        dtype = self.getType(index[1])
                    elif index[0] == 'method':
                        dtype = 'method'
                    else:
                        if self.className != '':                                 #For Functions
                            dtype = self.dirClasses.findFunType(self.className, self.funName)
                        else:                                             
                            dtype = self.dirFuns.getFunType(index[1])
                        if dtype == 'void':
                            exit(f'Error: Function type void has return value')
                elif type(index) is str and index[0] == '"' and len(index) == 3:    # chars
                    self.table.addVar(index, [], 'char', 'cte')
                elif type(index) is str:                                            #for variables
                    dtype = self.getType(index)
                else:
                    self.table.addVar(index, [], self.table.getValType(index), 'cte')

                self.addVP(index)

            elif index in self.plusMinus:
                multdiv = 1
                while multdiv:
                    multdiv = self.checkMultDiv()
                
                self.checkPlusMinus()
                self.addOP(index)
            elif index in self.multDiv:
                self.checkMultDiv()
                self.addOP(index)
                
            elif index in self.comparison:
                self.checkPlusMinus()
                self.checkMultDiv()
                self.checkComp()
                self.addOP(index)

            elif index in self.andOr:
                compar = 1
                while compar:
                    compar = self.checkComp()
                self.checkAndOr()
                self.addOP(index)

            elif index == '(':
                self.addOP(index)
            elif index == ')':
                while self.pOper[-1] != '(':
                    self.checkAndOr()
                    self.checkComp()
                    self.checkMultDiv()
                    self.checkPlusMinus()
                self.pOper.pop()        
        
        
        multdiv = 1
        while multdiv:
            multdiv = self.checkMultDiv()
        plusminus = 1
        while plusminus:
            plusminus = self.checkPlusMinus()
        compar = 1
        while compar:
            compar = self.checkComp()
        andOr = 1
        while andOr:
            andOr = self.checkAndOr()
                
            
    
    def polishEval(self, table: symbolTable):
        operandStack = []
        tokenList = self.vp
        
        for token in tokenList:
            if token in self.operators:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result = self.calculate(token, operand1, operand2)
                operandStack.append(result)
            else:
                if token[0].isalpha():
                    operandStack.append(float(table.getIdVal(token)))
                else:
                    operandStack.append(float(token))
        return operandStack.pop()
    
    
    def calculate(self, operator, operand1, operand2):
        if operator == "+":
            return operand1 + operand2
        elif operator == "-":
            return operand1 - operand2
        elif operator == "*":
            return operand1 * operand2
        elif operator == "/":
            return operand1 / operand2
        elif operator == "<":
            return operand1 < operand2
        elif operator == ">":
            return operand1 > operand2
        elif operator == "==":
            return operand1 == operand2
        elif operator == "<>":
            return operand1 != operand2
        elif operator == "&&":
            return operand1 and operand2
        elif operator == "||":
            return operand1 or operand2
    def clearCache(self):
        self.vp = []
        self.pOper = []
        self.pTipos = []
            
    def addVP(self, val):
        self.vp.append(val)
        
    def addOP(self, val):
        self.pOper.append(val)
        
    def checkPlusMinus(self):
        if len(self.pOper) > 0 and self.pOper[-1] in self.plusMinus:
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0
            
            
    def checkMultDiv(self):
        if len(self.pOper) > 0 and self.pOper[-1] in self.multDiv:
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0
    
    def checkComp(self):
        if len(self.pOper) > 0 and self.pOper[-1] in self.comparison:
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0
    
    def checkAndOr(self):
        if len(self.pOper) > 0 and self.pOper[-1] in self.andOr:
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0

    def __str__(self):
        print('\nCuadruplos is')
        c = 0
        for x in self.cuad:
            print(f'\n{c}. {x}')
            c = c+1
        return f''
        
