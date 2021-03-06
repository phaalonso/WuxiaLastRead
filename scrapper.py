import requests 
from bs4 import BeautifulSoup
import json
import re

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

def listar():
    ''' 
        Essa função realiza a pesquisa da novel na WuxiaWorld, atráves da api e retorna 
        uma lista com dicionários contendo os resultados da pesquisa.
        Os dicionários estao no seguinte formato:
        {
            'nome' : 'Nome da novel',
            'slug' : 'Caminho para abrir a página da novel'
        }
        O script continuara a se repetir até que o usuario deseja sair, ou encontre algum resultado valido
    '''
    api = 'https://www.wuxiaworld.com/api/novels/search?'
    print('Você pode usar -1 para sair do script.')
    while True:
        nome = str(input('Nome da novel:')).strip().replace(' ', '+')
        if nome == '-1':
            exit()
        
        try:
            r = requests.get(api, {
                'query': nome, 
                'count': 10
                }, headers = header)
            rjson = json.loads(r.content)
        except requests.ConnectionError as err:
            print('Ocorreu um erro de conexão')
            print('Porfavor verifique se há conexão com a internet!')
            exit()
        except json.JSONDecodeError as err:
            print('Algo de errado aconteceu com json!')
            print(err)
            exit()
        if len(rjson['items']) > 0: 
            break
        else:
            print(f'Nao encontramos nenhuma novel com esse nome: "{nome}"')

    lista = []
    for item in rjson['items']:
        lista.append({
            'nome' : item['name'],
            'slug' : item['slug']
        })
    # print(lista)
    return lista

def capitulos(link, slug):
    ''' 
        Essa função é responsavel por encontrar os capitulos no site e os retornar em uma lista 
        O parametro r é a resposta do request ao site da novel, enquanto o slug é link utilizado para acessar essa página. 
        Se o link da pagina fosse https://www.wuxiaworld.com/novel/emperors-domination
        O slug seria novel/emperors-domination
    '''
    try:
        r = requests.get(link, headers = header)
        if r.status_code != 200:
            print(f'Resposta do {r.url} \nCódigo {r.status_code}!!')
            exit()
    except requests.ConnectionError as err:
        print('Ocorreu um erro de conexão')
        print('Porfavor verifique se há conexão com a internet!')
        exit()

    soup = BeautifulSoup(r.content, 'html.parser')
    elem = soup.find_all('a', href=re.compile(slug))
    capitulos = []
    lenslug = len(slug)
    for cap in elem:
        if cap.span != None:
            capitulos.append({
                'href': cap['href'][lenslug:],
                'nome': cap.span.string
            })
        # print(cap.span.string)

    return capitulos


def get_texto(link, capitulo_selecionado):
    ''' 
        Essa função recebe o link do capítulo, extrai a novel da página
        e a retorna em uma lista de paragrafos.
    '''
    # print(link_capitulo)
    link += capitulo_selecionado['href']
    r = requests.get(link, headers = header)
    if r.status_code != 200:
        print(f'Resposta do url: {r.url}\n Código: {r.status_code}!!')
        exit()
    soup = BeautifulSoup(r.content, 'html.parser')
    texto = soup.find_all('p', style=False)
    arq = []
    for p in texto:
        if not (p.a != None and p.a['href'].startswith('/announcement/')):
            arq.append(p)

    novel = []
    ''' Filtrando o arquivo '''
    for p in arq:
        if p.string not in [None, 'Contact Us',
                            'Privacy Policy',
                            'RSS', 'Twitter',
                            'Facebook', 'Discord']:
            novel.append(p.string)
    return novel

def selecionar_capitulo(capitulos, link):
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
    return capitulos[cap]
    
def pesquisar_novel():
    ''' 
        Essa função realiza a pesquisa da novel e retorna seu dicionario com as informações.

        {
            'nome' : 'Nome da novel',
            'slug' : 'Caminho para abrir a página da novel',
            'abvv' : 'Abreviação da novel'
        }
    '''
    lista = listar()

    print('Novels encontradas:')
    i = 0
    for novel in lista:
        print(f'[{i}] {novel["nome"]} ')
        i += 1

    while True:
        try:
            i = int(input('Selecione uma novel(-1 para sair): '))
            if i == -1:
                exit()
            elif i < len(lista):
                break
            else:
                print('Valor invalido')
        except ValueError:
            print('Deve ser inserio um inteiro!!')
    return lista[i]
