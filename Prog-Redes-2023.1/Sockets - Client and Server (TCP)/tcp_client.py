import socket, sys, os
diretorio_atual = os.path.dirname(os.path.abspath(__file__)); sys.path.append(diretorio_atual + '\\Functions')
from socket_constants import * ; from Socket_Connection import CLIENT_TCP, RECV ; from Functions_Decorative import *

# ------------------------------------------------------------------------------------------------------------

print('='*100); frase = 'Client - Server'; ASCII_ART(frase); print('\t\t\tCreated by Kakanetwork');print('='*100)

# Criando o socket TCP
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ------------------------------------------------------------------------------------------------------------

try:
    while True:
        # Solicitar o arquivo
        nome_arquivo = input('\nDigite o nome do arquivo (EXIT p/ sair): ')
        
        # Enviando o nome do arquivo para o servidor
        print(f'\nSolicitando o arquivo: {nome_arquivo}')
        
        # Estabelecendo conexão 
        socket_client = CLIENT_TCP(HOST_SERVER, SOCKET_PORT, nome_arquivo, CODE_PAGE)

# ------------------------------------------------------------------------------------------------------------
        
        if nome_arquivo.upper() == 'EXIT': break

        dado_retorno = RECV(socket_client, BUFFER_SIZE, CODE_PAGE)

        if 'Size:' in dado_retorno:
            tamanho_total = int(dado_retorno.split(':')[1])

# ------------------------------------------------------------------------------------------------------------

        # Gravar o dado recebido em arquivo
        print(f'\nGravando o arquivo: {nome_arquivo}\nTamanho: {tamanho_total} bytes')
        nome_arquivo_ = ATUAL_DIR + '\\img_client\\' + nome_arquivo
        arquivo = open(nome_arquivo_, 'wb')
        bytes_recebidos = 0
        pct = 1

# ------------------------------------------------------------------------------------------------------------

        while True:
            # Recebendo o conteúdo do servidor
            dado_retorno = RECV(socket_client, BUFFER_SIZE)
            if not dado_retorno: break
            print(f'Pacote ({pct}) - Dados Recebidos: {len(dado_retorno)} bytes')
            arquivo.write(dado_retorno)
            bytes_recebidos += len(dado_retorno)
            if bytes_recebidos >= tamanho_total: break
            pct += 1
        arquivo.close()

# ------------------------------------------------------------------------------------------------------------

    # Fechando o socket
    socket_client.close()
except KeyboardInterrupt:
    print('\nFoi pressionado CTRL+C!')
    # Fechando o socket
    socket_client.close()    
except:
    print(f'\nERRO: {sys.exc_info()[0]}')
    socket_client.close()    
    
# ------------------------------------------------------------------------------------------------------------
