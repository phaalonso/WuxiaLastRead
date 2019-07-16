import json
import scrapper

'''
    {
        "Nome" : "usuario"
        "favoritos": [
            {
                'nome': 'Dragon King With Seven Stars',
                'slug': 'dragon-king-with-seven-stars'}
        ]
    }
'''
def pegar_lista():
    try:
        with open('favoritos.json', 'r') as f:
            lista = json.load(f)
    except:
        lista = {
            "fav": []
        }
    return lista

def adicionar(lista):
    novel = scrapper.pesquisar_novel()

    nomes = []
    for n in lista['fav']:
        nomes.append(n['nome'])

    if novel['nome'] in nomes:
        print('Essa novel ja esta nos seus favoritos')
        return
    slug = '/novel/' + novel['slug']
    link = 'https://www.wuxiaworld.com' + slug
    
    capitulos = scrapper.capitulos(link, slug)
    
    capitulo_selecionado = scrapper.selecionar_capitulo(capitulos, link)

    novel['last'] = capitulo_selecionado['href']
    lista['fav'].append(novel)
    print(capitulo_selecionado)
    with open('favoritos.json', 'w') as f:
        json.dump(lista, f)
