import sys
sys.path.append('../')
sys.setrecursionlimit(3000)
from analizador.error import error
from analizador.Arbol import Nodo

reservadas = [
    'NOTHING','INT64','FLOAT64','BOOL','CHAR','STRING',
    'LOG10','LOG','SIN','COS','TAN','SQRT', 'PRINT', 'PRINTLN',
    'TRUE', 'FALSE', 'PARSE', 'TRUNC', 'FLOAT','STRINGF','TYPEOF', 
    'IF', 'ELSE', 'WHILE', 'FOR', 'BREAK', 'RETURN', 'CONTINUE', 'END', 'IN',
    'STRUCT', 'MUTABLE', 'FUNCTION', 'LENGTH', 'POP', 'PUSH', 'LIST',
    'ELSEIF', 'LOWERCASE', 'UPPERCASE', 'GLOBAL'
]

esc = ['nothing','Int64','Float64','Bool','Char','String',
    'log10','log','sin','cos','tan','sqrt', 'print', 'println',
    'true', 'false', 'parse', 'trunc', 'float','string','typeof', 
    'if', 'else', 'while', 'for', 'break', 'return', 'continue', 'end', 'in',
    'struct', 'mutable', 'function', 'length', 'pop', 'push', 'List', 'elseif',
    'lowercase', 'uppercase', 'global']

tokens  = reservadas + [
    'COMENTL', 'COMENTML',
    'MAS','MENOS','POR','DIVIDIDO','POTENCIA','MODULO', 'IGUAL',
    'MENOR', 'MAYOR',
    'AND', 'OR', 'NOT',
    'DECIMAL','ENTERO','CADENA','CHAR_CADENA',
    'PTCOMA', 'COMA', 'PT','DOSPT','PARIZQ','PARDER','CORIZQ','CORDER',
    'ID'
]

t_NOTHING   = r'nothing'
t_INT64     = r'Int64'
t_FLOAT64   = r'Float64'
t_BOOL      = r'Bool'
t_CHAR      = r'Char'
t_PARSE    = r'parse'
t_TRUNC    = r'trunc'
t_FLOAT    = r'float'
t_STRINGF    = r'string'
t_TYPEOF    = r'typeof'
t_STRING    = r'String'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_POTENCIA  = r'\^'
t_MODULO    = r'%'
t_IGUAL     = r'='
t_MENOR     = r'<'
t_MAYOR     = r'>'
t_PTCOMA    = r';'
t_COMA      = r','
t_PT        = r'\.'
t_DOSPT     = r':'
t_LOG10     = r'log10'
t_LOG       = r'log'
t_SIN       = r'sin'
t_COS       = r'cos'
t_TAN       = r'tan'
t_SQRT      = r'sqrt'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'\!'
t_TRUE      = r'true'
t_FALSE     = r'false'
t_IF        = r'if'
t_ELSE      = r'else'
t_WHILE     = r'while'
t_FOR       = r'for'
t_BREAK     = r'break'
t_RETURN    = r'return'
t_CONTINUE  = r'continue'
t_PRINT     = r'print'
t_PRINTLN   = r'println'
t_END       = r'end'
t_IN        = r'in'
t_MUTABLE   = r'mutable'
t_FUNCTION  = r'function'
t_LENGTH    = r'length'
t_POP       = r'pop'
t_PUSH      = r'push'
t_STRUCT    = r'struct'
t_LIST      = r'List'
t_ELSEIF    = r'elseif'
t_GLOBAL    = r'global'


def t_COMENTML(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTL(t):
    r'\#[\n]?[^\n]*'
    t.lexer.lineno += t.value.count('\n')



def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'"[^"\n]*"'
    try:
        t.value = (t.value[1:-1])
    except:
        t.value = ""
    return t

def t_CHAR_CADENA(t):
    r'\'[^\'\n]\''
    return t

def t_ID(t):
    r'[_A-Za-z]\w*'
    if t.value in esc:
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t

    
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    str_err = "Caracter ilegal: %s"%(t.value[0])
    t.lexer.skip(1)


from expresiones.expresiones import *
from instrucciones.instrucciones import *
import ply.lex as lex
lexer = lex.lex()

funciones = {}
structs = {}

precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','MENOR','MAYOR','IGUAL', 'NOT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','POTENCIA','MODULO'), 
    ('right','UMENOS'),
    )

