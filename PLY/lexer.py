import ply.lex as lex


#El lexer empieza definiendo las palabras reservadas que el lenguaje usa usando diccionarios de python

t_SIGN = r'\"([^\\\"]|\\.)*\"'

reserved = {'program':'PROGRAM','var':'VAR', 'if':'IF', 'else':'ELSE', 'int':'INT', 'float':'FLOAT', 
			'class':'CLASS', 'public':'PUBLIC', 'private':'PRIVATE', 'inherit':'INHERIT', 'return':'RETURN', 'main':'MAIN',
			'fun':'FUN', 'char':'CHAR', 'void':'VOID', 'file':'FILE', 'while':'WHILE', 'outco':'OUTCO','inco':'INCO', 
			'bool':'BOOL', 'true':'TRUE', 'false':'FALSE'}

#Definimos los tokens

tokens = ['SIGN', 'LEFTPAREN','RIGHTPAREN', 'LEFTBRACKET', 'RIGHTBRACKET', 'SEMICOLON', 'COMP_EQUAL', 'COMP_NOTEQUAL',
		  'COMMA', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'CTEF', 'CTEI', 'COMP_GREATER', 
		  'COMP_LESS', 'COLON', 'COMP_OR', 'COMP_AND', 'LEFTKEY', 'RIGHTKEY', 'DOT', 'CHAR_DEC', 'ASSIGN', 'ID'] + list(reserved.values())

#Definimos las regex

def t_CTEF(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_CTEI(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'ID')
	return t

def t_newline(t):	
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\//.*'
    pass

def t_CHAR_DEC(t):
	r'\"[A-za-z0-9]\"'
	t.value = str(t.value)
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
t_LEFTBRACKET = r'\{'
t_RIGHTBRACKET = r'\}'
t_SEMICOLON = r'\;'
t_COMP_EQUAL = r'\=\='
t_COMP_NOTEQUAL = r'\<\>'
t_COMMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_COMP_GREATER = r'\>'
t_COMP_LESS = r'\<'
t_COLON = r':'
t_COMP_OR = r'\|\|'
t_COMP_AND = r'\&\&'
t_LEFTKEY = r'\['
t_RIGHTKEY = r'\]'
t_DOT = r'.'
t_ASSIGN = r'\='

t_ignore = " \t\n"

lexer = lex.lex()