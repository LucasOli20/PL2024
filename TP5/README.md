# TPC5 - Simulador de Máquina de Vending

# 2024-03-08

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

## Objetivo

Desenvolver um programa que simule uma máquina de vending.
A máquina tem um stock de produtos: uma lista de triplos, nome do produto, quantidade e preço.
```json
stock = [
 {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
 ...
]
```
A lista persiste num ficheiro em JSON que é carregado no arranque do programa e é atulizado
quando o programa termina.

A seguir apresenta-se um exemplo de uma interação com a máquina, assim que esta é ligada:
```bash
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade |  preço
---------------------------------
A23 água 0.5L 8 0.7
...
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insufuciente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> ...
...
maq: Saldo = 74c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```

## Resolução

Neste tpc foi desenvolvido um programa em Python em que simula uma máquina de Vending. O programa gerencia um stock de produtos, persiste essa informação num ficheiro `JSON`, e interage com o utilizador através de comandos específicos. A máquina permite listar os produtos, inserir moedas, selecionar produtos, verificar o saldo e devolver o troco ao sair.

### Estrutura

Para a realização do mesmo foi necessário importar os módulos, como mostrado a seguir:

```
import ply.lex as lex
import json
import sys
import re
from datetime import date
```

- `ply.lex`: Biblioteca utilizada para análise léxica.
- `json`: Para manipulação de ficheiros JSON, usado para carregar e salvar o stock.
- `sys`: Para interações com o sistema, mas não é utilizado explicitamente neste trecho.
- `re`: Biblioteca de expressões regulares para analisar e processar padrões de texto.
- `date`: Para obter a data atual e imprimir no início do programa.

#### **Definição dos Tokens**

Os tokens representam os diferentes comandos que a máquina pode processar:

```python
tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'SALDO',
    'ADICIONAR'
)
```

- **Inicialização do Lexer e Carregamento do Stock**:

    ```python
    lexer = lex.lex()

    with open("vendingStock.json","r", encoding='UTF-8') as file:
        dadosJson = json.load(file)

        stock = {}

        for item in dadosJson:
            key = item["cod"]
            value = (item['nome'], int(item["quant"]), float(item["preco"]))
            stock[key] = value

    lexer.stock = stock
    lexer.vendON = True
    lexer.saldo = 0

    print(f"maq: {date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    ```

    - Inicializa o lexer.
    - Carrega o stock de um ficheiro `JSON` e armazena-o no lexer.
    - Define o estado inicial da máquina.

#### **Funções de Manipulação de Tokens**

Cada comando tem uma função associada que define a sua expressão regular correspondente e a lógica para manipular esse comando.

- **LISTAR**:
    ```python
    def t_LISTAR(t):
        r"LISTAR"

        print("maq:")

        max_lengths = [len("cod"), len("nome"), len("quantidade"), len("preço")]

        for key, value in lexer.stock.items():
            max_lengths[0] = max(max_lengths[0], len(str(key)))
            max_lengths[1] = max(max_lengths[1], len(str(value[0])))
            max_lengths[2] = max(max_lengths[2], len(str(value[1])))
            max_lengths[3] = max(max_lengths[3], len(str(value[2])))

        format_str = "{:<" + str(max_lengths[0]) + "} | {:<" + str(max_lengths[1]) + "} | {:<" + str(max_lengths[2]) + "} | {:<" + str(max_lengths[3]) + "}"

        print(format_str.format("cod", "nome", "quantidade", "preço"))
        print("-------------------------------------------------------")

        for key, value in lexer.stock.items():
            print(format_str.format(key, value[0], value[1], value[2]))
            print("-------------------------------------------------------")

        return t
    ```

    - `t_LISTAR`: Função para processar o comando LISTAR.
    - Calcula o tamanho máximo de cada coluna para formatação.
    - Imprime os produtos no formato de tabela.

    Resultado:
    ```shell
    cod | nome                    | quantidade | preço
    -------------------------------------------------------
    B12 | Chá Gelado              | 12         | 1.5  
    -------------------------------------------------------
    C45 | Bolachas                | 25         | 1.2  
    -------------------------------------------------------
    D67 | Barra de Twix           | 30         | 1.0  
    -------------------------------------------------------
    E89 | Sumo de Laranja 0.5L    | 10         | 2.0  
    -------------------------------------------------------
    F34 | Crackers                | 20         | 0.8  
    -------------------------------------------------------
    G56 | Sandes de Queijo        | 8          | 2.5  
    -------------------------------------------------------
    H78 | Massa Instantânea       | 6          | 1.7  
    -------------------------------------------------------
    I90 | Banana                  | 11         | 1.1  
    -------------------------------------------------------
    J01 | Mistura de Frutos Secos | 15         | 1.3  
    -------------------------------------------------------
    A33 | Água Mineral 0.5L       | 18         | 0.9  
    -------------------------------------------------------
    D23 | Sandes de Frango        | 7          | 1.5  
    -------------------------------------------------------
    ```

