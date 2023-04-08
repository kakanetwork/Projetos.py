import requests, sys

# Url do site que iremos realizar o REQUEST
url = 'https://dados.ifrn.edu.br/dataset/d5adda48-f65b-4ef8-9996-1ee2c445e7c0/resource/00efe66e-3615-4d87-8706-f68d52d801d7/download/dados_extraidos_recursos_alunos-da-instituicao.json'

# Realizando o Request
try:
    dados = requests.get(url).json()
except:
    print(f'Não foi possivel acessar o URL, ERRO...... {sys.exc_info()[0]}')

"""
 LEMBRETE DE LAMBDA, MAP:
 o lambda vai percorrer cada item dentro da lista (cada item é um aluno e seus dados) que estão dentro de um dict (lista de dict's), então eu acesso primeiro os dicts
 com o Lambda, pois ele vai de item em item dentro da lista!, após acessar os dicts eu deixo claro no lambda que quero dentro do dict a key 'campus'
 e quem pega para mim os valores dentro dessa key, é o Map que joga para uma lista, entaõ o lambda é a função e o map é quem confirma essa função e joga na lista!
 o set serve para remover as duplicatas """


# Realizando a captura dos Campus do IFRN (sem as duplicatas)
campi = set(map(lambda c: c['campus'], dados))

print('\nEsses são os nossos Campus no IFRN e seus respectivos Alunos:')

for x in campi:
    # Realizando a função (definindo) para captura de todos os Campus (Com duplicatas)
    filtro = lambda m: m['campus'] == x
    # Aqui eu jogo quantos campus existem ao todo, e faço a contagem (qnt_campus_totais == qnt_alunos_totais) 
    # Como estamos dentro do FOR, ele vai fazer a contagem para cada Campus e apenas aqui a função lambda é ativada
    alunos = tuple(filter(filtro, dados))
    qt_alunos = len(alunos)
    print(f'Campus {x}: {qt_alunos} Alunos')

try:
    # Pedindo a sigla ao usuario e utilizando .upper para evitar erros de maiusculo/minusculo
    sigla = str(input('\nINFORME A SIGLA DO CAMPUS: ')).upper()
except: 
    # Tratamento Genérico
    print(f'Erro......: {sys.exc_info()[0]}')
    sys.exit()
else:
    # Tratamento para só aceitar siglas dentro das quais já filtramos em Campi
    if sigla in campi:
        # Parecido com o Filtro1 ele pega todos os cursos (com duplicatas) mas apenas da sigla/campus informado
        filtro2 = lambda m: m['campus'] == sigla
        campus_sigla = list(filter(filtro2, dados))
        # Aqui fazemos a captura dos cursos (sem duplicatas)
        curso = set(map(lambda c: c['curso'], campus_sigla))

        print(f'\nEsses são os cursos disponibilizados no {sigla}, e sua quantidade de alunos:')
        # Parecido com o primeiro for (lá era para os campus) e aqui será para os cursos do campus especifico (segue a mesma lógica)
        for x in curso:
            filtro_cursos = lambda c: c['curso'] == x
            qnt_cursos = list(filter(filtro_cursos, campus_sigla))
            qt_alun_cursos = len(qnt_cursos)
            print(f'Curso {x}: {qt_alun_cursos} Alunos')
    else:
        print("Sigla Inválida!")
        sys.exit()