def get_column(texto, linea_str, l):
    try:
        if(l > len(linea_str.split("\n"))):
            l = 0
        linea= linea_str.split("\n")[l-1]
    except Exception as e:
        print('\x1b[6;30;42m' + str(l) + '\x1b[0m')
        return 0
    return linea.find(str(texto))+1

# Definición de la gramática
def p_instrucciones(t):
    '''instrucciones    : instruccion PTCOMA instrucciones'''
    nodopt = Nodo('PTCOMA', [])
    nodo = Nodo('instrucciones', [  t[1][1], nodopt, t[3][1] ])
    t[0] =   [t[1][0]]
    t[0] =   [    t[0] + t[3][0]   , nodo  ]
  
def p_instrucciones1(t):
    '''instrucciones    : instruccion instrucciones'''
    nodo = Nodo('instrucciones', [  t[1][1], t[2][1] ])
    t[0] =   [t[1][0]]
    t[0] =   [    t[0] + t[2][0]   ,  nodo ]

def p_instrucciones_instruccion(t):
    '''instrucciones : instruccion PTCOMA
                     | instruccion'''
    nodo = Nodo('instrucciones', [  t[1][1]])
    try:
        if t[2] != "":
            nodopt = Nodo('PTCOMA', [])
            nodo.insertar(nodopt)
    except:
        pass
    l = [] 
    l.append(t[1][0])
    t[0] =  [ l ,   nodo]


def p_instruccion(t):
    '''instruccion  :   asignacion
                    |   asignacion_global
                    |   asignacion_array
                    |   asignacion_posicion_array
                    |   instruccion_if END
                    |   instruccion_while END
                    |   instruccion_break
                    |   instruccion_continue
                    |   instruccion_for END
                    |   instruccion_print
                    |   definicion_struct END
                    |   asignacion_prop_struct
                    |   definicion_funcion END
                    |   llamada_funcion_struct
                    |   instruccion_return
                    |   instruccion_push
                    |   instruccion_pop
                    |   instruccion_global'''
    nodo = Nodo('instruccion', [  t[1][1]  ])
    try:
        if t[2] != "":
            nodoend = Nodo('END', [])
            nodo.insertar(nodoend)
    except:
        pass

    t[0] =   [    t[1][0]  ,   nodo]

# ASIGNACION
def p_asignacion(t):
    '''asignacion  :   ID IGUAL expresion'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)

    nodo1 = Nodo(t[1], [])
    nodo2 = Nodo(t[2], [])
    nodo = Nodo('asignacion', [ nodo1, nodo2, t[3][1] ])

    t[0] =   [    asignacion(t[1], t[3][0], line, col) ,  nodo ]

def p_asignacion_global(t):
    '''asignacion_global  :   GLOBAL ID IGUAL expresion'''
    line = t.lexer.lineno
    col = get_column(t[2], lexer.lexdata, line)

    nodo1 = Nodo(t[1], [])
    nodo2 = Nodo(t[2], [])
    nodo3 = Nodo(t[3], [])
    nodo = Nodo('asignacion_global', [ nodo1, nodo2, nodo3, t[4][1] ])

    t[0] =   [    asignacion(t[2], t[4][0], line, col) ,  nodo ]


#ARRAYS

def p_asignacion_array(t):
    '''asignacion_array :   ID IGUAL expresion_array'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)  

    nodo1 = Nodo(t[1], [])
    nodo2 = Nodo(t[2], [])
    nodo = Nodo('asignacion_array', [ nodo1, nodo2, t[3][1] ])
    t[0] =   [    asignacion_array(t[1], t[3][0], line, col)   ,  nodo ]

