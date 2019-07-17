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
    ''' 
        Essa função é responsavel por acessar o arquivo favoritos.json e retornar as informações dela em um dicionário
    '''
    try:
        with open('favoritos.json', 'r') as f:
            lista = json.load(f)
    except:
        lista = {
            "fav": []
        }
    return lista

def adicionar(lista):
    ''' 
        Essa função realiza a pesqusia da novel que o usuário deseja adicionar ao seus favoritos.
        Ela irá verificar se a novel ja foi adicionado, e caso não seja ela irá receber o ultimo capitulo lido do usuário e salver em um arquivo.
    '''
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
    # print(capitulo_selecionado)
    with open('favoritos.json', 'w') as f:
        json.dump(lista, f)

def verificar_atualizacao(lista):
    ''' Realizara a verficação se a novel recebeu novos capitúlos'''

    link = 'https://www.wuxiaworld.com'

    if len(lista['fav']) == 0:
        print('\nA lista está vazia!! \nPor favor adicione uma novel primeiro!!\n')
        return()

    for n in lista['fav']:
        # print(n)
        '''
            {
                'nome': 'The Unrivaled Tang Sect',
                'slug': 'the-unrivaled-tang-sect', 'last': '/uts-chapter-1-2'
            }
         '''   
        print(f"\n-----{n['nome']}-----")
        slug = '/novel/' + n['slug']
        templ = link + slug
        capitulos = scrapper.capitulos(templ, slug)
        # print(capitulos[-1]['href'], n['last'])
        for cap in capitulos:
            if n['last'] == cap['href']:
                # print(cap)
                index = capitulos.index(cap)
                break
        
        print(f"Last read: {cap['nome']}")
        # print(index , len(capitulos))
        if not index == len(capitulos) - 1:
            print(f"Next chapter: {templ + capitulos[index + 1]['href']}\n")
        else:
            print('You already read the last chapter!\n')

def atualizar_arquivo(lista):
    ''' Essa função é responsavel por atualizar o ultimo capitulo lido do usuario guardado no arquivo
        favoritos.json
    '''

    if len(lista['fav']) == 0:
        print('\nA lista está vazia!! \nPor favor adicione uma novel primeiro!!\n')
        return()
    
    print('Escolha uma das novels abaixo: ')
    for i in range(0,len(lista['fav'])):
        print(f"[{i}] {lista['fav'][i]['nome']}")

    while True:
        try:
            op = int(input('Opção: '))
            
            if op == -1:
                exit()
            elif op >= 0 and op < len(lista['fav']):
                break
            else:
                print('Opção invalida!!!')
        except ValueError:
            print('Digite apenas inteiros!!!')

    print('----- Capitulos -----')
    slug = '/novel/' + lista['fav'][op]['slug']
    link = 'https://www.wuxiaworld.com' + slug
    capitulos = scrapper.capitulos(link, slug)
    capitulo_selecionado = scrapper.selecionar_capitulo(capitulos, link)

    # print(capitulo_selecionado['href'])
    # print(lista['fav'][op])
    lista['fav'][op]['last'] = capitulo_selecionado['href']
    # print(lista['fav'][op])
    with open('favoritos.json', 'w') as f:
        json.dump(lista, f)

    print('Capitulo atualizado!!')