import scrapper
import favoritos

while True:
    print(' 1 - Pesquisar por uma novel')
    print(' 2 - Adicionar novel aos favoritos')
    print(' 3 - Verificar favoritos')
    print('-1 - Para sair')
    while True:
        try:
            op = int(input('Sua escolha: '))
            if op == -1:
                exit()
            elif op > 0 and op < 4:
                break
        except ValueError:
            print('O valor da opção deve ser um valor inteiro!!')

    if op == 1:
        novel = scrapper.pesquisar_novel()
        # print(novel)
        slug = '/novel/' + novel['slug']
        link = 'https://www.wuxiaworld.com' + slug
        
        capitulos = scrapper.capitulos(link, slug)
        
        capitulo_selecionado = scrapper.selecionar_capitulo(capitulos, link)
        print(capitulo_selecionado)
        lista_texto = scrapper.get_texto(link, capitulo_selecionado)
        print(lista_texto)

    elif op == 2:
        lista = favoritos.pegar_lista()
        favoritos.adicionar(lista)
    
    elif op == 3:
        lista = favoritos.pegar_lista()
        favoritos.verificar_atualizacao(lista)