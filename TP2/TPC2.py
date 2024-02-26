import re
import sys

def convert(file):

    padroes = {
        r'^(#{1,6}) (.*)$' : lambda match: f'<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>', # Cabeçalhos
        r'(?<!\*)(\*)(?!\*)(.*?)(\*)(?!\*)': r'<i>\2</i>', # Itálico
        r'(\*\*)(.*?)(\*\*)': r'<b>\2</b>', # Negrito
        r'\d\.\s(.*)': r'<li>\1</li>', # Lista numerada
        r'\[([^]]+)\]\(([^)]+)\)': r'<a href="\2">\1</a>', # Links
        r'!\[(.+)?\]\((.+)\)': r'<img src="\2" alt="\1"/>', # Imagens
        r'\n': r'<br>', # Quebra linha
    }
    
    html = ""

    for line in file:
        html += line

    for padrao, troca in padroes.items():
        if callable(troca):
            html = re.sub(padrao, troca, html, flags=re.MULTILINE)
        else:
            html = re.sub(padrao, troca, html)

    
    # Converter listas numeradas
    html = re.sub(r'(\<li\>.+\<\/li\>(?:(?:\n).+$)*)', r'<ol>\n\1\n</ol>', html, flags=re.MULTILINE)

    return html

    
def main(input):
    if (len(input) > 1):
        file = open(input[1],'r')
        output = convert(file)
        print("html: " + output)

        fileHTML = open("pagina.html", "w",encoding="utf-8")
        fileHTML.write(output)
    else:
        print("Error")

if __name__ == "__main__":
    main(sys.argv)