- **Inserir Moedas**:

    ```python
    def t_MOEDA(t):
        r'MOEDA?\s+((1|2)[eE]|(2|5|10|20|50)[cC])((?:\s*,*\s*)((1|2)[eE]|(2|5|10|20|50)[cC]))*'

        values = re.findall(r'\d{1,2}', t.value)
        denominations = re.findall(r'[ec]', t.value)
        pairs = list(zip(values, denominations)) 
        for amount, unit in pairs:
            if unit == 'c':
                t.lexer.saldo += int(amount)
            else:
                t.lexer.saldo += int(amount) * 100

        eur = int(lexer.saldo/100)
        cents = lexer.saldo % 100
        if eur > 0:
            print(f"maq: Saldo = {eur}e{cents}c")
        else:
            print(f"maq: Saldo = {cents}c")
        return t
    ```

    - `t_MOEDA`: Função para processar o comando MOEDA.
    - Utiliza expressões regulares para identificar e calcular o valor total inserido.
    - Atualiza e exibe o saldo.

    Resultado:

    ```shell
    >> MOEDA 1e, 20c, 5c, 5c .
    maq: Saldo = 1e30c
    ```

- **Selecionar Produto**:

    ```python
    def t_SELECIONAR(t):
        r"SELECIONAR\s(.+)"

        encontrado = re.match(r"SELECIONAR\s(?P<codigo>.+)", t.value)
        if encontrado:
            produtoCod = encontrado.group('codigo')
            if produtoCod in lexer.stock.keys():
                nome, quant, preco = lexer.stock[produtoCod]

                preco = preco * 100

                if quant > 0:
                    if lexer.saldo > preco:
                        quant -= 1
                        dados = list(lexer.stock[produtoCod])
                        dados[1] = quant
                        new_dados = tuple(dados)
                        lexer.stock[produtoCod] = new_dados

                        print(f'maq: Pode retirar o produto dispensado "{nome}"')
                        lexer.saldo -= int(preco)
                        eur = int(lexer.saldo/100)
                        cents = lexer.saldo % 100
                        if eur > 0:
                            print(f"maq: Saldo = {eur}e{cents}c")
                        else:
                            print(f"maq: Saldo = {cents}c")
                    else:
                        print("maq: Saldo insufuciente para satisfazer o seu pedido")
                        euros, centimos = divmod(preco,100)
                        eur = int(lexer.saldo/100)
                        cents = lexer.saldo % 100
                        if eur > 0 and euros > 0:
                            print(f"maq: Saldo = {eur}e{cents}c; Pedido = {int(euros)}e{int(centimos)}c")
                        elif eur == 0 and euros > 0:
                            print(f"maq: Saldo = {cents}c; Pedido = {int(euros)}e{int(centimos)}c")
                        else:
                            print(f"maq: Saldo = {cents}c; Pedido = {int(centimos)}c")
                else:
                    print(f"maq: Produto Fora de Stock: {nome}")
                    print("maq: Por favor escolha outro Produto!")
            else:
                print(f'maq: O artigo não existe no Stock!: {produtoCod}.')

        return t
    ```

    - `t_SELECIONAR`: Função para processar o comando SELECIONAR.
    - Verifica se o produto existe e se há saldo suficiente.
    - Atualiza o saldo e a quantidade do produto, ou exibe mensagens de erro apropriadas.

    Resultado:

    ```shell
    >> SELECIONAR I90
    maq: Pode retirar o produto dispensado "Banana"
    maq: Saldo = 20c
    ```