def p_asignacion_posicion_array(t):
    '''asignacion_posicion_array  :   ID lista_acceso_posicion IGUAL expresion'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    nodo1 = Nodo("ID", [])
    nodo3 = Nodo(t[3], [])

    t[0] =   [    asignacion_array_posicion(t[1], t[2][0], t[4][0], line, col) , Nodo("asignacion_posicion_array", [nodo1, t[2][1], nodo3, t[4][1]])  ]
    
def p_asignacion_posicion_array_igual_array(t):
    '''asignacion_posicion_array  :   ID lista_acceso_posicion IGUAL expresion_array'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)  

    nodo1 = Nodo("ID", [])
    nodo3 = Nodo(t[3], [])

    t[0] =   [    asignacion_array_posicion(t[1], t[2][0], t[4][0], line, col),Nodo("asignacion_posicion_array", [nodo1, t[2][1],nodo3,t[4][1]  ])   ]

def p_expresion_array(t):
    '''expresion_array  :   CORIZQ lista_expresiones CORDER
                        |   CORIZQ empty CORDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)  
    nodo1 = Nodo(t[1], [])
    nodo3 = Nodo(t[3], [])
    if t[2] == None:
        t[0] =   [    expresion_array([], line, col), Nodo("expresion_array", [nodo1, t[2][1], nodo3,])  ]
    else:
        t[0] =   [    expresion_array(t[2][0], line, col)  ,  Nodo("expresion_array", [nodo1, t[2][1], nodo3,]) ]
        

def p_instruccion_push(t):
    '''instruccion_push :   PUSH NOT PARIZQ ID COMA expresion PARDER
                        |   PUSH NOT PARIZQ ID COMA expresion_array PARDER
                        |   PUSH NOT PARIZQ expresion_array COMA expresion PARDER
                        |   PUSH NOT PARIZQ expresion_array COMA expresion_array PARDER
                        |   PUSH NOT PARIZQ expresion COMA expresion_array PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line) 
    nodo1 = Nodo(t[1], [])
    nodo2 = Nodo(t[2], []) 
    nodo3 = Nodo(t[3], [])  
    nodo5 = Nodo(t[5], [])
    nodo7 = Nodo(t[7], [])
    nodo4 = Nodo(t[4], [])
    nodo = Nodo("instruccion_push", [nodo1,nodo2, nodo3, nodo4, nodo5, t[6][1], nodo7  ])
    if isinstance(t[4],str) == False:
        nodo = Nodo("instruccion_push", [nodo1,nodo2, nodo3, t[4][1], nodo5, t[6][1], nodo7  ])
        t[0] =   [    instruccion_push(t[4][0], t[6][0], line, col)   ,  nodo ]
    else:
        t[0] =   [    instruccion_push(t[4], t[6][0], line, col)   ,  nodo ]

def p_instruccion_pop(t):
    '''instruccion_pop  :   POP NOT PARIZQ ID PARDER
                        |   POP NOT PARIZQ expresion_array PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)  
    nodo1 = Nodo(t[1], [])
    nodo2 = Nodo(t[2], [])
    nodo3 = Nodo(t[3], [])
    nodo5 = Nodo(t[5], [])
    if isinstance(t[4], str):
        nodo4 = Nodo(t[4], [])
        nodo = Nodo("instruccion_pop",[ nodo1, nodo2, nodo3,nodo4,nodo5])
        t[0] =   [    instruccion_pop(t[4], line, col)  , nodo  ]
    else:
        nodo = Nodo("instruccion_pop",[ nodo1, nodo2, nodo3, t[4][1], nodo5])
        t[0] =   [    instruccion_pop(t[4][0], line, col)  , nodo  ]
    

# ACCESO A POSICIOM ARRAY
def p_expresion_acceso_array(t):
    '''expresion_acceso_array   :   ID lista_acceso_posicion'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    nodo1 = Nodo(t[1]) 
    t[0] =   [    expresion_acceso_array(t[1], t[2][0], line, col) , Nodo("expresion_acceso_array", [nodo1,t[2][1]])  ]

def p_lista_acceso_array(t):
    '''lista_acceso_posicion    :   CORIZQ expresion CORDER lista_acceso_posicion'''
    nodo1 = Nodo(t[1])
    nodo3 = Nodo(t[3])
    t[0] =   [t[2][0]]
    t[0] =   [    t[0] + t[4][0]   ,  Nodo("lista_acceso_posicion", [nodo1, t[2][1], nodo3, t[4][1]]) ]

