import ply.lex as lex


#El lexer empieza definiendo las palabras reservadas que el lenguaje usa usando diccionarios de python

reserved = {'program':'PROGRAM','var':'VAR', 'print':'PRINT', 'if':'IF', 'else':'ELSE', 'int':'INT', 'float':'FLOAT', 
			'class':'CLASS', 'public':'PUBLIC', 'private':'PRIVATE', 'inherit':'INHERIT', 'return':'RETURN'}

#Definimos los tokens

tokens = ['LEFTPAREN','RIGHTPAREN', 'LEFTBRACKET', 'RIGHTBRACKET', 'SEMICOLON', 'EQUAL', 'NOTEQUAL',
		  'COMMA', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'CTESTRING', 'CTEI', 'CTEF','ID', 'GREATER', 
		  'LESS', 'COLON'] + list(reserved.values())

#Definimos las regex

def t_CTEI(t):
	r'\d+'
	t.value = int(t.value)
	return t;

def t_CTEF(t):
	r'[0-9]*\.[0-9]+|[0-9]+'
	t.value = float(t.value)
	return t

def t_ID(t):
	r'[A-za-z]([A-za-z]|[0-9])*'
	t.type = reserved.get(t.value, 'ID')
	return t

def t_newline(t):	
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\//.*'
    pass


def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
t_LEFTBRACKET = r'\{'
t_RIGHTBRACKET = r'\}'
t_SEMICOLON = r'\;'
t_EQUAL = r'\='
t_NOTEQUAL = r'<>'
t_COMMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_CTESTRING = r'\".*\"'
t_GREATER = r'>'
t_LESS = r'<'
t_COLON = r':'
t_CLASS = 

t_ignore = " \t"

lexer = lex.lex()