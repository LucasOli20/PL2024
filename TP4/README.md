# TPC4 - Analisador léxico SQL

# 2024-03-01

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

## Objetivo

Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do género:

```
Select id, nome, salario From empregados Where salario >= 820
```

## Resolução

Neste tpc utilizou-se <u>expressões regulares</u> para analisar o texto de entrada, como também um analisador léxico `(lexer)` para uma linguagem de query simples, utilizando o módulo `ply.lex` em Python. O lexer é capaz de identificar e categorizar tokens em frases como a proposta no [objetivo](#objetivo).

### Estrutura

Para a realização do mesmo é necessário importar o módulo, como mostrado a seguir:

```
import ply.lex as lex
```

#### **Definição dos Tokens**

Os tokens são definidos da seguinte maneira:

```python
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
```

#### **Expressões Regulares para os Tokens**

Os padrões de expressões regulares são definidos para cada token. Estes padrões determinam como cada token deve ser identificador na string de input.

- **Tokens de Símbolos e Operadores**:
Para operadores e símbolos:
```python
t_SEPARADOR = r"\,|\;"
t_LEFTP = r"\("
t_RIGHTP = r"\)"
t_OPERADORES = r">=|<=|=|<|>"
```

- **Tokens de Palavras Reservadas**:
Para as palavras reservadas como  `SELECT`, `FROM`, `WHERE`, `UPDATE` e `DELETE`, são utilizadas as seguintes expressões regulares:
```python
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
```

- **Tokens de Variáveis e Números**:
Para variáveis e números:
```python
def t_NUMBER(t):
    r"\d+"
    return t

def t_VARIAVEL(t):
    r"\w+"
    return t
```


- **Inicialização e Processamento do Lexer**:
O Lexer é inicializado e o input é lido a partir do `stdin`:
```python
lexer = lex.lex()

data = sys.stdin.read()

lexer.input(data)

while tok := lexer.token():
    print(tok)
```

O input é processado e os tokens são escritos um por um até que não haja mais tokens para processar.


## Conclusão

Este tpc implementa um analisador léxico para uma linguagem de query básica, reconhecendo os diversos elementos sintáticos como palavras reservadas, operadores, separadores, variáveis e números. O lexer utiliza o módulo `ply.lex` para analisar e categorizar o input conforme definido pelas expressões regulares. Sendo então este tpc um passo fundamental para a construção de um compilador como lecionado nas aulas de `Processamento de Linguagens`.
