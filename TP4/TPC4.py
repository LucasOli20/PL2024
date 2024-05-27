import re
import sys
import ply.lex as lex

tokens = (
    'SELECT',
    'FROM',
    'WHERE',
    'UPDATE',
    'DELETE',
    'NUMBER',
    'VARIAVEL',
    'OPERADORES',
    'SEPARADOR',
    'LEFTP',
    'RIGHTP'
)

t_SEPARADOR = r"\,|\;"
t_LEFTP = r"\("
t_RIGHTP = r"\)"

def t_SELECT(t):
    r"[Ss][Ee][Ll][Ee][Cc][Tt]"
    return t

def t_FROM(t):
    r"[Ff][Rr][Oo][Mm]"
    return t

def t_WHERE(t):
    r"[Ww][Hh][Ee][Rr][Ee]"
    return t

def t_UPDATE(t):
    r"[Uu][Pp][Dd][Aa][Tt][Ee]"
    return t

def t_DELETE(t):
    r"[Dd][Ee][Ll][Ee][Tt][Ee]"
    return t

def t_NUMBER(t):
    r"\d+"
    return t

def t_OPERADORES(t):
    r">=|<=|=|<|>"
    return t

def t_VARIAVEL(t):
    r"\w+"
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

data = sys.stdin.read()

lexer.input(data)

while tok := lexer.token():
    print(tok)


