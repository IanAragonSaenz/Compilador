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

























def p_block(p):
    '''block : LEFTBRACKET statement_block RIGHTBRACKET'''


def p_statement_block(p):
    '''statement_block : statement statement_block
                       | empty'''


def p_statement(p):
    '''statement : assignment
                 | condition
                 | writing'''


def p_expression(p):
    '''expression : exp comparation'''


def p_comparation(p):
    '''comparation : COMP_GREATER comparation_exp
                      | COMP_LESS comparation_exp
                      | COMP_NOTEQUAL comparation_exp
                      | empty'''


def p_comparation_exp(p):
    '''comparation_exp : exp'''


def p_exp(p):
    '''exp : term operator'''


def p_operator(p):
    '''operator : PLUS term operator
                | MINUS term operator
                | empty'''


def p_term(p):
    '''term : factor term_operator'''


def p_term_operator(p):
    '''term_operator : TIMES factor term_operator
                     | DIVIDE factor term_operator
                     | empty'''


def p_factor(p):
    '''factor : LEFTPAREN expression RIGHTPAREN
              | sign var_cte'''


def p_op(p):
    '''sign : PLUS
            | MINUS
            | empty'''


def p_var_cte(p):
    '''var_cte : ID
               | CTEI
               | CTEF'''


def p_assignment(p):
    '''assignment : ID COMP_EQUAL expression SEMICOLON'''


def p_condition(p):
    '''condition : IF LEFTPAREN expression RIGHTPAREN block else_condition SEMICOLON'''


def p_else_condition(p):
    '''else_condition : ELSE block
                      | empty'''


def p_writing(p):
    '''writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON'''


def p_print_val(p):
    '''print_val : expression print_exp
                 | CTESTRING print_exp'''


def p_print_exp(p):
    '''print_exp : COMMA  print_val
                 | empty'''


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