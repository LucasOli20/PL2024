import sys

listaModalidades = []

listaDistribuida = {}

aptos = 0
inaptos = 0
atletas = 0

for indice,lines in enumerate(sys.stdin):
    if indice == 0:
        continue

    myline = lines.rstrip()

    line = myline.split(",")

    if line[8] not in listaModalidades:
        listaModalidades.append(line[8])

    if line[12] == 'true':
        aptos = aptos + 1
    else:
        inaptos = inaptos + 1

    atletas = atletas + 1

    idade = int(line[5])

    intervaloIdades = (idade - (idade%5), idade - (idade%5)+4)

    if intervaloIdades in listaDistribuida.keys():
        listaDistribuida[intervaloIdades].append(line)
    else:
        listaDistribuida[intervaloIdades] = []

        
listaModalidades = sorted(listaModalidades)

print("Modalidades:\n")
for i,modalidade in enumerate(listaModalidades):
    if i+1 == len(listaModalidades):
        print(modalidade + ".\n")
    else:
        print(modalidade,end=",\n")
    

# print("aptos: ", aptos)
# print("inaptos: ", inaptos)
# print("atletas: ", atletas)
print("Percentagens da Aptabilidade dos Atletas:\n")
print("Atletas aptos: " + str((aptos/atletas)*100) + "%")
print("Atletas inaptos: " + str((inaptos/atletas)*100) + "%\n")

print("Escalões:\n")
for i,key in enumerate(sorted(listaDistribuida.keys())):
        if i+1 == len(listaDistribuida.keys()):
            print(f"[{key[0]}-{key[1]}].")
        else:
            print(f"[{key[0]}-{key[1]}]", end=", ")


