import re
import ply.lex as lex

# Define tokens
tokens = ('NUM','STRING','DECL','INIT','END',
          'COMMENT','LISTA','BOOL','TUPLE',
          'PLUS','MINUS','TIMES','DIVIDE',
          'MOD','ID','DEF','EDEF','INST',
          'EINST','REC','EQ','GT','LT',
          'GTE','LTE','AND','OR','NOT',
          'LP','RP')

reserved = {
    'if'    : 'IF',
    'else'  : 'ELSE',
    'then'  : 'THEN'
}

tokens = tokens + tuple(reserved.values()) 

states = (
   ('lang','exclusive'),
   ('func','inclusive'),
   ('inst','inclusive'),
)

t_ANY_COMMENT = r'\-\-'
t_lang_inst_PLUS = r'\+'
t_lang_inst_MINUS = r'-'
t_lang_inst_TIMES = r'\*'
t_lang_inst_DIVIDE = r'/'
t_lang_inst_MOD = r'%'
t_lang_inst_EQ = r'=='
t_lang_inst_GT = r'>'
t_lang_inst_LT = r'<'
t_lang_inst_GTE = r'>='
t_lang_inst_LTE = r'<='
t_lang_inst_AND = r'&&'
t_lang_inst_OR = r'\|\|'
t_lang_inst_NOT = r'!'
t_lang_inst_LP = r'\('
t_lang_inst_RP = r'\)'
t_ANY_ignore = ' \t\n'
t_lang_inst_DECL = r'='

def t_INIT(t):
    r'\"\"\"FPYTHON'
    lexer.push_state("lang")
    t.value = 'INIT'
    return t

def t_lang_END(t):
    r'\"\"\".*'
    lexer.pop_state()
    t.value = 'END'  
    return t

def t_lang_DEF(t):
    r'def\s\w+:'
    lexer.push_state("func")
    t.value = str(t.value)
    return t

def t_func_EDEF(t):
    r'end'
    lexer.pop_state()
    t.value = str(t.value)
    return t

def t_func_INST(t):
    r'.*\s*='
    lexer.push_state("inst")
    t.value = str(t.value)
    return t

def t_inst_EINST(t):
    r'\;'
    lexer.pop_state()
    t.value = str(t.value)
    return t

def t_ANY_NUM(t):
    r'\d+(\.\d*)?([eE][+-]?\d+)?'
    t.value = str(t.value)
    return t

def t_ANY_STRING(t):
    r'"[a-zA-Z_][a-zA-Z0-9_]*"'
    t.value = str(t.value)
    return t

def t_ANY_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = str(t.value)
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_ANY_TUPLE(t):
    r'\((.*,)+\)'
    t.value = str(t.value)
    return t

def t_lang_inst_LISTA(t):
    r'\[.*\]'
    t.value = str(t.value)
    return t

def t_ANY_BOOL(t):
    r'(True)|(False)'
    t.value = str(t.value)
    return t

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


# Test the lexer
#with open("ex3.txt", 'r') as f:
#    content = f.read()

#lexer.input(content)
#for tok in lexer:
#    print(tok)
#    print(lexer.current_state())
