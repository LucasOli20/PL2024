import ply.lex as lex
import json
import sys
import re
from datetime import date

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'SALDO',
    'ADICIONAR'
)

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

def t_SALDO(t):
    r"SALDO"
    eur = int(lexer.saldo/100)
    cents = lexer.saldo % 100
    if eur > 0:
        print(f"maq: Saldo = {eur}e{cents}c")
    else:
        print(f"maq: Saldo = {cents}c")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

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

while(lexer.vendON):
    data = input('>> ')
    lexer.input(data)
    lexer.token()

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