def p_lista_acceso_array1(t):
    '''lista_acceso_posicion    :   CORIZQ expresion CORDER'''
    l =   []
    l.append(t[2][0])
    nodo1 = Nodo(t[1])
    nodo3 = Nodo(t[3])
    t[0] = [l, Nodo("lista_acceso_posicion", [nodo1, t[2][1], nodo3])]

def p_lista_expresiones(t):
    '''lista_expresiones    :   expresion COMA lista_expresiones'''
    nodo2 = Nodo(t[2])
    t[0] =   [t[1][0]]
    t[0] =   [    t[0] + t[3][0]   , Nodo("lista_expresiones", [t[1][1], nodo2, t[3][1]])  ]

def p_lista_expresiones1(t):
    '''lista_expresiones    :   expresion_array COMA lista_expresiones'''
    nodo2 = Nodo(t[2])
    t[0] =   [t[1][0]]
    t[0] =   [    t[0] + t[3][0]   , Nodo("lista_expresiones", [t[1][1], nodo2, t[3][1] ])  ]

def p_lista_expresiones_unica(t):
    '''lista_expresiones    :   expresion
                            |   expresion_array'''
    l =  []
    l.append(t[1][0])
    t[0] = [l, Nodo("lista_expresiones", [t[1][1]])]

def p_expresion_primitiva(t):
    '''expresion_primitiva  : ENTERO
                            | DECIMAL
                            | CADENA
                            | CHAR_CADENA
                            | TRUE
                            | FALSE'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    nodo1 = Nodo(t[1], [])
    t[0] =   [    expresion_primitiva(t[1], line, col)  ,  Nodo("expresion_primitiva", [   nodo1     ])  ]

# ACCESO RANGE ARRAY

def p_expresion_acceso_array_range(t):
    '''expresion_accesos_array_range    :   ID CORIZQ expresion_range CORDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    nodo4 = Nodo(t[4])
    t[0] =   [    expression_array_range(t[1], t[3][0],line, col)  , Nodo("expresion_accesos_array_range", [n1, n2, t[3][1], nodo4])  ]

# EXPRESIONES
def p_expresion(t):
    '''expresion    :   tipo_expresion definicion_tipo''' 
    line = t.lexer.lineno
    col = get_column(t[1][0], lexer.lexdata, line)
    if isinstance(t[1][0], dict ):
        t[0] =   [    t[1][0]  ,   Nodo("expresion", [ t[1][1], t[2][1] ])]
    else:
        t[0] =   [    validar_tipo_expresion(t[1][0], t[2][0], line, col) ,  Nodo("expresion", [ t[1][1], t[2][1] ]) ]


def p_tipo_expresion(t):
    '''tipo_expresion   :   expresion_primitiva
                        |   expresion_id
                        |   expresion_binaria
                        |   expresion_binaria_Log
                        |   expresion_parentesis
                        |   expresion_unaria
                        |   expresion_nativa
                        |   expresion_acceso_array
                        |   expresion_acceso_struct
                        |   llamada_funcion_struct
                        |   expresion_nothing
                        |   expresion_accesos_array_range
                        |   instruccion_push
                        |   instruccion_pop'''    
    t[0] =   [    t[1][0]  ,   Nodo("tipo_expresion", [ t[1][1] ])  ]

def p_definicion_tipo(t):
    '''definicion_tipo  :   DOSPT DOSPT tipo
                        |   empty'''
    
    if t[1][0] is None:
        nodo1 = Nodo("empty", [])
        t[0] =   [    t[1][0]  ,  Nodo("definicion_tipo", [ nodo1 ])  ]
              
    else:
        nodo1 = Nodo("DOSPT", [])
        nodo2 = Nodo("DOSPT", [])
        t[0] =   [    t[3][0]  , Nodo("definicion_tipo", [ nodo1, nodo2, t[3][1] ])  ] 

