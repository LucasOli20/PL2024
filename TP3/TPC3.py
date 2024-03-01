import re
import sys

dicionario = [
    ('numero', r'\d+'),
    ('igual', r'='),
    ('on', r'[oO][nN]'),
    ('off', r'[oO][fF][fF]')
]

def main(input):
    
    texto = input[1].split("\n")

    regex = '|'.join('(?P<%s>%s)' % par for par in dicionario)

    soma = True
    valor = 0

    for linha in texto:

        ms = re.finditer(regex,linha)
        for m in ms:
            dic = m.groupdict()
            if dic['on'] is not None:
                soma = True
            elif dic['off'] is not None:
                soma = False
            elif dic['numero'] is not None and soma == True:
                valor += int(dic['numero'])
            elif dic['igual'] is not None:
                print(f"Valor somado: {valor}")
            

if __name__ == "__main__":
    main(sys.argv)
