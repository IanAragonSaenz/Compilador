from symbol_table import symbolTable
from DirFun import dirFun
from SCube import sCube
class cuadruplos:
    def __init__(self, table: symbolTable, dirFuns: dirFun):
        self.cube = sCube()
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
        self.returns = 0
        #{'accion' : '*', 'val1' : '1', 'val2' : 'count', 'final' : 't3'}
        
    #function ['int', 'fib', 
    #[['int', 'param1'], ['int', 'param2']], 
    #['float', [['prepucio', None]]], 
    #[['condition', [3], [['assign', 'param1', ['param2']]], None]], 
    #[3]]

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
        f.close()


    def saveFunCuads(self, fun):
        self.funName = fun[1]
        self.returns = 0
        self.dirFuns.addFun(fun, self.count)
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
            self.table.addVar(fun[1], [], fun[0], 'global')
        self.funName = ''
        self.clearTemp()
        self.returns = 0

    def saveReturnCuads(self, code):
        if self.funName == '':
            exit('Error: return used outside of a function')

        funType = self.dirFuns.getFunType(self.funName)
        if funType != 'void' and not code[1]:
            exit(f'Error: {funType} function not returning a value, function name: {self.funName[-1]}')
        elif funType == 'void' and code[1]:
            exit(f'Error: void function returning a value, function name: {self.funName[-1]}')
        elif funType != 'void' and code[1]:
            ret = self.saveExpCuads(code[1])
            cuadruplo =  {'accion': 'return', 'val1': '', 'val2': '', 'final': ret}
            self.addCuad(cuadruplo)
        else:
            cuadruplo =  {'accion': 'return', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
        
        self.returns += 1
    
    def saveArrayCuads(self, code):
        address = self.table.getIdDirV(code[1])
        dimMin = 0
        dimMax = self.getArrayDim(code[1])
        if len(dimMax) != len(code[2]) or len(dimMax) == 0:
            exit(f'Error: dimensions are not the same in var {code[1]}')
        
        dtype = self.getType(code[1])
        exp = code[2][0]
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
        params = self.dirFuns.getFunParams(call[1])

        if len(params) != len(call[2]):
            exit(f'params don\'t match with function {call[1]} definition')
        
        p = 1
        for param in call[2]:
            val = self.saveExpCuads(param)
            
            dtype = self.checkType(val)

            if dtype != params[p-1]:
                exit(f'type mismatch on parameter {param} from function {call[1]}')

            cuadruplo =  {'accion': 'param', 'val1': val, 'val2': '', 'final': f'par{p}'}
            self.addCuad(cuadruplo)
            p += 1

        cuadruplo =  {'accion': 'Gosub', 'val1': '', 'val2': '', 'final': call[1]}
        self.addCuad(cuadruplo)

        funType = self.dirFuns.getFunType(call[1])
        if funType != 'void':
            if self.funName == '':
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
        if len(self.funName) > 0:
            fun = self.dirFuns.getIdType(self.funName, index)
            if fun == -1:
                dtype = self.table.getIdType(index)
                if dtype == -1:
                    exit('var doesnt exist no{}'.format(index))
                else:
                    return dtype
            else:
                return fun
        else:
            dtype = self.table.getIdType(index)
            if dtype == -1:
                exit('var doesnt exist yes{}'.format(index))
            else:
                return dtype

    def getArrayDim(self, index):
        if len(self.funName) > 0:
            fun = self.dirFuns.getIdDim(self.funName, index)
            if fun == -1:
                dtype = self.table.getIdDim(index)
                if dtype == -1:
                    exit('var doesnt exist no{}'.format(index))
                else:
                    return dtype
            else:
                return fun
        else:
            dtype = self.table.getIdDim(index)
            if dtype == -1:
                exit('var doesnt exist yes{}'.format(index))
            else:
                return dtype

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
        right = self.getType(val)
        

        typeCheck = self.cube.typeCheck(left, right, '=')
        if typeCheck == 'x':
            exit(f'type mismatch when assigning value {code[1]}')
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

                # Do cuads for call or an array in case a function is being used in an exp    
                if type(operand2) == list:
                    if operand2[0] == 'call':
                        operand2 = self.saveCallCuads(operand2)
                    elif operand2[0] == 'array':
                        operand2 = self.saveArrayCuads(operand2)

                type2 = self.getType(operand2)
                type1 = self.getType(operand1)
                
                typeResult = self.cube.typeCheck(type1, type2, token)
                if typeResult == 'x':
                    exit('Type mismatch between {} : {} and {} : {}'.format(operand1, type1, operand2, type2))
                else:
                    typeList.append(typeResult)
                    if self.funName == '':
                        self.table.addVar('t{}'.format(self.t), [], typeResult, 'temporal')
                    else:
                        self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), typeResult)
                                    
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
                    else:                                                       #For Functions
                        dtype = self.dirFuns.getFunType(index[1])
                        if dtype == 'void':
                            exit(f'void function can\'t be used in an expression')
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
        
