class symbolTable:

    def add(self, type, dType, id, args):

        if type == 'V':
            self.type = "VARIABLE"
            if dType == "int":
                self.dataType = 'f'
            elif dType == "float":
                self.dataType = 'f'
            else:
                self.dataType = 'c'
            self.id = id
            self.args = "NULL"


