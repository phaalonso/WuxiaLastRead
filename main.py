from scrapper import *

lista = pesquisar_novel()

print('Novels encontradas:')
i = 0
for novel in lista:
    print(f'[{i}] {novel["nome"]} ')
    i += 1

while True:
    i = int(input('Selecione uma novel(-1 para sair): '))
    if i == -1:
        exit()
    elif i < len(lista):
        break
    else:
        print('Valor invalido')

slug = '/novel/' + lista[i]['slug']
link = 'https://www.wuxiaworld.com' + slug

capitulos = novel_capitulos(link, slug)

''' Imprimir capitulos de forma limpa, com titulo '''
l = 1
for cap in capitulos:
    print(f'[{l}] {cap["nome"]}')
    l += 1

while True:
    try:
        print('Escolha um capitulo, o numero necessário é o que esta entre [] ')
        print('Use -1 para sair')
        cap = int(input('Capitulo: '))
        if cap == -1:
            exit()
        elif cap > 0 and cap <= len(capitulos):
            cap -= 1
            break
        else:
            raise ValueError('Não existe uma novel com esse index!')
    except ValueError as err:
        print('Valor invalido!')
        print(err)

# print(capitulos[cap])

#TODO Abrir a página da novel selecionada, e extrair o texto dela
link_capitulo = link + capitulos[cap]['href']
print(link_capitulo)
novel = pegar_novel(link_capitulo)

print(novel)