def p_definicion_tipo_struct(t):
    '''definicion_tipo  :   DOSPT DOSPT ID'''
    
    n1 = Nodo(t[1],[])
    n2 = Nodo(t[2],[])
    n3 = Nodo(t[3],[])
    t[0] =   [    None ,  Nodo("definicion_tipo", [ n1,n2,n3 ])  ]


def p_expresion_id(t):
    '''expresion_id  : ID'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)

    t[0] =   [    expresion_id(t[1], line, col) , Nodo("expresion_id", [Nodo(t[1])])  ]

def p_expresion_binaria(t):
    '''expresion_binaria    :   expresion MAS expresion
                            |   expresion MENOS expresion
                            |   expresion POR expresion
                            |   expresion DIVIDIDO expresion
                            |   expresion POTENCIA expresion
                            |   expresion MODULO expresion
                            |   expresion MENOR expresion
                            |   expresion MAYOR expresion
                            |   expresion AND expresion
                            |   expresion OR expresion'''
    line = t.lexer.lineno
    col = get_column(t[2], lexer.lexdata, line)
    n2 = Nodo(t[2])
    t[0] =   [    expresion_binaria(t[1][0], t[2], t[3][0], line,col) , Nodo("expresion_binaria", [t[1][1], n2, t[3][1]])  ]

def p_expresion_binaria_Log(t):
    '''expresion_binaria_Log        :   expresion MENOR IGUAL expresion
                                    |   expresion MAYOR IGUAL expresion
                                    |   expresion IGUAL IGUAL expresion
                                    |   expresion NOT IGUAL expresion'''
    line = t.lexer.lineno
    col = get_column(t[2], lexer.lexdata, line)
    n2  = Nodo(t[2])
    n3 = Nodo(t[3])
    t[0] =   [    expresion_binaria(t[1][0], t[2]+t[3], t[4][0], line, col)   ,  Nodo("expresion_binaria_Log", [t[1][1], n2, n3, t[4][1]]) ]

def p_expresion_parentesis(t):
    '''expresion_parentesis :   PARIZQ expresion PARDER'''
    n1 = Nodo(t[1])
    n3 = Nodo(t[3])
    t[0] =   [    t[2][0]  , Nodo("expresion_parentesis", [n1, t[2][1], n3]) ]

def p_expresion_unaria(t):
    '''expresion_unaria : MENOS expresion %prec UMENOS'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    expresion_binaria(expresion_primitiva(0, line, col), '-', t[2][0], line, col)    , Nodo("expresion_unaria", [n1, t[2][1]])  ]

def p_expresion_nativa(t):
    '''expresion_nativa :   LOG10 PARIZQ expresion PARDER
                        |   SIN PARIZQ expresion PARDER
                        |   COS PARIZQ expresion PARDER
                        |   TAN PARIZQ expresion PARDER
                        |   SQRT PARIZQ expresion PARDER
                        |   FLOAT PARIZQ expresion PARDER
                        |   STRING PARIZQ expresion PARDER
                        |   TYPEOF PARIZQ expresion PARDER
                        |   LENGTH PARIZQ expresion PARDER
                        |   LENGTH PARIZQ expresion_array PARDER
                        |   TRUNC PARIZQ expresion PARDER
                        |   LOWERCASE PARIZQ expresion PARDER
                        |   UPPERCASE PARIZQ expresion PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    t[0] =   [    expresion_nativa(t[1], t[3][0], line, col)   , Nodo("expresion_nativa", [n1,n2,t[3][1],n4])  ]
    
def p_expresion_nativa_parametros(t):
    '''expresion_nativa :   LOG PARIZQ expresion COMA expresion PARDER
                        |   PARSE PARIZQ tipo COMA expresion PARDER
                        |   TRUNC PARIZQ tipo COMA expresion PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    n6 = Nodo(t[6])
    t[0] =   [    expresion_nativa_log(t[1],t[3][0], t[5][0], line, col)  , Nodo("expresion_nativa", [n1,n2,t[3][1],n4,t[5][1],n6])  ]

