# TPC6 - GIC (Gramática Independente de Contexto)

# 2024-03-15

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

## Objetivo

Construir uma gramática GIC (Gramática Independente do Contexto) simples para os seguintes exemplos:

```
? a
b = a * 2 / ( 27 - 3 )
! a + b
c = ( a * b ) / ( a / b )
```

## Resolução

```
T = {VAR, NUM, '+', '-', '*', '/', '=', '(', ')', '?', '!'}

N = {S, Expression, Expression2, Expression3, Operation, Operation2}

S = S

P = {
    S -> '?' VAR                         LA = {'?'}
       | '!' Expression                   LA = {'!'}
       | VAR '=' Expression               LA = {VAR}

    Expression -> Expression2 Operation

    Operation -> '+' Expression               LA = {'+'}
        | '-' Expression                  LA = {'-'}
        | &                              LA = {$, ')'} 
    
    Expression2 -> Expression3 Operation2      LA = {'(', VAR, NUM}

    Operation2 -> '*' Expression              LA = {'*'}
         | '/' Expression                 LA = {'/'}
         | &                             LA = {'+', '-', $, ')'}

    Expression3 -> '(' Expression ')'      LA = {'('}
           | VAR                         LA = {VAR}
           | NUM                         LA = {NUM}
}
```

## Conclusão

A criação de uma Gramática Independente do Contexto (GIC) para os exemplos fornecidos demonstrou como definir uma gramática que reconhece e analisa expressões aritméticas e comandos específicos.
