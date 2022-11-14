from symbol_table import symbolTable
from SCube import sCube
class cuadruplos:
    def __init__(self, table: symbolTable):
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
        #{'accion' : '*', 'val1' : '1', 'val2' : 'count', 'final' : 't3'}
        
    
    def saveExpCuads(self, exp):
        self.readEXP(exp)
        val = self.expCuads()
        self.clearCache()
        return val
    
    def saveOutcoCuads(self, code):
        for x in code[1]:
            if type(x) is str:
                val = self.saveExpCuads([x])
            else:
                val = self.saveExpCuads(x)
            cuadruplo =  {'accion': 'outco', 'val1': val, 'val2': '', 'final': ''} 
            self.addCuad(cuadruplo)
                
        
    def saveIncoCuads(self, code):
        val = code[1]
        cuadruplo =  {'accion': 'inco', 'val1': val, 'val2': '', 'final': ''} 
        self.addCuad(cuadruplo)
        
    def saveAssignCuads(self, code):
        val = self.saveExpCuads(code[2])
        left = self.table.getIdType(code[1])

        if type(val) is str and val[0] == '"' and len(val) == 3:
            right = 'char'
        elif type(val) is str:
            right = self.table.getIdType(val)
        else:
            right = self.table.getValType(val)


        typeCheck = self.cube.typeCheck(left, right, '=')
        if typeCheck == 'x':
            print(f'type mismatch when assigning value {code[1]}')
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
            for block in code[3]:
                self.blockHandle(block)

        salto = self.pSalto.pop()
        self.cuad[salto]['final'] = self.count

        
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

    def blockHandle(self, code):
        if code[0] == 'condition':
            self.saveConditionCuads(code)
        elif code[0] == 'assign':
            self.saveAssignCuads(code)
            # ['assign', p[1], p[3]]
        elif code[0] == 'while':
            self.saveWhileCuads(code)
        elif code[0] == 'outco':
            self.saveOutcoCuads(code)
        elif code[0] == 'inco':
            self.saveIncoCuads(code)

    def addCuad(self, cuadruplo):
        self.cuad.append(cuadruplo)
        self.count = self.count + 1

    def expCuads(self):
        operandStack = []
        tokenList = self.vp
        
        for token in tokenList:
            if token in self.operators:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                type2 = self.pTipos.pop()
                type1 = self.pTipos.pop()

                typeResult = self.cube.typeCheck(type1, type2, token)
                if typeResult == 'x':
                    print('Type mismatch')
                else:
                    self.pTipos.append(typeResult)
                    self.table.addVar('t{}'.format(self.t), typeResult, 'temporal')
                    
                #result = self.calculate(token, operand1, operand2)
                
                cuadruplo =  {'accion': token, 'val1': operand1, 'val2': operand2, 'final': 't{}'.format(self.t)}
                self.addCuad(cuadruplo)
                operandStack.append('t{}'.format(self.t))
                self.t = self.t + 1
            else:
                operandStack.append(token)
        return operandStack.pop()
        
    def readEXP(self, exp):
        for index in exp:
            if index not in self.operators:
                if type(index) is str and index[0] == '"' and len(index) == 3:
                    self.pTipos.append('char')
                elif type(index) is str:
                    self.pTipos.append(self.table.getIdType(index))
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
        
