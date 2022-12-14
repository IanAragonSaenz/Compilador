
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASSIGN BOOL CHAR CHAR_DEC CLASS COLON COMMA COMP_AND COMP_EQUAL COMP_GREATER COMP_LESS COMP_NOTEQUAL COMP_OR CTEF CTEI DIVIDE DOT ELSE FALSE FILE FLOAT FUN ID IF INCO INHERIT INT LEFTBRACKET LEFTKEY LEFTPAREN MAIN MINUS OUTCO PLUS PRIVATE PROGRAM PUBLIC RETURN RIGHTBRACKET RIGHTKEY RIGHTPAREN SEMICOLON SIGN TIMES TRUE VAR VOID WHILEprogram : PROGRAM ID SEMICOLON dec_vars_mult dec_fun dec_class MAIN LEFTPAREN RIGHTPAREN LEFTBRACKET dec_vars_mult dec_block RIGHTBRACKETdec_vars_mult : dec_vars_idk\n                | emptydec_vars_idk : dec_vars dec_vars_moredec_vars_more : dec_vars_idk\n                    | emptydec_vars : VAR vars SEMICOLONvars : vars_simple \n            | vars_complexvars_simple : type_simple vars_simple_dec vars_simple_dec : vars_simple_id vars_simple_morevars_simple_more : COMMA vars_simple_dec\n                        | emptyvars_simple_id : ID vars_simple_arrvars_simple_arr : LEFTKEY CTEI RIGHTKEY vars_simple_arr2\n                        | emptyvars_simple_arr2 : LEFTKEY CTEI RIGHTKEY\n                        | emptyvars_complex : type_complex vars_complex_dec vars_complex_dec : ID vars_complex_more vars_complex_more : COMMA vars_complex_dec\n                        | emptytype_simple : INT\n            | FLOAT\n            | CHAR\n            | BOOLtype_complex : FILE\n            | IDdec_fun : dec_fun_idk\n                | emptydec_fun_idk : fun dec_fun_moredec_fun_more : dec_fun_idk\n                    | emptyfun : FUN fun_type fun_id LEFTPAREN param_pos RIGHTPAREN LEFTBRACKET dec_vars_mult dec_block RIGHTBRACKETparam_pos : param\n                | emptyparam : type_simple ID param_moreparam_more : COMMA param\n                | emptyfun_type : type_simple\n                | VOIDfun_return : RETURN dec_exp_method SEMICOLONdec_block : block\n                | emptyblock : statement block_moreblock_more : block\n                    | emptystatement : dec_assign\n                        | dec_call\n                        | dec_read\n                        | dec_write\n                        | dec_condition\n                        | dec_cycle\n                        | dec_method\n                        | fun_returndec_exp : dec_exp_sdec_exp_s : dec_term pm_oppm_op : PLUS dec_exp_s\n                | MINUS dec_exp_s\n                | emptydec_exp_method : dec_exp_s\n                        | emptydec_exp_method_call : dec_exp_method dec_exp_method_moredec_exp_method_more : COMMA dec_exp_method_call\n                            | emptydec_term : dec_fact md_opmd_op : TIMES dec_term\n                | DIVIDE dec_term\n                | emptydec_fact : var_cte\n                | LEFTPAREN hyper_call RIGHTPARENhyper_call : h_exph_exp : s_exp ao_opao_op : COMP_AND h_exp\n                | COMP_OR h_exp\n                | emptys_exp : dec_exp_s comp_opcomp_op : COMP_LESS dec_exp_s\n                | COMP_GREATER dec_exp_s\n                | COMP_EQUAL dec_exp_s\n                | COMP_NOTEQUAL dec_exp_s\n                | emptydec_class : dec_class_idk\n                    | emptydec_class_idk : class_body dec_class_moredec_class_more : dec_class_idk\n                    | emptyclass_body : CLASS ID dec_inherit LEFTBRACKET PRIVATE COLON dec_vars_mult dec_fun PUBLIC COLON dec_vars_mult dec_fun RIGHTBRACKET SEMICOLONdec_inherit : COLON INHERIT ID\n                    | emptydec_assign : var_id ASSIGN hyper_call SEMICOLONdec_call : ID LEFTPAREN call_pos RIGHTPAREN SEMICOLONdec_call_exp : ID LEFTPAREN call_pos RIGHTPARENcall_pos : call\n                | emptycall : hyper_call call_morecall_more : COMMA call\n                | emptydec_read : INCO LEFTPAREN var_id RIGHTPAREN SEMICOLONdec_write : OUTCO LEFTPAREN write RIGHTPAREN SEMICOLONwrite : print_sign write_morewrite_more : COMMA write \n                | emptydec_condition : IF LEFTPAREN hyper_call RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET dec_elsedec_else : ELSE LEFTBRACKET dec_block RIGHTBRACKET\n                | emptydec_cycle : WHILE LEFTPAREN hyper_call RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKETdec_method : ID DOT ID LEFTPAREN dec_exp_method_call RIGHTPARENvar_cte : var_id\n                | dec_call_exp\n                | var_const\n                | dec_methodvar_const : cte_num\n               | CHAR_DEC\n               | TRUE\n               | FALSEcte_num : CTEF\n               | CTEI\n               | MINUS CTEI\n                | MINUS CTEFprint_sign : hyper_call\n                | SIGNvar_id : ID\n                | ID LEFTKEY dec_exp RIGHTKEY\n                | ID LEFTKEY dec_exp RIGHTKEY LEFTKEY dec_exp RIGHTKEYfun_id : IDempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,119,],[0,-1,]),'ID':([2,6,7,8,9,15,16,17,21,22,23,24,25,26,27,28,33,37,38,39,40,54,60,72,76,78,86,88,97,98,99,100,101,102,103,104,105,111,113,116,117,118,123,124,125,126,127,134,168,170,171,174,175,178,185,188,189,192,193,194,195,197,199,203,214,224,225,226,228,229,232,234,242,243,245,247,249,251,],[3,-2,-3,-127,28,-4,-5,-6,43,45,-23,-24,-25,-26,-27,-28,50,52,-40,-41,-7,43,45,80,82,-127,93,-127,93,-48,-49,-50,-51,-52,-53,-54,-55,139,93,139,156,139,139,161,139,139,139,139,-42,139,139,139,139,139,139,139,139,139,139,139,139,139,-91,139,-92,139,-99,-100,93,93,-108,139,-127,-107,-104,-106,93,-105,]),'SEMICOLON':([3,18,19,20,41,42,43,44,45,53,55,56,58,59,61,67,69,77,84,85,111,115,128,129,130,131,132,133,135,136,137,138,139,140,141,142,143,144,145,153,154,155,159,169,172,173,176,179,180,183,187,190,191,196,198,200,201,207,208,209,210,211,216,217,218,219,220,221,230,232,241,244,],[4,40,-8,-9,-10,-127,-127,-19,-127,-11,-13,-14,-16,-20,-22,-12,-21,-127,-15,-18,-127,-17,168,-61,-62,-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,-72,-127,-127,199,-57,-60,-66,-69,-119,-120,214,-73,-76,-77,-82,-124,225,226,-58,-59,-67,-68,-71,-74,-75,-78,-79,-80,-81,-93,-108,-125,248,]),'FUN':([4,5,6,7,8,13,15,16,17,40,87,112,182,213,231,],[-127,14,-2,-3,-127,14,-4,-5,-6,-7,-127,14,-34,-127,14,]),'CLASS':([4,5,6,7,8,10,11,12,13,15,16,17,32,34,35,36,40,182,248,],[-127,-127,-2,-3,-127,33,-29,-30,-127,-4,-5,-6,33,-31,-32,-33,-7,-34,-88,]),'MAIN':([4,5,6,7,8,10,11,12,13,15,16,17,29,30,31,32,34,35,36,40,47,48,49,182,248,],[-127,-127,-2,-3,-127,-127,-29,-30,-127,-4,-5,-6,46,-83,-84,-127,-31,-32,-33,-7,-85,-86,-87,-34,-88,]),'VAR':([4,8,40,78,87,88,213,],[9,9,-7,9,9,9,9,]),'INCO':([6,7,8,15,16,17,40,78,86,88,97,98,99,100,101,102,103,104,105,113,168,199,214,225,226,228,229,232,242,243,245,247,249,251,],[-2,-3,-127,-4,-5,-6,-7,-127,107,-127,107,-48,-49,-50,-51,-52,-53,-54,-55,107,-42,-91,-92,-99,-100,107,107,-108,-127,-107,-104,-106,107,-105,]),'OUTCO':([6,7,8,15,16,17,40,78,86,88,97,98,99,100,101,102,103,104,105,113,168,199,214,225,226,228,229,232,242,243,245,247,249,251,],[-2,-3,-127,-4,-5,-6,-7,-127,108,-127,108,-48,-49,-50,-51,-52,-53,-54,-55,108,-42,-91,-92,-99,-100,108,108,-108,-127,-107,-104,-106,108,-105,]),'IF':([6,7,8,15,16,17,40,78,86,88,97,98,99,100,101,102,103,104,105,113,168,199,214,225,226,228,229,232,242,243,245,247,249,251,],[-2,-3,-127,-4,-5,-6,-7,-127,109,-127,109,-48,-49,-50,-51,-52,-53,-54,-55,109,-42,-91,-92,-99,-100,109,109,-108,-127,-107,-104,-106,109,-105,]),'WHILE':([6,7,8,15,16,17,40,78,86,88,97,98,99,100,101,102,103,104,105,113,168,199,214,225,226,228,229,232,242,243,245,247,249,251,],[-2,-3,-127,-4,-5,-6,-7,-127,110,-127,110,-48,-49,-50,-51,-52,-53,-54,-55,110,-42,-91,-92,-99,-100,110,110,-108,-127,-107,-104,-106,110,-105,]),'RETURN':([6,7,8,15,16,17,40,78,86,88,97,98,99,100,101,102,103,104,105,113,168,199,214,225,226,228,229,232,242,243,245,247,249,251,],[-2,-3,-127,-4,-5,-6,-7,-127,111,-127,111,-48,-49,-50,-51,-52,-53,-54,-55,111,-42,-91,-92,-99,-100,111,111,-108,-127,-107,-104,-106,111,-105,]),'RIGHTBRACKET':([6,7,8,11,12,13,15,16,17,34,35,36,40,78,86,88,94,95,96,97,98,99,100,101,102,103,104,105,113,120,121,122,148,168,182,199,213,214,225,226,228,229,231,232,237,238,239,242,243,245,247,249,250,251,],[-2,-3,-127,-29,-30,-127,-4,-5,-6,-31,-32,-33,-7,-127,-127,-127,119,-43,-44,-127,-48,-49,-50,-51,-52,-53,-54,-55,-127,-45,-46,-47,182,-42,-34,-91,-127,-92,-99,-100,-127,-127,-127,-108,242,243,244,-127,-107,-104,-106,-127,251,-105,]),'PUBLIC':([6,7,8,11,12,13,15,16,17,34,35,36,40,87,112,147,182,],[-2,-3,-127,-29,-30,-127,-4,-5,-6,-31,-32,-33,-7,-127,-127,181,-34,]),'INT':([9,14,66,90,],[23,23,23,23,]),'FLOAT':([9,14,66,90,],[24,24,24,24,]),'CHAR':([9,14,66,90,],[25,25,25,25,]),'BOOL':([9,14,66,90,],[26,26,26,26,]),'FILE':([9,],[27,]),'VOID':([14,],[39,]),'COMMA':([42,43,45,56,58,77,82,84,85,115,129,130,131,132,133,135,136,137,138,139,140,141,142,143,144,145,152,153,154,155,163,164,165,169,172,173,176,179,180,187,190,191,196,197,198,207,208,209,210,211,216,217,218,219,220,221,223,230,232,234,241,],[54,-127,60,-14,-16,-127,90,-15,-18,-17,-61,-62,-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,185,-72,-127,-127,203,-121,-122,-57,-60,-66,-69,-119,-120,-73,-76,-77,-82,-127,-124,-58,-59,-67,-68,-71,-74,-75,-78,-79,-80,-81,234,-93,-108,-127,-125,]),'LEFTKEY':([43,77,93,139,161,198,],[57,83,118,118,118,224,]),'LEFTPAREN':([46,51,52,93,107,108,109,110,111,116,118,123,125,126,127,134,139,156,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[62,66,-126,116,124,125,126,127,134,134,134,134,134,134,134,134,178,197,134,134,134,134,134,134,134,134,134,134,134,134,134,134,134,134,]),'COLON':([50,79,181,],[64,87,213,]),'LEFTBRACKET':([50,63,65,70,80,81,205,206,246,],[-127,71,-90,78,-89,88,228,229,249,]),'CTEI':([57,83,111,116,118,123,125,126,127,134,146,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[68,92,145,145,145,145,145,145,145,145,179,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,]),'RIGHTPAREN':([62,66,73,74,75,82,89,91,114,116,129,130,131,132,133,135,136,137,138,139,140,141,142,143,144,145,149,150,151,152,153,154,155,160,161,162,163,164,165,166,167,169,172,173,176,177,178,179,180,184,186,187,190,191,196,197,198,202,204,207,208,209,210,211,212,215,216,217,218,219,220,221,222,223,227,230,232,233,234,235,240,241,],[70,-127,81,-35,-36,-127,-37,-39,-38,-127,-61,-62,-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,183,-94,-95,-127,-72,-127,-127,200,-123,201,-127,-121,-122,205,206,-57,-60,-66,-69,211,-127,-119,-120,-96,-98,-73,-76,-77,-82,-127,-124,-101,-103,-58,-59,-67,-68,-71,230,-97,-74,-75,-78,-79,-80,-81,232,-127,-102,-93,-108,-63,-127,-65,-64,-125,]),'INHERIT':([64,],[72,]),'RIGHTKEY':([68,92,131,132,133,135,136,137,138,139,140,141,142,143,144,145,157,158,169,172,173,176,179,180,198,207,208,209,210,211,230,232,236,241,],[77,115,-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,198,-56,-57,-60,-66,-69,-119,-120,-124,-58,-59,-67,-68,-71,-93,-108,241,-125,]),'PRIVATE':([71,],[79,]),'DOT':([93,139,],[117,117,]),'ASSIGN':([93,106,198,241,],[-123,123,-124,-125,]),'CHAR_DEC':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,141,]),'TRUE':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,]),'FALSE':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,143,]),'CTEF':([111,116,118,123,125,126,127,134,146,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[144,144,144,144,144,144,144,144,180,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,]),'MINUS':([111,116,118,123,125,126,127,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,170,171,173,174,175,176,178,179,180,185,188,189,192,193,194,195,197,198,203,209,210,211,224,230,232,234,241,],[146,146,146,146,146,146,146,171,-127,-70,146,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,146,146,-66,146,146,-69,146,-119,-120,146,146,146,146,146,146,146,146,-124,146,-67,-68,-71,146,-93,-108,146,-125,]),'SIGN':([125,203,],[165,165,]),'PLUS':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,173,176,179,180,198,209,210,211,230,232,241,],[170,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,-66,-69,-119,-120,-124,-67,-68,-71,-93,-108,-125,]),'COMP_LESS':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,155,169,172,173,176,179,180,198,207,208,209,210,211,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,192,-57,-60,-66,-69,-119,-120,-124,-58,-59,-67,-68,-71,-93,-108,-125,]),'COMP_GREATER':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,155,169,172,173,176,179,180,198,207,208,209,210,211,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,193,-57,-60,-66,-69,-119,-120,-124,-58,-59,-67,-68,-71,-93,-108,-125,]),'COMP_EQUAL':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,155,169,172,173,176,179,180,198,207,208,209,210,211,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,194,-57,-60,-66,-69,-119,-120,-124,-58,-59,-67,-68,-71,-93,-108,-125,]),'COMP_NOTEQUAL':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,155,169,172,173,176,179,180,198,207,208,209,210,211,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,195,-57,-60,-66,-69,-119,-120,-124,-58,-59,-67,-68,-71,-93,-108,-125,]),'COMP_AND':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,154,155,169,172,173,176,179,180,191,196,198,207,208,209,210,211,218,219,220,221,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,188,-127,-57,-60,-66,-69,-119,-120,-77,-82,-124,-58,-59,-67,-68,-71,-78,-79,-80,-81,-93,-108,-125,]),'COMP_OR':([131,132,133,135,136,137,138,139,140,141,142,143,144,145,154,155,169,172,173,176,179,180,191,196,198,207,208,209,210,211,218,219,220,221,230,232,241,],[-127,-127,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,189,-127,-57,-60,-66,-69,-119,-120,-77,-82,-124,-58,-59,-67,-68,-71,-78,-79,-80,-81,-93,-108,-125,]),'TIMES':([132,133,135,136,137,138,139,140,141,142,143,144,145,179,180,198,211,230,232,241,],[174,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,-119,-120,-124,-71,-93,-108,-125,]),'DIVIDE':([132,133,135,136,137,138,139,140,141,142,143,144,145,179,180,198,211,230,232,241,],[175,-70,-109,-110,-111,-112,-123,-113,-114,-115,-116,-117,-118,-119,-120,-124,-71,-93,-108,-125,]),'ELSE':([242,],[246,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'dec_vars_mult':([4,78,87,88,213,],[5,86,112,113,231,]),'dec_vars_idk':([4,8,78,87,88,213,],[6,16,6,6,6,6,]),'empty':([4,5,8,10,13,32,42,43,45,50,66,77,78,82,86,87,88,97,111,112,113,116,131,132,152,154,155,163,178,197,213,223,228,229,231,234,242,249,],[7,12,17,31,36,49,55,58,61,65,75,85,7,91,96,7,7,122,130,12,96,151,172,176,186,190,196,204,151,130,7,235,96,96,12,130,247,96,]),'dec_vars':([4,8,78,87,88,213,],[8,8,8,8,8,8,]),'dec_fun':([5,112,231,],[10,147,239,]),'dec_fun_idk':([5,13,112,231,],[11,35,11,11,]),'fun':([5,13,112,231,],[13,13,13,13,]),'dec_vars_more':([8,],[15,]),'vars':([9,],[18,]),'vars_simple':([9,],[19,]),'vars_complex':([9,],[20,]),'type_simple':([9,14,66,90,],[21,38,76,76,]),'type_complex':([9,],[22,]),'dec_class':([10,],[29,]),'dec_class_idk':([10,32,],[30,48,]),'class_body':([10,32,],[32,32,]),'dec_fun_more':([13,],[34,]),'fun_type':([14,],[37,]),'vars_simple_dec':([21,54,],[41,67,]),'vars_simple_id':([21,54,],[42,42,]),'vars_complex_dec':([22,60,],[44,69,]),'dec_class_more':([32,],[47,]),'fun_id':([37,],[51,]),'vars_simple_more':([42,],[53,]),'vars_simple_arr':([43,],[56,]),'vars_complex_more':([45,],[59,]),'dec_inherit':([50,],[63,]),'param_pos':([66,],[73,]),'param':([66,90,],[74,114,]),'vars_simple_arr2':([77,],[84,]),'param_more':([82,],[89,]),'dec_block':([86,113,228,229,249,],[94,148,237,238,250,]),'block':([86,97,113,228,229,249,],[95,121,95,95,95,95,]),'statement':([86,97,113,228,229,249,],[97,97,97,97,97,97,]),'dec_assign':([86,97,113,228,229,249,],[98,98,98,98,98,98,]),'dec_call':([86,97,113,228,229,249,],[99,99,99,99,99,99,]),'dec_read':([86,97,113,228,229,249,],[100,100,100,100,100,100,]),'dec_write':([86,97,113,228,229,249,],[101,101,101,101,101,101,]),'dec_condition':([86,97,113,228,229,249,],[102,102,102,102,102,102,]),'dec_cycle':([86,97,113,228,229,249,],[103,103,103,103,103,103,]),'dec_method':([86,97,111,113,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,228,229,234,249,],[104,104,138,104,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,138,104,104,138,104,]),'fun_return':([86,97,113,228,229,249,],[105,105,105,105,105,105,]),'var_id':([86,97,111,113,116,118,123,124,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,228,229,234,249,],[106,106,135,106,135,135,135,160,135,135,135,135,135,135,135,135,135,135,135,135,135,135,135,135,135,135,135,106,106,135,106,]),'block_more':([97,],[120,]),'dec_exp_method':([111,197,234,],[128,223,223,]),'dec_exp_s':([111,116,118,123,125,126,127,134,170,171,178,185,188,189,192,193,194,195,197,203,224,234,],[129,155,158,155,155,155,155,155,207,208,155,155,155,155,218,219,220,221,129,155,158,129,]),'dec_term':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[131,131,131,131,131,131,131,131,131,131,209,210,131,131,131,131,131,131,131,131,131,131,131,131,]),'dec_fact':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,132,]),'var_cte':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,]),'dec_call_exp':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,136,]),'var_const':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,]),'cte_num':([111,116,118,123,125,126,127,134,170,171,174,175,178,185,188,189,192,193,194,195,197,203,224,234,],[140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,]),'call_pos':([116,178,],[149,212,]),'call':([116,178,185,],[150,150,215,]),'hyper_call':([116,123,125,126,127,134,178,185,203,],[152,159,164,166,167,177,152,152,164,]),'h_exp':([116,123,125,126,127,134,178,185,188,189,203,],[153,153,153,153,153,153,153,153,216,217,153,]),'s_exp':([116,123,125,126,127,134,178,185,188,189,203,],[154,154,154,154,154,154,154,154,154,154,154,]),'dec_exp':([118,224,],[157,236,]),'write':([125,203,],[162,227,]),'print_sign':([125,203,],[163,163,]),'pm_op':([131,],[169,]),'md_op':([132,],[173,]),'call_more':([152,],[184,]),'ao_op':([154,],[187,]),'comp_op':([155,],[191,]),'write_more':([163,],[202,]),'dec_exp_method_call':([197,234,],[222,240,]),'dec_exp_method_more':([223,],[233,]),'dec_else':([242,],[245,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID SEMICOLON dec_vars_mult dec_fun dec_class MAIN LEFTPAREN RIGHTPAREN LEFTBRACKET dec_vars_mult dec_block RIGHTBRACKET','program',13,'p_program','parser.py',15),
  ('dec_vars_mult -> dec_vars_idk','dec_vars_mult',1,'p_dec_vars_mult','parser.py',51),
  ('dec_vars_mult -> empty','dec_vars_mult',1,'p_dec_vars_mult','parser.py',52),
  ('dec_vars_idk -> dec_vars dec_vars_more','dec_vars_idk',2,'p_dec_vars_idk','parser.py',57),
  ('dec_vars_more -> dec_vars_idk','dec_vars_more',1,'p_dec_vars_more','parser.py',66),
  ('dec_vars_more -> empty','dec_vars_more',1,'p_dec_vars_more','parser.py',67),
  ('dec_vars -> VAR vars SEMICOLON','dec_vars',3,'p_dec_vars','parser.py',72),
  ('vars -> vars_simple','vars',1,'p_vars','parser.py',79),
  ('vars -> vars_complex','vars',1,'p_vars','parser.py',80),
  ('vars_simple -> type_simple vars_simple_dec','vars_simple',2,'p_vars_simple','parser.py',85),
  ('vars_simple_dec -> vars_simple_id vars_simple_more','vars_simple_dec',2,'p_vars_simple_dec','parser.py',90),
  ('vars_simple_more -> COMMA vars_simple_dec','vars_simple_more',2,'p_vars_simple_more','parser.py',104),
  ('vars_simple_more -> empty','vars_simple_more',1,'p_vars_simple_more','parser.py',105),
  ('vars_simple_id -> ID vars_simple_arr','vars_simple_id',2,'p_vars_simple_id','parser.py',111),
  ('vars_simple_arr -> LEFTKEY CTEI RIGHTKEY vars_simple_arr2','vars_simple_arr',4,'p_vars_simple_arr','parser.py',116),
  ('vars_simple_arr -> empty','vars_simple_arr',1,'p_vars_simple_arr','parser.py',117),
  ('vars_simple_arr2 -> LEFTKEY CTEI RIGHTKEY','vars_simple_arr2',3,'p_vars_simple_arr2','parser.py',126),
  ('vars_simple_arr2 -> empty','vars_simple_arr2',1,'p_vars_simple_arr2','parser.py',127),
  ('vars_complex -> type_complex vars_complex_dec','vars_complex',2,'p_vars_complex','parser.py',134),
  ('vars_complex_dec -> ID vars_complex_more','vars_complex_dec',2,'p_vars_complex_dec','parser.py',138),
  ('vars_complex_more -> COMMA vars_complex_dec','vars_complex_more',2,'p_vars_complex_more','parser.py',151),
  ('vars_complex_more -> empty','vars_complex_more',1,'p_vars_complex_more','parser.py',152),
  ('type_simple -> INT','type_simple',1,'p_type_simple','parser.py',159),
  ('type_simple -> FLOAT','type_simple',1,'p_type_simple','parser.py',160),
  ('type_simple -> CHAR','type_simple',1,'p_type_simple','parser.py',161),
  ('type_simple -> BOOL','type_simple',1,'p_type_simple','parser.py',162),
  ('type_complex -> FILE','type_complex',1,'p_type_complex','parser.py',167),
  ('type_complex -> ID','type_complex',1,'p_type_complex','parser.py',168),
  ('dec_fun -> dec_fun_idk','dec_fun',1,'p_dec_fun','parser.py',180),
  ('dec_fun -> empty','dec_fun',1,'p_dec_fun','parser.py',181),
  ('dec_fun_idk -> fun dec_fun_more','dec_fun_idk',2,'p_dec_fun_idk','parser.py',186),
  ('dec_fun_more -> dec_fun_idk','dec_fun_more',1,'p_dec_fun_more','parser.py',194),
  ('dec_fun_more -> empty','dec_fun_more',1,'p_dec_fun_more','parser.py',195),
  ('fun -> FUN fun_type fun_id LEFTPAREN param_pos RIGHTPAREN LEFTBRACKET dec_vars_mult dec_block RIGHTBRACKET','fun',10,'p_fun','parser.py',200),
  ('param_pos -> param','param_pos',1,'p_param_pos','parser.py',204),
  ('param_pos -> empty','param_pos',1,'p_param_pos','parser.py',205),
  ('param -> type_simple ID param_more','param',3,'p_param','parser.py',210),
  ('param_more -> COMMA param','param_more',2,'p_param_more','parser.py',217),
  ('param_more -> empty','param_more',1,'p_param_more','parser.py',218),
  ('fun_type -> type_simple','fun_type',1,'p_fun_type','parser.py',223),
  ('fun_type -> VOID','fun_type',1,'p_fun_type','parser.py',224),
  ('fun_return -> RETURN dec_exp_method SEMICOLON','fun_return',3,'p_fun_return','parser.py',228),
  ('dec_block -> block','dec_block',1,'p_dec_block','parser.py',239),
  ('dec_block -> empty','dec_block',1,'p_dec_block','parser.py',240),
  ('block -> statement block_more','block',2,'p_block','parser.py',246),
  ('block_more -> block','block_more',1,'p_block_more','parser.py',255),
  ('block_more -> empty','block_more',1,'p_block_more','parser.py',256),
  ('statement -> dec_assign','statement',1,'p_statement','parser.py',261),
  ('statement -> dec_call','statement',1,'p_statement','parser.py',262),
  ('statement -> dec_read','statement',1,'p_statement','parser.py',263),
  ('statement -> dec_write','statement',1,'p_statement','parser.py',264),
  ('statement -> dec_condition','statement',1,'p_statement','parser.py',265),
  ('statement -> dec_cycle','statement',1,'p_statement','parser.py',266),
  ('statement -> dec_method','statement',1,'p_statement','parser.py',267),
  ('statement -> fun_return','statement',1,'p_statement','parser.py',268),
  ('dec_exp -> dec_exp_s','dec_exp',1,'p_dec_exp','parser.py',281),
  ('dec_exp_s -> dec_term pm_op','dec_exp_s',2,'p_dec_exp_s','parser.py',286),
  ('pm_op -> PLUS dec_exp_s','pm_op',2,'p_pm_op','parser.py',290),
  ('pm_op -> MINUS dec_exp_s','pm_op',2,'p_pm_op','parser.py',291),
  ('pm_op -> empty','pm_op',1,'p_pm_op','parser.py',292),
  ('dec_exp_method -> dec_exp_s','dec_exp_method',1,'p_dec_exp_method','parser.py',301),
  ('dec_exp_method -> empty','dec_exp_method',1,'p_dec_exp_method','parser.py',302),
  ('dec_exp_method_call -> dec_exp_method dec_exp_method_more','dec_exp_method_call',2,'p_dec_exp_method_call','parser.py',309),
  ('dec_exp_method_more -> COMMA dec_exp_method_call','dec_exp_method_more',2,'p_dec_exp_method_more','parser.py',316),
  ('dec_exp_method_more -> empty','dec_exp_method_more',1,'p_dec_exp_method_more','parser.py',317),
  ('dec_term -> dec_fact md_op','dec_term',2,'p_dec_term','parser.py',325),
  ('md_op -> TIMES dec_term','md_op',2,'p_md_op','parser.py',329),
  ('md_op -> DIVIDE dec_term','md_op',2,'p_md_op','parser.py',330),
  ('md_op -> empty','md_op',1,'p_md_op','parser.py',331),
  ('dec_fact -> var_cte','dec_fact',1,'p_dec_fact','parser.py',340),
  ('dec_fact -> LEFTPAREN hyper_call RIGHTPAREN','dec_fact',3,'p_dec_fact','parser.py',341),
  ('hyper_call -> h_exp','hyper_call',1,'p_hyper_call','parser.py',351),
  ('h_exp -> s_exp ao_op','h_exp',2,'p_h_exp','parser.py',357),
  ('ao_op -> COMP_AND h_exp','ao_op',2,'p_ao_op','parser.py',361),
  ('ao_op -> COMP_OR h_exp','ao_op',2,'p_ao_op','parser.py',362),
  ('ao_op -> empty','ao_op',1,'p_ao_op','parser.py',363),
  ('s_exp -> dec_exp_s comp_op','s_exp',2,'p_s_exp','parser.py',371),
  ('comp_op -> COMP_LESS dec_exp_s','comp_op',2,'p_comp_op','parser.py',375),
  ('comp_op -> COMP_GREATER dec_exp_s','comp_op',2,'p_comp_op','parser.py',376),
  ('comp_op -> COMP_EQUAL dec_exp_s','comp_op',2,'p_comp_op','parser.py',377),
  ('comp_op -> COMP_NOTEQUAL dec_exp_s','comp_op',2,'p_comp_op','parser.py',378),
  ('comp_op -> empty','comp_op',1,'p_comp_op','parser.py',379),
  ('dec_class -> dec_class_idk','dec_class',1,'p_dec_class','parser.py',392),
  ('dec_class -> empty','dec_class',1,'p_dec_class','parser.py',393),
  ('dec_class_idk -> class_body dec_class_more','dec_class_idk',2,'p_dec_class_idk','parser.py',398),
  ('dec_class_more -> dec_class_idk','dec_class_more',1,'p_dec_class_more','parser.py',406),
  ('dec_class_more -> empty','dec_class_more',1,'p_dec_class_more','parser.py',407),
  ('class_body -> CLASS ID dec_inherit LEFTBRACKET PRIVATE COLON dec_vars_mult dec_fun PUBLIC COLON dec_vars_mult dec_fun RIGHTBRACKET SEMICOLON','class_body',14,'p_class_body','parser.py',412),
  ('dec_inherit -> COLON INHERIT ID','dec_inherit',3,'p_dec_inherit','parser.py',416),
  ('dec_inherit -> empty','dec_inherit',1,'p_dec_inherit','parser.py',417),
  ('dec_assign -> var_id ASSIGN hyper_call SEMICOLON','dec_assign',4,'p_dec_assign','parser.py',433),
  ('dec_call -> ID LEFTPAREN call_pos RIGHTPAREN SEMICOLON','dec_call',5,'p_dec_call','parser.py',436),
  ('dec_call_exp -> ID LEFTPAREN call_pos RIGHTPAREN','dec_call_exp',4,'p_dec_call_exp','parser.py',440),
  ('call_pos -> call','call_pos',1,'p_call_pos','parser.py',444),
  ('call_pos -> empty','call_pos',1,'p_call_pos','parser.py',445),
  ('call -> hyper_call call_more','call',2,'p_call','parser.py',450),
  ('call_more -> COMMA call','call_more',2,'p_call_more','parser.py',458),
  ('call_more -> empty','call_more',1,'p_call_more','parser.py',459),
  ('dec_read -> INCO LEFTPAREN var_id RIGHTPAREN SEMICOLON','dec_read',5,'p_dec_read','parser.py',474),
  ('dec_write -> OUTCO LEFTPAREN write RIGHTPAREN SEMICOLON','dec_write',5,'p_dec_write','parser.py',477),
  ('write -> print_sign write_more','write',2,'p_write','parser.py',481),
  ('write_more -> COMMA write','write_more',2,'p_write_more','parser.py',489),
  ('write_more -> empty','write_more',1,'p_write_more','parser.py',490),
  ('dec_condition -> IF LEFTPAREN hyper_call RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET dec_else','dec_condition',8,'p_dec_condition','parser.py',496),
  ('dec_else -> ELSE LEFTBRACKET dec_block RIGHTBRACKET','dec_else',4,'p_dec_else','parser.py',502),
  ('dec_else -> empty','dec_else',1,'p_dec_else','parser.py',503),
  ('dec_cycle -> WHILE LEFTPAREN hyper_call RIGHTPAREN LEFTBRACKET dec_block RIGHTBRACKET','dec_cycle',7,'p_dec_cycle','parser.py',509),
  ('dec_method -> ID DOT ID LEFTPAREN dec_exp_method_call RIGHTPAREN','dec_method',6,'p_dec_method','parser.py',513),
  ('var_cte -> var_id','var_cte',1,'p_var_cte','parser.py',519),
  ('var_cte -> dec_call_exp','var_cte',1,'p_var_cte','parser.py',520),
  ('var_cte -> var_const','var_cte',1,'p_var_cte','parser.py',521),
  ('var_cte -> dec_method','var_cte',1,'p_var_cte','parser.py',522),
  ('var_const -> cte_num','var_const',1,'p_var_const','parser.py',529),
  ('var_const -> CHAR_DEC','var_const',1,'p_var_const','parser.py',530),
  ('var_const -> TRUE','var_const',1,'p_var_const','parser.py',531),
  ('var_const -> FALSE','var_const',1,'p_var_const','parser.py',532),
  ('cte_num -> CTEF','cte_num',1,'p_cte_num','parser.py',540),
  ('cte_num -> CTEI','cte_num',1,'p_cte_num','parser.py',541),
  ('cte_num -> MINUS CTEI','cte_num',2,'p_cte_num','parser.py',542),
  ('cte_num -> MINUS CTEF','cte_num',2,'p_cte_num','parser.py',543),
  ('print_sign -> hyper_call','print_sign',1,'p_print_sign','parser.py',550),
  ('print_sign -> SIGN','print_sign',1,'p_print_sign','parser.py',551),
  ('var_id -> ID','var_id',1,'p_var_id','parser.py',555),
  ('var_id -> ID LEFTKEY dec_exp RIGHTKEY','var_id',4,'p_var_id','parser.py',556),
  ('var_id -> ID LEFTKEY dec_exp RIGHTKEY LEFTKEY dec_exp RIGHTKEY','var_id',7,'p_var_id','parser.py',557),
  ('fun_id -> ID','fun_id',1,'p_fun_id','parser.py',566),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',576),
]
