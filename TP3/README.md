# TPC3 - Somador ON/OFF

# 2024-02-16

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

## Objetivo

- **Somar sequências de dígitos:** O programa deve identificar e somar todas as sequências de dígitos que encontrar em um texto de entrada.

- **Desligar comportamento de soma ao encontrar `Off`:** Sempre que o programa encontrar a string <u>`Off`</u> em qualquer combinação de maiúsculas e minúsculas, o comportamento de soma das sequências de dígitos deve ser desligado.

- **Ligar comportamento de soma ao encontrar `On`:** Sempre que o programa encontrar a string <u>`On`</u> em qualquer combinação de maiúsculas e minúsculas, o comportamento de soma das sequências de dígitos deve ser novamente ligado.

- **Imprimir resultado ao encontrar `=`:** Sempre que o programa encontrar o caractere <u>`=`</u>, o resultado da soma das sequências de dígitos deve ser exibido no ecrã.

## Resolução

Este script utiliza <u>expressões regulares</u> para analisar o texto de entrada e realizar as ações específicas com base em padrões predefinidos. Ao ler a entrada da linha de comando, processa linha por linha e executa operações de acordo com as regras definidas.


O script realiza os seguintes passos:

1. **Correspondência de Expressão Regular**: Define uma lista de `tuplos`, cada uma contendo um <u>rótulo e um padrão de expressão regular</u>.
2. **Processamento**: Processa cada linha do texto de entrada usando as expressões regulares definidas.
3. **Execução de Ações**: Executa ações com base nos padrões correspondidos, como alternar a flag `soma` ou acumular valores.
4. **Saída**: Imprime o valor acumulado quando encontra o símbolo `'='` na entrada.

## Exemplo

Entrada: `5on10off3`

Saída: `Valor somado: 15`


Neste exemplo, os números são acumulados quando a flag `soma` está como `True` (alternada pelas palavras-chave <u>`on`</u> e <u>`off`</u>) e produz a soma quando encontra o símbolo `=`.
