from symbol_table import symbolTable
from SCube import sCube
from Cuadruplos import cuadruplos
import numpy as np

cuad = cuadruplos()
table = symbolTable()
cube = sCube()
def p_program(p):
    '''program : PROGRAM ID SEMICOLON dec_vars dec_fun dec_class MAIN LEFTPAREN RIGHTPAREN LEFTBRACKET dec_vars dec_block RIGHTBRACKET'''
    p[0] = ("COMPILED", p[1], p[2], p[3], p[4])



##
##          DECLARACION DE VARIABLES
##
def p_dec_vars(p):
    '''dec_vars : VAR vars SEMICOLON 
                | empty'''
    if len(p) == 4:
        p[0] = p[2]

        #print(table)
        ret = table.idSplit(p[2][1], p[2][0], 'global')
        if ret == -1:
            print("Error: variable ya declarada")
        

## elige entre simple o complejo
def p_vars(p):
    '''vars : vars_simple 
            | vars_complex'''
    p[0] = p[1]

## se hace vars simple poniendo su tipo y luego la declaracion
def p_vars_simple(p):
    '''vars_simple : type_simple vars_simple_dec '''
    p[0] = (p[1], p[2])

## se llama al id para poder poner arrays o no y el more para loopear
def p_vars_simple_dec(p):
    '''vars_simple_dec : vars_simple_id vars_simple_more'''
    if p[2]:
        if type(p[2]) is list:
            p[2].append(p[1])
            p[0] = p[2]
        else:
            p[0] = [p[2], p[1]]
    else:
        p[0] = [p[1]]
    
    

## Loopea para multiples declaraciones
def p_vars_simple_more(p):
    '''vars_simple_more : COMMA vars_simple_dec
                        | empty'''
    if len(p) == 3:
        p[0] = p[2]

## Pone el id y la posibilidad de que sea array
def p_vars_simple_id(p):
    '''vars_simple_id : ID vars_simple_arr'''
    p[0] = [p[1], p[2]]
    
## opcion para tener array de una dimension
def p_vars_simple_arr(p):
    '''vars_simple_arr : LEFTKEY CTEI RIGHTKEY vars_simple_arr2
                        | empty'''
    if len(p) == 5:
        if p[4]:
            p[0] = [p[2], p[4]]
        else:
            p[0] = [p[2]]
    else:
        p[0] = []

## opcion para tener array de dos dimensiones o dejarlo en una
def p_vars_simple_arr2(p):
    '''vars_simple_arr2 : LEFTKEY CTEI RIGHTKEY
                        | empty'''
    if len(p) == 4:
        p[0] = p[2]

##
## declaracion de vars complejas
def p_vars_complex(p):
    '''vars_complex : type_complex vars_complex_dec '''
    p[0] = (p[1], p[2])

def p_vars_complex_dec(p):
    '''vars_complex_dec : ID vars_complex_more '''
    if p[2]:
        if type(p[2]) is list:
            p[0] = p[2].append(p[1])
        else:
            p[0] = [p[2], p[1]]
    else:
        p[0] = p[1]


def p_vars_complex_more(p):
    '''vars_complex_more : COMMA vars_complex_dec
                        | empty'''
    if len(p) == 3:
        p[0] = p[2]


## tipos simples
def p_type_simple(p):
    '''type_simple : INT
            | FLOAT
            | CHAR'''
    p[0] = p[1]
            
## tipos complejos           
def p_type_complex(p):
    '''type_complex : FILE
            | ID'''
    p[0] = p[1]
            

            
            

##
##          DECLARACION DE FUNCIONES
##

def p_dec_fun(p):
    '''dec_fun : fun
                | empty'''
    if p[1]:
        p[0] = p[1]

def p_fun(p):
    '''fun : FUN fun_type ID LEFTPAREN param_pos RIGHTPAREN LEFTBRACKET dec_block RETURN dec_exp_method SEMICOLON RIGHTBRACKET'''
    p[0] = (p[2], p[3], p[4])

def p_param_pos(p):
    '''param_pos : param
                | empty'''

def p_param(p):
    '''param : type_simple ID param_more'''

def p_param_more(p):
    '''param_more : COMMA param
                | empty'''

def p_fun_type(p):
    '''fun_type : type_simple
                | VOID'''




## 
##          DECLARACION DE BLOQUE Y ESTATUTOS
##

def p_dec_block(p):
    '''dec_block : block
                | empty'''

def p_block(p):
    '''block : statement block_more'''

def p_block_more(p):
    '''block_more : block
                    | empty'''

def p_statement(p):
    '''statement : dec_assign
                        | dec_call
                        | dec_read
                        | dec_write
                        | dec_condition
                        | dec_cycle
                        | dec_method'''






## 
##          DECLARACION DE EXP
##

def p_dec_exp(p):
    '''dec_exp : dec_exp_s'''
    p[0] = p[1]
    print(p[0])
    cuad.readEXP(p[0])
    print(cuad)
    cuad.clearCache()

    

def p_dec_exp_s(p):
    '''dec_exp_s : dec_term pm_op'''
    #p[0] = str(p[1]) + str(p[2])
    p[0] = p[1] + p[2]
    #cuad.checkPlusMinus()

