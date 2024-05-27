# TPC1 - Análise de um Dataset

# 2024-02-09

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

## Objetivo

O objetivo deste TPC é desenvolver um programa em Python que analise um dataset esportivo e realizar as seguintes tarefas:

1. Lista ordenada alfabeticamente das modalidades desportivas;

2. Percentagens de atletas aptos e inaptos para a prática desportiva;

3. Distribuição de atletas por escalão etário (escalão = intervalo de 5 anos): ... [30-34], [35-39], ...

## Resolução

### **Estrutura**

Para a realização do mesmo é necessário importar o módulo `sys`, como mostrado a seguir:

```
import sys
```

#### **Variáveis de Armazenamento**

As seguintes variáveis são inicializadas para armazenar as informações necessárias para a realização das tarefas:

```python
listaModalidades = []
listaDistribuida = {}
aptos = 0
inaptos = 0
atletas = 0
```

#### **Leitura e Processamento do Dataset**

O dataset é lido linha por linha a partir da entrada padrão:

```python
for indice, lines in enumerate(sys.stdin):
    if indice == 0:
        continue  # Salta a primeira linha (cabeçalho)

    myline = lines.rstrip()
    line = myline.split(",")  # Divide a linha em campos usando vírgula como separador
```


#### **Extração de Modalidades**:
As modalidades esportivas são extraídas e adicionadas à lista de modalidades, realizando a verificação da existência das modalidades na lista:
```python
if line[8] not in listaModalidades:
        listaModalidades.append(line[8])
```

#### **Contagem de Atletas Aptos e Inaptos**:
A contagem dos atletas aptos e inaptos é atualizado com base no valor do campo de aptidão:
```python
if line[12] == 'true':
        aptos += 1
    else:
        inaptos += 1

    atletas += 1
```

#### **Distribuição por Escalão Etário**:
A idade do atleta é usada para calcular o intervalo etário e distribuir os atletas nos respetivos escalões:

```python
idade = int(line[5])
intervaloIdades = (idade - (idade % 5), idade - (idade % 5) + 4)

if intervaloIdades in listaDistribuida.keys():
    listaDistribuida[intervaloIdades].append(line)
else:
    listaDistribuida[intervaloIdades] = []
```


#### Ordenação e Impressão dos Resultados:
- **Modalidades Esportivas**:

```python
listaModalidades = sorted(listaModalidades)

print("Modalidades:\n")
for i, modalidade in enumerate(listaModalidades):
    if i + 1 == len(listaModalidades):
        print(modalidade + ".\n")
    else:
        print(modalidade, end=",\n")
```

- **Percentagens de Aptos e Inaptos**:

```python
print("Percentagens da Aptabilidade dos Atletas:\n")
print("Atletas aptos: " + str((aptos / atletas) * 100) + "%")
print("Atletas inaptos: " + str((inaptos / atletas) * 100) + "%\n")
```

- **Distribuição por Escalão Etário**:

```python
print("Escalões:\n")
for i, key in enumerate(sorted(listaDistribuida.keys())):
    if i + 1 == len(listaDistribuida.keys()):
        print(f"[{key[0]}-{key[1]}].")
    else:
        print(f"[{key[0]}-{key[1]}]", end=", ")
```

## Conclusão

Este TPC implementa o processamento de um dataset esportivo, produzindo uma lista ordenada de modalidades, calculando percentagens de aptidão e distribuindo atletas por escalões etários de 5 anos. A abordagem como pedido evita o uso do módulo CSV, utilizando assim métodos básicos de manipulação de strings e listas para atingir os objetivos propostos do TPC.