def p_expresion_range(t):
    '''expresion_range  :   expresion DOSPT expresion
                        |   tipo_expresion DOSPT tipo_expresion'''
    n2 = Nodo(t[2])
    line = t.lexer.lineno
    col = get_column(t[2], lexer.lexdata, line)
    t[0] =   [    expresion_range(t[1][0],t[3][0], line, col) , Nodo("expresion_range", [t[1][1],n2,t[3][1]])  ]

def p_expresion_nothing(t):
    '''expresion_nothing : NOTHING'''
    t[0] =   [    expresion_nothing()   ,  Nodo("NOTHING", []) ]

## INSTRUCCIONES

# INSTRUCCION IF
def p_instruccion_if(t):
    '''instruccion_if   :   IF expresion empty instrucciones empty'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], None, [], line, col)   , Nodo("instruccion_if", [n1, t[2][1],t[4][1] ])   ]

def p_instruccion_elseif_b(t):
    '''instruccion_elseif   :   ELSEIF expresion empty instrucciones empty'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], None, [], line, col)   , Nodo("instruccion_elseif", [n1, t[2][1],t[4][1] ])  ]

def p_instruccion_elseif(t):
    '''instruccion_elseif   :   ELSEIF expresion empty instrucciones empty ELSE empty instrucciones empty'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n6 = Nodo(t[6])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], None, t[8][0], line, col) , Nodo("instruccion_elseif", [n1, t[2][1],t[4][1], n6, t[8][1] ])  ]

def p_instruccion_elseif_c(t):
    '''instruccion_elseif   :   ELSEIF expresion empty instrucciones empty instruccion_elseif'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], t[6][0], [], line, col)   , Nodo("instruccion_elseif", [n1, t[2][1],t[4][1],t[6][1] ])  ]

def p_instruccion_if_else(t):
    '''instruccion_if   :   IF expresion empty instrucciones empty ELSE empty instrucciones empty'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n6 = Nodo(t[6])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], None, t[8][0], line, col) , Nodo("instruccion_if", [n1, t[2][1],t[4][1], n6, t[8][1] ])  ]

def p_bloque_elseif(t):
    '''instruccion_if    :   IF expresion empty instrucciones empty instruccion_elseif '''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_if(t[2][0], t[4][0], t[6][0], [], line, col)   , Nodo("instruccion_if", [n1, t[2][1],t[4][1], t[6][1] ])  ]

# INSTRUCCION WHILE
def p_while(t):
    '''instruccion_while    :   WHILE expresion instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_while(t[2][0], t[3][0],line, col)   , Nodo("instruccion_while", [n1, t[2][1], t[3][1]])  ]

# INSTRUCCION FOR
def p_for_range(t):
    '''instruccion_for  :   FOR ID IN expresion_range instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])

    t[0] =   [    instruccion_for(t[2], t[4][0], t[5][0], 'range', line, col) ,  Nodo("instruccion_for", [n1,n2,n3, t[4][1], t[5][1]]) ]

def p_for_string(t): 
    '''instruccion_for  :   FOR ID IN expresion instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    t[0] =   [    instruccion_for(t[2], t[4][0], t[5][0], "expresion", line, col) , Nodo("instruccion_for", [n1,n2,n3, t[4][1], t[5][1]])  ]

