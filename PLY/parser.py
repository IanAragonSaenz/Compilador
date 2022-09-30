def p_program(p):
    '''program : PROGRAM ID SEMICOLON dec_vars dec_fun dec_class MAIN LEFTPAREN RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET'''
    p[0] = "COMPILED"



##
##          DECLARACION DE VARIABLES
##
def p_dec_vars(p):
    '''dec_vars : vars SEMICOLON 
                | empty'''

## elige entre simple o complejo
def p_vars(p):
    '''vars : vars_simple 
            | vars_complex'''

## se hace vars simple poniendo su tipo y luego la declaracion
def p_vars_simple(p):
    '''vars_simple : type_simple vars_simple_dec '''

## se llama al id para poder poner arrays o no y el more para loopear
def p_vars_simple_dec(p):
    '''vars_simple_dec : vars_simple_id vars_simple_more'''

## Loopea para multiples declaraciones
def p_vars_simple_more(p):
    '''vars_simple_more : COMMA vars_simple_dec'''

## Pone el id y la posibilidad de que sea array
def p_vars_simple_id(p):
    '''vars_simple_id : ID vars_simple_arr'''
    
## opcion para tener array de una dimension
def p_vars_simple_arr(p):
    '''vars_simple_arr : LEFTKEY CTEI RIGHTKEY vars_simple_arr2
                        | empty'''

## opcion para tener array de dos dimensiones o dejarlo en una
def p_vars_simple_arr2(p):
    '''vars_simple_arr2 : LEFTKEY CTEI RIGHTKEY
                        | empty'''

##
## declaracion de vars complejas
def p_vars_complex(p):
    '''vars_complex : type_complex vars_complex_dec '''

def p_vars_complex_dec(p):
    '''vars_complex_dec : ID vars_complex_more '''

def p_vars_complex_more(p):
    '''vars_complex_more : COMMA vars_complex_dec'''

## tipos simples
def p_type_simple(p):
    '''type : INT
            | FLOAT
            | CHAR'''
            
## tipos complejos           
def p_type_complex(p):
    '''type : FILE
            | ID'''
            

            
            

##
##          DECLARACION DE FUNCIONES
##

def p_dec_fun(p):
    '''dec_fun : fun
                | empty'''

def p_fun(p):
    '''fun : FUN fun_type ID LEFTPAREN param_pos RIGHTPAREN LEFTBRACKET dec_block RETURN dec_exp RIGHTBRACKET'''

def p_param_pos(p):
    '''param_pos : param
                | empty'''

def p_param(p):
    '''param : type_simple id param_more'''

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
                        | dec_cycle'''






## 
##          DECLARACION DE EXP
##

def p_dec_exp(p):
    '''dec_exp : dec_term pm_op'''
                
def p_pm_op(p):
    '''pm_op : PLUS dec_exp
                | MINUS dec_term
                | empty'''
                
## declaracion de term
def p_dec_term(p):
    '''dec_term : dec_fact md_op'''
                
def p_md_op(p):
    '''md_op : TIMES dec_term
                | DIVIDE dec_term
                | empty'''

## declaracion de factor
def p_dec_fact(p):
    '''dec_fact : ID
                | LEFTPAREN H_EXP RIGHTPAREN'''

## declaracion de hiper expresion             
def p_H_EXP(p):
    '''p_H_EXP : S_EXP ao_op'''

def p_ao_op(p):
    '''ao_op : COMP_AND H_EXP
                | COMP_OR H_EXP
                | empty'''

## DECLARACION DE SUPER EXPRESION
def p_S_EXP(p):
    '''p_S_EXP : dec_exp comp_op dec_exp'''
    
def p_comp_op(p):
    '''comp_op : COMP_LESS dec_exp
                COMP_GREAT dec_exp
                COMP_EQUAL dec_exp
                COMP_NOTEQUAL dec_exp
                | empty'''






##
##          DECLARACION DE CLASSES
##

def p_dec_class(p):
    '''dec_class : CLASS ID dec_inherit LEFTBRACKET PRIVATE COLON dec_vars dec_fun PUBLIC COLON dec_vars dec_fun RIGHTBRACKET SEMICOLON'''

def p_dec_inherit(p):
    '''dec_inherit : COLON INHERIT ID
                    | empty'''







##
##          DECLARACION DE ASIGNACION
##


def p_dec_assign(p):
    '''dec_assign : ID EQUAL H_EXP'''

def p_dec_call(p):
    '''dec_call : ID LEFTPAREN call_pos RIGHTPAREN SEMICOLON'''
    
def p_call_pos(p):
    '''call_pos : call
                | empty'''

def p_call(p):
    '''call : dec_exp call_more'''

def p_call_more(p):
    '''call_more : COMMA call'''
    
    




##
##          DECLARACION DE LECTURA
##


def p_dec_read(p):
    '''dec_read : INCO LEFTPAREN ID RIGHTPAREN SEMICOLON'''

def p_dec_write(p):
    '''dec_read : LEFTPAREN write RIGHTPAREN SEMICOLON'''

def p_write(p):
    '''write : dec_exp write_more
            | sign write_more'''

def p_write_more(p):
    '''write_more : COMMA write 
                |empty'''


def p_var_cte(p):
    '''var_cte : ID
               | CTEI
               | CTEF'''


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
            if yacc.parse(data) == "COMPILED":
                print("Compilado")
        except EOFError:
            print(EOFError)
    else:
        print("No hay archivo")