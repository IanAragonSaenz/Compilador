from symbol_table import symbolTable

class cuadruplos:
    def __init__(self):
        self.vp = []
        self.pOper = []
        self.pSalto = []
        self.operators = ["+", "-", "*", "/", "<", ">", "==", "<>", "(", ")", "&&", "||"]
        self.plusMinus = ["+", "-"]
        self.multDiv = ["*", "/"]
        self.comparison = ["<", ">", "==", "<>"]
        self.andOr = ["&&", "||"]
        self.t = 1
        self.count = 0
        self.cuad = []
        #{'accion' : '*', 'val1' : '1', 'val2' : 'count', 'final' : 't3'}
        
    
    def saveExpCuads(self, exp):
        self.readEXP(exp)
        val = self.expCuads()
        self.clearCache()
        return val

    def saveAssignCuads(self, assign):
        val = self.saveExpCuads(assign[2])
        cuadruplo =  {'accion': '=', 'val1': val, 'val2': '', 'final': assign[1]}
        self.cuad.append(cuadruplo)
        self.count = self.count + 1
        
    def saveConditionCuads(self, code):
        val = self.saveExpCuads(code[1])
        cuadruplo =  {'accion': 'gotoF', 'val1': val, 'val2': '', 'final': ''}
        self.cuad.append(cuadruplo)
        self.count = self.count + 1
        self.pSalto.append(self.count-1)
        
        for block in code[2]:
            self.blockHandle(block)

        # check for else
        if code[3]:
            falso = self.pSalto.pop()
            cuadruplo =  {'accion': 'goto', 'val1': '', 'val2': '', 'final': ''}
            self.cuad.append(cuadruplo)
            self.count = self.count + 1
            self.pSalto.append(self.count-1)
            self.cuad[falso]['final'] = self.count
            for block in code[3]:
                self.blockHandle(block)

        salto = self.pSalto.pop()
        self.cuad[salto]['final'] = self.count

        

    def blockHandle(self, code):
        if code[0] == 'condition':
            self.saveConditionCuads(code)
            
        elif code[0] == 'assign':
            self.saveAssignCuads(code)
            # ['assign', p[1], p[3]]



    def expCuads(self):
        operandStack = []
        tokenList = self.vp
        
        for token in tokenList:
            if token in self.operators:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                #result = self.calculate(token, operand1, operand2)
                cuadruplo =  {'accion': token, 'val1': operand1, 'val2': operand2, 'final': 't{}'.format(self.t)}
                self.cuad.append(cuadruplo)
                self.count = self.count + 1
                operandStack.append('t{}'.format(self.t))
                self.t = self.t + 1
                
            else:
                if token[0].isalpha():
                    operandStack.append(token)
                else:
                    operandStack.append(float(token))
        return operandStack.pop()
        
    def readEXP(self, exp):
        for index in exp:
            if index not in self.operators:
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
        