def p_for_array(t):
    '''instruccion_for  :   FOR ID IN expresion_array instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    t[0] =   [    instruccion_for(t[2], t[4][0], t[5][0], "array", line, col) , Nodo("instruccion_for", [n1,n2,n3, t[4][1], t[5][1]])  ]

# INSTRUCCION BREAK
def p_break(t):
    '''instruccion_break : BREAK '''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_break(line, col)  ,  Nodo("instruccion_break", [n1]) ]

# INSTRUCCION CONTINUE
def p_continue(t):
    '''instruccion_continue : CONTINUE '''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_continue(line, col)   , Nodo("instruccion_continue", [n1])  ]

# INSTRUCCION PRINT
def p_print_lista_expresiones(t):
    '''instruccion_print    :   tipo_print PARIZQ lista_expresiones PARDER'''
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    t[0] =   [    instruccion_print(t[3][0], t[1][0]) ,  Nodo("instruccion_print", [t[1][1], n2, t[3][1], n4 ]) ]

# INSTRUCCION PRINT
def p_print_lista_expresiones_vacio(t):
    '''instruccion_print    :   tipo_print PARIZQ empty PARDER'''
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    t[0] =   [    instruccion_print([], t[1][0])   ,  Nodo("instruccion_print", [t[1][1], n2, t[3][1], n4 ]) ]

def p_tipo_print(t):
    '''tipo_print   :   PRINTLN
                    |   PRINT'''
    n1 = Nodo(t[1])
    t[0] =   [    t[1]  ,  Nodo("tipo_print", [n1]) ]

# TIPOS
def p_tipo(t):
    '''tipo :   INT64
            |   FLOAT64
            |   BOOL
            |   CHAR
            |   STRING
            |   LIST'''
    nodo = Nodo(t[1], [])
    t[0] =   [    t[1]  ,  nodo ]

# STRUCT
def p_definicion_struct(t):
    '''definicion_struct    :   tipo_struct STRUCT ID parametros_struct'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    t[0] =   [    definicion_struct(t[1][0], t[3], t[4][0], line, col)    , Nodo("definicion_struct", [t[1][1], n2, n3, t[4][1]])  ]
    structs[t[3]] = len(t[4][0])

def p_parametros_struct(t):
    '''parametros_struct :  param_struct PTCOMA parametros_struct'''
    n2 = Nodo(t[2])
    t[0] =   [t[1][0]]
    t[0] =   [    t[0] + t[3][0]   ,  Nodo("parametros_struct", [t[1][1], n2,t[3][1]]) ]

def p_parametros_struct_unico(t):
    '''parametros_struct : param_struct PTCOMA'''
    n2 = Nodo(t[2])
    t[0] =   []
    t[0].append(t[1][0])
    t[0] = [t[0], Nodo("parametros_struct", [t[1][1],n2])]

def p_param_struc_tipo(t):
    '''param_struct : ID definicion_tipo'''
    n1 = Nodo(t[1])
    t[0] =   [    [t[1], t[2][0]]  , Nodo("param_struct", [n1, t[2][1]])  ]

def p_tipo_struct(t):
    '''tipo_struct  :   MUTABLE
                    |   empty'''
    if t[1][0] is None:
        t[0] =   [    t[1][0]  ,  Nodo("tipo_struct", [t[1][1]]) ]
    else:
        t[0] =   [    t[1]  ,  Nodo("tipo_struct", [Nodo(t[1], [])]) ]
        
# EXPRESION ACCESO STRUCT

def p_expresion_acceso_struct(t):
    '''expresion_acceso_struct  :   ID lista_acceso_struct'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    expresion_acceso_struct(t[1], t[2][0], line, col)    , Nodo("expresion_acceso_struct", [n1, t[2][1]])  ]

def p_lista_acceso_struct(t):
    '''lista_acceso_struct  : PT ID lista_acceso_struct'''
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    t[0] =   [t[2]]
    t[0] =   [    t[0] + t[3][0]   ,  Nodo("lista_acceso_struct", [n1, n2, t[3][1]]) ]

def p_lista_acceso_struct1(t):
    '''lista_acceso_struct  : PT ID'''
    t[0] =   []
    t[0].append(t[2])
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    t[0] = [t[0], Nodo("lista_acceso_struct", [n1, n2])]

# ASIGNACION PROP STRUCT

def p_asignacion_prop_struct(t):
    '''asignacion_prop_struct   :   ID PT ID IGUAL expresion'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    n4 = Nodo(t[4])
    t[0] =   [    asignacion_prop_struct(t[1], t[3], t[5][0], line, col)   , Nodo("asignacion_prop_struct", [n1, n2, n3, n4, t[5][1]])  ]
    
def p_asignacion_prop_struct_array(t):
    '''asignacion_prop_struct   :   ID PT ID IGUAL expresion_array'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    n4 = Nodo(t[4])
    t[0] =   [    asignacion_prop_struct(t[1], t[3], t[5][0], line, col)   ,  Nodo("asignacion_prop_struct", [n1, n2, n3, n4, t[5][1]]) ]

# DEFINICION FUNCION
def p_definicion_funcion(t):
    '''definicion_funcion   :   FUNCTION ID PARIZQ parametros_funcion PARDER instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    n5 = Nodo(t[5])
    t[0] =   [     definicion_funcion(t[2], t[4][0], t[6][0], line, col)  , Nodo("definicion_funcion", [n1, n2, n3, t[4][1], n5,t[6][1]])  ]
    funciones[t[2]] = len(t[4][0])

