# TPC2 - Conversor de ficheiro MD para HTML

# 2024-02-16

# Autor

- **Nome**: Lucas Oliveira

- **Nr.Aluno**: A98695

# Objetio
Consistiu em criar um convertor de ficheiros do tipo `MarkDown` para `HTML` para os seguintes elementos:

- **Cabeçalhos**
- **Itálico**
- **Negrito**
- **Lista Numerada**
- **Lista não Numerada**
- **Links**
- **Imagens**

# Resolução

Para a realização desta tarefa, foram usados os módulos `sys` e `re` do <u>**Python**</u>.

Primeira, o programa verifica se existe algum argumento passado para poder ler, em que se existe, abri-mos então o ficheiro em modo <u>leitura</u> e manda-mos para a função que converte para `html`

Para processar os diferentes elementos em linguagem `Markdown`, foram utilizadas expressões regulares:

* Para os `cabeçalhos` usou-se uma expressão regular que busca por linhas iniciadas por um ou mais `#`, substituindo por cabeçalhos em <u>**HTML**</u>: `<h1>`,`<h2>`,`<h3>`, etc, conforme a quantidade de `#` presentes.

* Para o `itálico` ou `negrito`, normalmente o texto está envolvidos entre `*` e são utilizados as tags `<i>` para o **itálico**, e quando o texto tem envolvido `**` é utilizado as tags `<b>` para o **negrito**.

* Para `listas numeradas`, primeiro transforma-se as linhas iniciadas com o número seguido do ponto em itens da tag `<li>`, de seguida, esses itens são agrupados entre tags `ol` para assim formar a lista numerada.

* para `links`, o texto com o formato `[texto do link](link)` é substituido pelas tags `<a>`, em que o texto é o conteúdo e o link é o atributo `href`.

* para `imagens`, o texto com o formato `![texto alternativo](caminho da imagem)` é substituido pelas tags `<img>`, em que o texto alternativo é o atributo `alt` e o caminho da imagem é o `src`.

No final, é escrito o conteúdo todo convertido em um ficheiro **HTML**.
