from symbol_table import symbolTable

class cuadruplos:
    def __init__(self):
        self.vp = []
        self.pOper = []
        self.pSalto = []
        
    #polishEval(readExp("3+1*1"))
    def readEXP(self, exp):
        #3*1
        # 3 
        plusminus = 1
        for index in exp:
            if index != '+' and index != '-' and index != '/' and index != '*':
                self.addVP(index)
            elif index == '+' or index == '-':
                multdiv = 1
                while multdiv:
                    multdiv = self.checkMultDiv()
                
                self.checkPlusMinus()
                self.addOP(index)
            elif index == '*' or index == '/':
                self.checkMultDiv()
                self.addOP(index)
        
        multdiv = 1
        while multdiv:
            multdiv = self.checkMultDiv()
        while plusminus:
            plusminus = self.checkPlusMinus()
            
            
    
    def polishEval(self, table: symbolTable):
        operators = ["+", "-", "*", "/"]
        operandStack = []
        tokenList = self.vp
        
        for token in tokenList:
            if token in operators:
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
        
    def clearCache(self):
        self.vp = []
        self.pOper = []
        self.pSalto = []
            
    def addVP(self, val):
        self.vp.append(val)
        
    def addOP(self, val):
        self.pOper.append(val)
        #print('Added ',val)
        
    def checkPlusMinus(self):
        if len(self.pOper) > 0 and (self.pOper[-1] == '+' or self.pOper[-1] == '-'):
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0
            
            
    def checkMultDiv(self):
        if len(self.pOper) > 0 and (self.pOper[-1] == '*' or self.pOper[-1] == '/'):
            signo = self.pOper.pop(-1)
            self.addVP(signo)
            return 1
        return 0

    def __str__(self):
        print("Exp result is", self.polishEval())
        return f'VP is {self.vp}'
        
#1+3*4-2