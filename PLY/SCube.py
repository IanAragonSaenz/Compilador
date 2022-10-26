class sCube:
    def __init__(self):
        self.cube = {
            "ii": {
                '+': 'i',
                '-': 'i',
                '*': 'i',
                '/': 'f',
                '&&': 'b',
                '||': 'b',
                '<': 'b',
                '>': 'b',
                '==': 'b',
                '<>': 'b'
            },
            "if": {
                '+': 'f',
                '-': 'f',
                '*': 'f',
                '/': 'f',
                '&&': 'b',
                '||': 'b',
                '<': 'b',
                '>': 'b',
                '==': 'b',
                '<>': 'b'
            },
            "ib": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            
            "ic": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
              
            "ff": {
                '+': 'f',
                '-': 'f',
                '*': 'f',
                '/': 'f',
                '&&': 'b',
                '||': 'b',
                '<': 'b',
                '>': 'b',
                '==': 'b',
                '<>': 'b'
            },
            "fb": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            
             "fc": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
               "cb": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },

# cambio a los opuestos

            "fi": {
                '+': 'f',
                '-': 'f',
                '*': 'f',
                '/': 'f',
                '&&': 'b',
                '||': 'b',
                '<': 'b',
                '>': 'b',
                '==': 'b',
                '<>': 'b'
            },
            
            "bi": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            
            "ci": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            
            "bf": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            
            "cf": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            },
            "bc": {
                '+': 'x',
                '-': 'x',
                '*': 'x',
                '/': 'x',
                '&&': 'b',
                '||': 'b',
                '<': 'x',
                '>': 'x',
                '==': 'x',
                '<>': 'x'
            } 
        }

    def typeCheck(self, num1, num2, op):
        dtype = self.shortenType(num1) + self.shortenType(num2)
        return self.cube[dtype][op]

    def shortenType(self, dtype):
        if dtype == 'int':
            return 'i'
        if dtype == 'float':
            return 'f'
        if dtype == 'char':
            return 'c'
        if dtype == 'bool':
            return 'b'