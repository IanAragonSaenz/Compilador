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
        self.count = 0
        self.cuad = []
        self.table = table
        self.dirFuns = dirFuns
        self.funName = ''
        #{'accion' : '*', 'val1' : '1', 'val2' : 'count', 'final' : 't3'}
        
    #function ['int', 'fib', 
    #[['int', 'param1'], ['int', 'param2']], 
    #['float', [['prepucio', None]]], 
    #[['condition', [3], [['assign', 'param1', ['param2']]], None]], 
    #[3]]
    def saveFunCuads(self, fun):
        size = 0
        self.funName = fun[1]
        self.dirFuns.addFun(fun, self.count)
        for block in fun[4]:
            size += self.blockHandleFun(block)
        ret, tsize = self.saveExpCuads(fun[5])
        size += tsize
        self.dirFuns.addTemp(fun[1], size) 
        cuadruplo =  {'accion': 'return', 'val1': '', 'val2': '', 'final': ret}
        self.addCuad(cuadruplo)

        cuadruplo =  {'accion': 'EndProc', 'val1': '', 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.funName = ''
        self.dirFuns.printSelf()
        self.clearTemp()


    def saveExpCuads(self, exp):
        self.readEXP(exp)
        val, tSize = self.expCuads()
        self.clearCache()
        return val, tSize

    
    def saveOutcoCuads(self, code):
        size = 0
        for x in code[1]:
            if type(x) is str:
                val, tsize = self.saveExpCuads([x])
            else:
                val, tsize = self.saveExpCuads(x)
            cuadruplo =  {'accion': 'outco', 'val1': val, 'val2': '', 'final': ''} 
            self.addCuad(cuadruplo)
            size += tsize
        return size
           
        
    def saveIncoCuads(self, code):
        val = code[1]
        cuadruplo =  {'accion': 'inco', 'val1': val, 'val2': '', 'final': ''} 
        self.addCuad(cuadruplo)
        return 0
        
    def getType(self, index):
        if len(self.funName) > 0:
            fun = self.dirFuns.getIdType(self.funName, index)
            if fun == -1:
                dtype = self.table.getIdType(index)
                if dtype == -1:
                    exit('var doesnt exist {}'.format(index))
                else:
                    return dtype
            else:
                return fun
        else:
            dtype = self.table.getIdType(index)
            if dtype == -1:
                exit('var doesnt exist {}'.format(index))
            else:
                return dtype
        return -1

    def saveAssignCuads(self, code):
        val, size = self.saveExpCuads(code[2])
        left = self.getType(code[1])

        if type(val) is str and val[0] == '"' and len(val) == 3:
            right = 'char'
        elif type(val) is str:
            right = self.getType(val)
        else:
            right = self.table.getValType(val)


        typeCheck = self.cube.typeCheck(left, right, '=')
        if typeCheck == 'x':
            print(f'type mismatch when assigning value {code[1]}')
        #elif typeCheck != left and left == 'int' and typeCheck == 'float':


        cuadruplo =  {'accion': '=', 'val1': val, 'val2': '', 'final': code[1]}
        self.addCuad(cuadruplo)
        return size
        
    def saveConditionCuads(self, code):
        val, size = self.saveExpCuads(code[1])
        cuadruplo =  {'accion': 'gotoF', 'val1': val, 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.pSalto.append(self.count-1)
        
        for block in code[2]:
            size += self.blockHandle(block)

        # check for else
        if code[3]:
            falso = self.pSalto.pop()
            cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': ''}
            self.addCuad(cuadruplo)
            self.pSalto.append(self.count-1)
            self.cuad[falso]['final'] = self.count
            for block in code[3]:
                size += self.blockHandle(block)

        salto = self.pSalto.pop()
        self.cuad[salto]['final'] = self.count
        return size

        
    def saveWhileCuads(self, code):
        self.pSalto.append(self.count) #Revaluar 3
        val, size = self.saveExpCuads(code[1])
        cuadruplo =  {'accion': 'gotoF', 'val1': val, 'val2': '', 'final': ''}
        self.addCuad(cuadruplo)
        self.pSalto.append(self.count-1) #guardar donde va el gotoF, para ponerle a donde saltar
        
        for block in code[2]:
            size += self.blockHandle(block)
        
        falso = self.pSalto.pop()
        retorno = self.pSalto.pop()
        cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': retorno}
        self.addCuad(cuadruplo)
        self.cuad[falso]['final'] = self.count
        return size

    def blockHandle(self, code):
        if code[0] == 'condition':
            return self.saveConditionCuads(code)
        elif code[0] == 'assign':
            return self.saveAssignCuads(code)
            # ['assign', p[1], p[3]]
        elif code[0] == 'while':
            return self.saveWhileCuads(code)
        elif code[0] == 'outco':
            return self.saveOutcoCuads(code)
        elif code[0] == 'inco':
            return self.saveIncoCuads(code)
        else:
            print("Error: statement non existant")
            return 0
    
    def blockHandleFun(self, code):
        if code[0] == 'condition':
            return self.saveConditionCuads(code)
        elif code[0] == 'assign':
            return self.saveAssignCuads(code)
        elif code[0] == 'while':
            return self.saveWhileCuads(code)
        elif code[0] == 'outco':
            return self.saveOutcoCuads(code)
        elif code[0] == 'inco':
            return self.saveIncoCuads(code)
        elif code[0] == 'return':
            return 0

    def addCuad(self, cuadruplo):
        self.cuad.append(cuadruplo)
        self.count = self.count + 1

    def clearTemp(self):
        self.t = 1

    def expCuads(self):
        operandStack = []
        tokenList = self.vp
        size = 0
        
        for token in tokenList:
            if token in self.operators:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                type2 = self.pTipos.pop()
                type1 = self.pTipos.pop()

                typeResult = self.cube.typeCheck(type1, type2, token)
                if typeResult == 'x':
                    exit('Type mismatch between {} and {}'.format(operand1, operand2))
                else:
                    self.pTipos.append(typeResult)
                    if self.funName == '':
                        self.table.addVar('t{}'.format(self.t), typeResult, 'temporal')
                    else:
                        self.dirFuns.addTempVar(self.funName, 't{}'.format(self.t), typeResult)
                    
                #result = self.calculate(token, operand1, operand2)
                
                cuadruplo =  {'accion': token, 'val1': operand1, 'val2': operand2, 'final': 't{}'.format(self.t)}
                self.addCuad(cuadruplo)
                operandStack.append('t{}'.format(self.t))
                self.t = self.t + 1
                size = size + 1
            else:
                operandStack.append(token)
        if len(operandStack) < 1:
            return '', size
        else:
            return operandStack.pop(), size
        
    def readEXP(self, exp):
        for index in exp:
            if index not in self.operators:
                if type(index) is str and index[0] == '"' and len(index) == 3:
                    self.pTipos.append('char')
                elif type(index) is str:
                    dtype = self.getType(index)
                    self.pTipos.append(dtype)
                else:
                    self.pTipos.append(self.table.getValType(index))

                self.addVP(index)
                #print('VP is', self.vp)
                #print('pilaT is', self.pTipos)
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
        
