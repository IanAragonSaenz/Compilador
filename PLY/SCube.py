class sCube:
    def __init__(self):
        self.cube = {
            "ii": {
                '+': 'int',
                '-': 'int',
                '*': 'int',
                '/': 'float',
                '&&': 'x',
                '||': 'x',
                '<': 'bool',
                '>': 'bool',
                '==': 'bool',
                '<>': 'bool',
                '=': 'int'
            },
            "if": {
                '+': 'float',
                '-': 'float',
                '*': 'float',
                '/': 'float',
                '&&': 'x',
                '||': 'x',
                '<': 'bool',
                '>': 'bool',
                '==': 'bool',
                '<>': 'bool',
                '=': 'float'
            },
            "ib": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            
            "ic": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
              
            "ff": {
                '+': 'float',
                '-': 'float',
                '*': 'float',
                '/': 'float',
                '&&': 'x',
                '||': 'x',
                '<': 'bool',
                '>': 'bool',
                '==': 'bool',
                '<>': 'bool',
                '=': 'float'
            },
            "fb": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            
             "fc": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
               "cb": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
               
               "cc": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'bool',
                '<>': 'bool',
                '=': 'char'
            },

            "bb": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'bool',
                '||': 'bool',
                '<': 'x',
                '>': 'x',
                '==': 'bool',
                '<>': 'bool',
                '=': 'bool'
            },

# cambio a los opuestos

            "fi": {
                '+': 'float',
                '-': 'float',
                '*': 'float',
                '/': 'float',
                '&&': 'x',
                '||': 'x',
                '<': 'bool',
                '>': 'bool',
                '==': 'bool',
                '<>': 'bool',
                '=': 'float'
            },
            
            "bi": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            
            "ci": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            
            "bf": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            
            "cf": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            },
            "bc": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'x',
                '||': 'x',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x',
                '=': 'x'
            } 
        }

    #typeCheck recibe dos numeros y un operador y regresa el tipo de dato que arroja esa operacion
    def typeCheck(self, num1, num2, op):
        dtype = self.shortenType(num1) + self.shortenType(num2)
        return self.cube[dtype][op]

    #shortenType recibe el tipo de dato y regresa un version corta de ese tipo
    def shortenType(self, dtype):
        if dtype == 'int':
            return 'i'
        if dtype == 'float':
            return 'f'
        if dtype == 'char':
            return 'c'
        if dtype == 'bool':
            return 'b'
        else:
            exit('type {} doesn\'t exist'.format(dtype))
