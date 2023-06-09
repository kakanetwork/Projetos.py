import socket
from functions_others import *
from variables import *

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR O CHAT ENTRE CLIENTES ESPECIFICOS  '''

def CHAT(comand=None, clients_dict=None, info_client=None, sock=None, **kwargs): 
    try:
        ip_destination = comand[1] # guardando o ip de destino da mensagem
        port = comand[2] # guardando a porta de destino
        for chave, valor in clients_dict.items(): # dando um for na lista de clientes
            port_envio = str(chave) 
            sock_envio = valor[1] # pegando o socket do cliente destino 
            ip_envio = valor[0]
            if ip_destination == ip_envio and port == port_envio: # verificando se o ip/porta (ou seja cliente) está conectado ao servidor
                msg_chat = f"\nO Cliente: {info_client[0]}:{info_client[1]} lhe enviou uma mensagem!\nMensagem >> {comand[3]}\n" # formatação de mensagem
                sock_envio.send(msg_chat.encode(UNICODE)) # realizando o envio para o socket do cliente destino
            else:
                msg_erro = f"\nO Cliente informado para encaminhar a mensagem não está conectado Servidor!\n"
                sock.send(msg_erro.encode(UNICODE))
                exit()
    except:
        print(f'\nErro no Chat...{sys.exc_info()[0]}')  
        exit() 
            
# ============================================================================================================

''' FUNÇÃO PARA REALIZAR O PRINT DA
 LISTAGEM DE CLIENTES CONECTADOS AO SERVIDOR '''

def LIST_CLIENTS(clients_dict=None, sock=None, **kwargs):
    try:
        msg_title = "\nOs Clientes conectados ao Servidor são:" # formatando mensagem
        sock.send(msg_title.encode(UNICODE)) 
        num = 0
        for chave, valor in clients_dict.items():  # faço um for para pegar cada cliente conectado e enviar 
            ip = valor[0] 
            num+=1 # formatação numeração cliente
            msg_list = f"\nCLIENTE {num}\nIP: {ip}\nPORT: {chave}\n" # formatação listagem clientes
            sock.send(msg_list.encode(UNICODE)) # enviando mensagens 
    except:
        print(f'\nErro no List_Clients...{sys.exc_info()[0]}')  
        exit() 

# ============================================================================================================

def CLIENT_INTERACTION(sock_client, info_client, clients_connected):
    try:
        opções = {
            '/l': LIST_CLIENTS,
            '/m': CHAT
        }
        msg = b'' 
        while msg != b'/q': 
            try:
                msg = sock_client.recv(512).decode(UNICODE)
                comand = COMAND_SPLIT(msg)
                for opcao in opções.keys():
                    if comand[0] == opcao:
                        print(comand)
                        opções[opcao](clients_dict=clients_connected,sock=sock_client, comand=comand, info_client=info_client)
            except:
                msg = b'/q'
        del clients_connected[info_client[1]]
        sock_client.close()
    except:
        print(f'\nErro no Client_Interaction...{sys.exc_info()[0]}')  
        exit() 


# ============================================================================================================











def broadCast(msg, addrSource):
    #msg = f"{addrSource} -> {msg.decode(UNICODE)}"
    #PRINT_DIV(msg)
    for sockConn, addr in clients_connected:
        if addr != addrSource:
            sockConn.send(msg.encode(UNICODE))