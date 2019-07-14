import requests 
from bs4 import BeautifulSoup
import json
import re

url = 'https://www.wuxiaworld.com/api/novels/search?'
nome = 'King'
''' Adequa o nome, ao formato necessário ao link. Substituindo os ' '  por '+' '''
nome = nome.strip().replace(' ', '+')
plink = {
    'query' : nome,
    'count' : 5
}
r = requests.get(url, plink)
rjson = json.loads(r.content)
# print(rjson['items'])
# file = open('arq.json','w')
# json.dump(rjson, file)
# file.close()

lista = []
for item in rjson['items']:
    lista.append({
        'nome' : item['name'],
        'slug' : item['slug'],
        'abvv'  : item['abbreviation']
    })

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
r = requests.get(link)
if r.status_code != 200:
    print(f'Resposta do {r.url} \nCódigo {r.status_code}!!')
    exit()

sop = BeautifulSoup(r.content, 'html.parser')
# print(sop)
elem = sop.find_all('a', href=re.compile(lista[i]['slug']))
capitulos = []
lenslug = len(slug)
for cap in elem:
    if cap.span != None:
        capitulos.append({
            'href': cap['href'][lenslug:],
            'nome': cap.span.string
        })
    # print(cap.span.string)

# print(capitulos)

#TODO Imprimir capitulos de forma limpa, com titulo
recorte = '/' + lista[i]['abvv'].lower() + '-chapter-'
lrecorte = len(recorte)
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

print(capitulos[cap])