def p_pm_op(p):
    '''pm_op : PLUS dec_exp_s
                | MINUS dec_exp_s
                | empty'''
    if len(p) == 3:
        #p[0] = str(p[1]) + str(p[2])
        p[0] = [p[1]] + p[2]
        #cuad.addOP(p[1])
    else:
        p[0] = []
    
    

def p_dec_exp_method(p):
    '''dec_exp_method : dec_exp_s
                        | empty'''
    if p[1]:
        p[0] = p[1]
    else:
        p[0] = []
                        
## declaracion de term
def p_dec_term(p):
    '''dec_term : dec_fact md_op'''
    #p[0] = str(p[1]) + str(p[2])
    p[0] = p[1] + p[2]
    #cuad.checkMultDiv()

def p_md_op(p):
    '''md_op : TIMES dec_term
                | DIVIDE dec_term
                | empty'''
    if len(p) == 3:
        #p[0] = str(p[1]) + str(p[2])
        p[0] = [p[1]] + p[2]

        #cuad.addOP(p[1])
    else:
        p[0] = []

## declaracion de factor
def p_dec_fact(p):
    '''dec_fact : var_cte
                | LEFTPAREN h_exp RIGHTPAREN'''
    if len(p) == 2:
        #p[0] = str(p[1])
        p[0] = [str(p[1])]
        #cuad.addVP(p[1])
    else:
        p[0] = ['(', str(p[2]), ')']

## declaracion de hiper expresion             
def p_h_exp(p):
    '''h_exp : s_exp ao_op'''
    #p[0] = str(p[1]) + str(p[2])
    p[0] = p[1] + p[2]


def p_ao_op(p):
    '''ao_op : COMP_AND h_exp
                | COMP_OR h_exp
                | empty'''
    if len(p) == 3:
        #p[0] = str(p[1]) + str(p[2])
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

## DECLARACION DE SUPER EXPRESION
def p_s_exp(p):
    '''s_exp : dec_exp_s comp_op'''
    #p[0] = str(p[1]) + str(p[2])
    p[0] = p[1] + p[2]
    
def p_comp_op(p):
    '''comp_op : COMP_LESS s_exp
                | COMP_GREATER s_exp
                | COMP_EQUAL s_exp
                | COMP_NOTEQUAL s_exp
                | empty'''
    if len(p) == 3:
        #p[0] = str(p[1]) + str(p[2])
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []






##
##          DECLARACION DE CLASSES
##

def p_dec_class(p):
    '''dec_class : CLASS ID dec_inherit LEFTBRACKET PRIVATE COLON dec_vars dec_fun PUBLIC COLON dec_vars dec_fun RIGHTBRACKET SEMICOLON
                    | empty'''

def p_dec_inherit(p):
    '''dec_inherit : COLON INHERIT ID
                    | empty'''







##
##          DECLARACION DE ASIGNACION
##


def p_dec_assign(p):
    '''dec_assign : var_id COMP_EQUAL dec_exp SEMICOLON'''

def p_dec_call(p):
    '''dec_call : fun_id LEFTPAREN call_pos RIGHTPAREN SEMICOLON'''
    
def p_call_pos(p):
    '''call_pos : call
                | empty'''

def p_call(p):
    '''call : dec_exp call_more'''

def p_call_more(p):
    '''call_more : COMMA call
                | empty'''
    
    




##
##          DECLARACION DE LECTURA
##


def p_dec_read(p):
    '''dec_read : INCO LEFTPAREN ID RIGHTPAREN SEMICOLON'''

def p_dec_write(p):
    '''dec_write : OUTCO LEFTPAREN write RIGHTPAREN SEMICOLON'''

def p_write(p):
    '''write : dec_exp write_more
            | var_cte write_more'''

def p_write_more(p):
    '''write_more : COMMA write 
                | empty'''

## declaracion condicion
def p_dec_condition(p):
    '''dec_condition : IF LEFTPAREN dec_exp RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET dec_else'''

def p_dec_else(p):
    '''dec_else : ELSE LEFTBRACKET dec_block RIGHTBRACKET
                | empty'''

## declaracion while
def p_dec_cycle(p):
    '''dec_cycle : WHILE LEFTPAREN dec_exp RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET'''

## llamada metodo
def p_dec_method(p):
    '''dec_method : ID DOT ID LEFTPAREN dec_exp_method RIGHTPAREN SEMICOLON'''



def p_var_cte(p):
    '''var_cte : var_id
               | CTEI
               | CTEF
               | SIGN'''
    p[0] = p[1]

def p_var_id(p):
    '''var_id : ID'''
    p[0] = p[1]
    if table.checkVar(p[1]) == -1:
        print("Error: Variable", p[1], "no definida")

def p_fun_id(p):
    '''fun_id : ID'''
    p[0] = p[1]
    #if table.checkVar(p[1]) == -1:
    #    print("Error: Variable", p[1], "no definida")


# Error rule for syntax errors
def p_error(p):
    # raise Exception("Syntax error in input! - {} ".format(p))
    print("Error de sintaxis! - {} ".format(p))


def p_empty(p):
    '''empty :'''
    pass


import sys
import ply.yacc as yacc

from lexer import tokens

yacc.yacc()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            dat = yacc.parse(data)
            print(dat)
            
            if dat == "COMPILED":
                print("Compilado")
        except EOFError:
            print(EOFError)
    else:
        print("No hay archivo")