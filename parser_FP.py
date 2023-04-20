import re
import ply.yacc as yacc
import sys
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIVIDE', 'MOD'),
)

def p_program(p):
    """
    program : init frases end
    """
    p[0] = p[2]

def p_init(p):
    """
    init : INIT
    """
    p[0] = ""

def p_end(p):
    """
    end : END
    """
    p[0] = ""

def p_comments(p):
    """
    comments : COMMENT conteudo
    """
    p[0] = "#" + p[2] + "\n"

def p_frases(p):
    """
    frases : comments
           | decl
           | cond
           | func
           | frases func
           | frases cond
           | frases comments
           | frases decl
    """
    p[0] = "".join(p[1:]) +"\n"

def p_func(p):
    """
    func : DEF insts EDEF
    """
    aux = str(p[1]).split(" ")[1]
    aux = 'f_' + aux[0:]
    aux = aux[:-1] + '(x)' + aux[-1:] + '\n'

    p[0] = 'def ' + aux + p[2] + "\telse:\n\t\traise ValueError\n"

def p_insts(p):
    """
    insts : inst
          | insts inst
    """
    p[0] = "".join(p[1:])

##FALTAM CASOS AQUI
def p_inst(p):
    """
    inst : INST exp EINST
         | INST logic EINST
         | INST cond EINST
         | INST rec EINST
    """
    arg = str(p[1]).replace(" ","").replace("=","")
    if p[2] == 'rec':
        if ':' in arg:
            p[0] = "\tif len(x) >= 1:\nh = x[0]\nt = x[1:]\n" + p[2] +'\n'
        elif '[]' in arg:
            p[0] = "\tif len(x) == 0:\n\t\treturn " + p[2] +'\n'
        else:
            p[0] = "\tif x == "+ arg + ":\n\t\treturn " + p[2] +'\n'
    elif p[2] == 'cond':
        p[0] = "\tif x == "+ arg + ":\n\t\t" + p[2] +'\n'
    elif '[' in arg and len(arg) == 3:
        p[0] = "\tif len(x) == 1:\n\t\t"+arg[1]+" = x[0]"+"\n\t\treturn " + p[2] +'\n'
    else:
        if ':' in arg:
            p[0] = "\tif len(x) >= 1:\n\t\t"+arg[1]+" = x[0]\n\t\t"+arg[3]+" = x[1:]\n\t\treturn" + p[2] +'\n'
        elif '[]' in arg:
            p[0] = "\tif len(x) == 0:\n\t\treturn " + p[2] +'\n'
        else:
            p[0] = "\tif x == "+ arg + ":\n\t\t" + p[2]+'\n'

def p_rec(p):
    """
    rec : exp REC exp
    """
    p[0] = p[1] + "\n\t\treturn " + p[3] + "\n"
    
def p_decl(p):
    """
    decl : exp DECL exp
         | exp DECL logic
    """
    p[0] = p[1] + '=' + p[3] + "\n"

def p_exp(p):
    """
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp MOD exp
        | conteudo
    """
    if len(p) == 4:
        p[0] = "(" + p[1] + str(p[2]) + p[3] + ")"
    else:
        p[0] = p[1]

def p_logic(p):
    """
    logic : exp EQ exp
          | exp GT exp
          | exp LT exp
          | exp GTE exp
          | exp LTE exp
          | exp AND exp
          | exp OR exp
          | NOT logic
    """
    if p[2] == '==' or p[2] == '<' or p[2] == '>' or p[2] == '>=' or p[2] == '<=':
        p[0] = '(' + p[1] + str(p[2]) + p[3] + ')'
    elif p[2] == '&&':
        p[0] = '(' + p[1] +' and '+ p[3] + ')'
    elif p[2] == '||':
        p[0] = '(' + p[1] +' or '+ p[3] + ')'
    elif p[1] == '!':
        p[0] = '(' + 'not ' + p[2] + ')'
    else:
        p[0] = p[1]

def p_cond(p):
    """
    cond : IF logic THEN exp ELSE exp
    """
    print(p)
    p[0] = 'if '+p[2]+':\n\t\t\treturn '+p[4]+ "\n\t\telse"+':\n\t\t\treturn '+p[6]

def p_conteudo(p):
    """
    conteudo : NUM
             | STRING
             | ID
             | BOOL
             | TUPLE
             | lista
             | call
    """
    p[0] = p[1]

def p_call(p):
    """
    call : ID LP exp RP
    """
    p[0] = 'f_'+str(p[1]) + '(' +str(p[3]) +')'

def p_lista(p):
    'lista : LISTA'

    if '<-' in p[1]:
        string = p[1][1:-1] 
        aux = string.split('|')
        instrucao = aux[0].replace(" ","")
        resto = aux[1]
        aux2 = resto.split(',')
        aux3 = aux2[0].replace(" ","").split('<-')
        dominio = aux3[1][1:-1].split("..")
        var = aux3[0].replace(" ","")
        merda = aux2[1:]

        condicoes = ''
        for x in merda:
            condicoes+=' if '+ x.replace(" ","")

        resultado = '['+instrucao+' for '+var+" in range("+dominio[0]+','+dominio[1]+")"+condicoes+']'
        p[0] = resultado

    else: p[0] = p[1]

def p_error(p):
    if p:
        error_info = "Syntax error at token " + str(p.type) + "('" + str(p.value) + "')"
        error_info += " on line " + str(p.lineno) + ", position " + str(p.lexpos)
        print(error_info)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


#UI

print("                                          ")
print(" _____ ______   _______ _   _  ___  _   _ ")
print("|  ___|  _ \ \ / /_   _| | | |/ _ \| \ | |")
print("| |_  | |_) \ V /  | | | |_| | | | |  \| |")
print("|  _| |  __/ | |   | | |  _  | |_| | |\  |")
print("|_|   |_|    |_|   |_| |_| |_|\___/|_| \_|")
print("                                          ")

try:
    fInput = input("Insert the name of the input file: ")
    fread = open(fInput, "r")
except OSError:
        print("[ERROR] File not found!")
        sys.exit()
with fread: 
    input_str = fread.read()
    fOutput = input("Insert the name of the output file: ")
    fwrite = open(str(fOutput), "w")

    begin = input_str[:input_str.find("\"\"\"FPYTHON")]
    end = input_str[input_str.find("\"\"\"")+10:]
    end = end[end.find("\"\"\"")+3:]
    doit = input_str[input_str.find("\"\"\"FPYTHON"):input_str.rfind("\"\"\"")+3]

    result = begin + parser.parse(doit) + end

    fwrite.write(result)
    fwrite.close()