- **Adicionar Produto**:

    ```python
    def t_ADICIONAR(t):
        r'ADICIONAR\s+(.+?)\s*,*\s*"(.+?)"\s*,*\s*(\d+)\s*,*\s*(\d\.*\d*)'

        matched = re.match(r'ADICIONAR\s+(?P<cod>.+?)\s*,*\s*"(?P<nome>.+?)"\s*,*\s*(?P<quantidade>\d+)\s*,*\s*(?P<valor>\d\.*\d*)', t.value)
        codigo = matched.group('cod')

        if codigo not in lexer.stock.keys():
            nome = matched.group('nome')
            quantidade = matched.group('quantidade')
            preco = matched.group('valor')
            lexer.stock[codigo] = (nome, quantidade, preco)
            print(f'maq: Artigo adicionado com Sucesso!: Cod = {codigo}; Nome = "{nome}"; Quantidade = {quantidade}; Preco = {preco}')
        else:
            print(f'maq: Código: {codigo} já existente no sistema.')
            print(f"cod: {codigo}; nome: {lexer.stock[codigo][0]}; quant: {lexer.stock[codigo][1]}; preço: {lexer.stock[codigo][2]}")
            add = input("Introduza quantos quer adicionar à quantidade existente (caso não deseje adicionar introduza 0) >> ")

            while not add.isdigit() or int(add) <= 0:
                print("O input não contém apenas dígitos ou não é um número inteiro ou não é um número positivo")
                add = input("Introduza quantos quer adicionar (caso não deseje adicionar introduza 0) >> ")

            adiciona = int(add)

            dados = list(lexer.stock[codigo])

            dados[1] += adiciona

            new_dados = tuple(dados)

            lexer.stock[codigo] = new_dados

            print(f"maq: Quantidade do Artigo {codigo} incrementado com sucesso!")

        return t
    ```

    - `t_ADICIONAR`: Função para processar o comando ADICIONAR.
    - Adiciona um novo produto ao stock ou incrementa a quantidade de um produto existente.
    - Verifica se o código do produto já existe e solicita a quantidade a ser adicionada.

    Resultado:

    ```shell
    >> ADICIONAR B140, "BANANA", 10, 1.5
    maq: Artigo adicionado com Sucesso!: Cod = B140; Nome = "BANANA"; Quantidade = 10; Preco = 1.5

    maq:
    cod  | nome                    | quantidade | preço
    -------------------------------------------------------
    B12  | Chá Gelado              | 12         | 1.5  
    -------------------------------------------------------
    C45  | Bolachas                | 25         | 1.2  
    -------------------------------------------------------
    D67  | Barra de Twix           | 30         | 1.0  
    -------------------------------------------------------
    E89  | Sumo de Laranja 0.5L    | 10         | 2.0  
    -------------------------------------------------------
    F34  | Crackers                | 20         | 0.8  
    -------------------------------------------------------
    G56  | Sandes de Queijo        | 8          | 2.5  
    -------------------------------------------------------
    H78  | Massa Instantânea       | 6          | 1.7  
    -------------------------------------------------------
    I90  | Banana                  | 10         | 1.1  
    -------------------------------------------------------
    J01  | Mistura de Frutos Secos | 15         | 1.3  
    -------------------------------------------------------
    A33  | Água Mineral 0.5L       | 18         | 0.9  
    -------------------------------------------------------
    D23  | Sandes de Frango        | 7          | 1.5  
    -------------------------------------------------------
    B140 | BANANA                  | 10         | 1.5  
    -------------------------------------------------------
    ```

- **Saldo**:

    ```python
    def t_SALDO(t):
        r"SALDO"
        eur = int(lexer.saldo/100)
        cents = lexer.saldo % 100
        if eur > 0:
            print(f"maq: Saldo = {eur}e{cents}c")
        else:
            print(f"maq: Saldo = {cents}c")
        return t
    ```

    - `t_SALDO`: Função para processar o comando SALDO.
    - Exibe o saldo atual na máquina.

    Resultado:

    ```shell
    >> SALDO
    maq: Saldo = 20c
    ```

- **SAIR**:

    ```python
    def t_SAIR(t):
    r"SAIR"

    if lexer.saldo == 0:
        print("maq: Sem troco para dar")
    else:
        listaDeTrocos = []
        euros = [200, 100]
        centimos = [50, 20, 10, 5]

        for valor in euros:
            quantidade, resto = divmod(lexer.saldo, valor)
            if quantidade != 0:
                listaDeTrocos.append(f"{quantidade}x {valor/100}e")
            lexer.saldo = resto

        for valor in centimos:
            if lexer.saldo == 0:
                break
            quantidade, resto = divmod(lexer.saldo, valor)
            if quantidade != 0:
                listaDeTrocos.append(f"{quantidade}x {valor}c")
            lexer.saldo = resto

        saida = "maq: Pode retirar o troco: "
        for i in range(len(listaDeTrocos)):
            saida += listaDeTrocos[i]
            if i < len(listaDeTrocos) - 2:
                saida += ", "
            elif i < len(listaDeTrocos) - 1:
                saida += " e "
        saida += "."
        print(saida)
    print("maq: Até à próxima")
    lexer.vendON = False
    return t
    ```

    - `t_SAIR`: Função para processar o comando SAIR.
    - Calcula e devolve o troco ao usuário, se houver.
    - Finaliza o programa, definindo vendON como False.

    Resultado:

    ```shell
    >> SAIR
    maq: Pode retirar o troco: 1x 1.0e, 1x 50c, 1x 20c e 1x 10c.
    maq: Até à próxima
    maq: Produtos do stock atualizados com sucesso!
    ```

- **Atualização do Stock**:

    ```python
    stockFinal = []

    for key, valor in lexer.stock.items():
        stockFinal.append({
            "cod" : key,
            "nome" : valor[0],
            "quant" : valor[1],
            "preco" : valor[2]
        })

    with open("vendingStock.json", "w", encoding="UTF-8") as file:
        json.dump(stockFinal,file,indent=2)

    print("maq: Produtos do stock atualizados com sucesso!")
    ```

    - Converte o stock atualizado de volta para o formato `JSON`.
    - Salva no ficheiro `JSON` para persistência entre execuções.


## Conclusão

Este tpc implementa um simulador de uma máquina  de vending, permitindo listar produtos, inserir moedas, selecionar produtos, verificar saldo e adicionar novos produtos. A integração com `ply.lex` permite o processamento eficiente de comandos do utilizador, enquanto a persistência dos dados de stock em `JSON` garante que o estado da máquina é mantido entre execuções.