# DEFINICION FUNCION SIN PARAMETROS
def p_definicion_funcion_noParam(t):
    '''definicion_funcion   :   FUNCTION ID PARIZQ empty PARDER instrucciones'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n3 = Nodo(t[3])
    n5 = Nodo(t[5])
    t[0] =   [     definicion_funcion(t[2], [], t[6][0], line, col)    , Nodo("definicion_funcion", [n1, n2, n3, n5,t[6][1]])  ]
    funciones[t[2]] = 0

# LISTA PARAMETROS
def p_lista_identicadores(t):
    '''parametros_funcion  :   param_func COMA parametros_funcion'''
    n2 = Nodo(t[2])
    t[0] =   [t[1][0]] 
    t[0] =   [    t[0] + t[3][0]   ,  Nodo("parametros_funcion", [t[1][1],n2,t[3][1]]) ]

def p_lista_identicadores_unico(t):
    '''parametros_funcion : param_func '''
    t[0] =   []
    t[0].append(t[1][0])
    t[0] = [t[0], Nodo("parametros_funcion", [t[1][1]])]

def p_param_func(t):
    '''param_func   :   ID definicion_tipo'''
    n1 = Nodo(t[1])
    t[0] =   [    [t[1], t[2][0]]  , Nodo("param_func", [n1, t[2][1]])  ]

# LLAMADA FUNCION O STRUCT CON PARAMETROS
def p_asignacion_funcion_struct(t):
    '''llamada_funcion_struct    :   ID PARIZQ lista_expresiones PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    if t.lexer.lexdata.find(("function " + t[1])) != -1:
        t[0] =   [    instruccion_llamada_funcion(t[1], t[3][0], line, col)    ,  Nodo("llamada_funcion_struct", [n1,n2,t[3][1],n4]) ]
    elif t.lexer.lexdata.find(("struct " + t[1])) != -1:
        t[0] =   [    instruccion_construir_struct(t[1], t[3][0], line, col)   ,  Nodo("llamada_funcion_struct", [n1,n2,t[3][1],n4]) ]

# LLAMADA FUNCION O STRUCT SIN PARAMETROS
def p_asignacion_funcion_struct_vacio(t):
    '''llamada_funcion_struct    :   ID PARIZQ empty PARDER'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    n4 = Nodo(t[4])
    if(t[1] in funciones.keys()):
        t[0] =   [    instruccion_llamada_funcion(t[1], [], line, col)  ,  Nodo("llamada_funcion_struct", [n1,n2,n4]) ]
    elif (t[1] in structs.keys()):
        t[0] =   [    {"id_struct": t[1], 'parametros': []} ,  Nodo("llamada_funcion_struct", [n1,n2,n4]) ]

def p_instruccion_return(t):
    '''instruccion_return   :   RETURN expresion
                            |   RETURN expresion_array'''
    line = t.lexer.lineno
    col = get_column(t[1], lexer.lexdata, line)
    n1 = Nodo(t[1])
    t[0] =   [    instruccion_return(t[2][0], line, col)   , Nodo("llamada_funcion_struct", [n1,t[2][1]])  ]

def p_instruccion_global(t):
    '''instruccion_global   : GLOBAL ID'''
    n1 = Nodo(t[1])
    n2 = Nodo(t[2])
    t[0] =   [    instruccion_global() , Nodo("llamada_funcion_struct", [n1,n2])  ]

def p_empty(t):
     'empty :'
     
     t[0] =  [    None  ,  Nodo("empty", []) ]

def p_error(p):
     # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    error("sintaxis: '%s'"%(p.value),"syntax error", p.lineno)
    print('Syntax error in input! Parser State: {} | {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))


import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    global lexer
    lexer = lex.lex()
    return parser.parse(input)