import socket
import sys
import json
import time
import threading
from random import randint
from tabuleiro import gerarTabuleiro, editInput, jogador, jogada, automatico, velha, empate

clientes = []

host = socket.gethostname()
port = 10100

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(10)

def sendTabuleiro(tabuleiro, client):
    tab = json.dumps(tabuleiro)
    client.send(tab.encode())

def recvPosicao(client, tabuleiro, key):
    pos = client.recv(5000).decode().split(' ', 1)
    x, y = editInput(pos[0], pos[1])

    # Se for 0 a posição é válida
    if not (jogada(tabuleiro, (x, y), key)):
        valid = '1'
    else:
        valid = '0'
    
    return valid

def recebeOpcao(client):
    try:
        while True:
            op = client.recv(1024).decode()
            print(type(op), op)
            if op == '1':
                print("Jogar no automatico")
                jogando = False

                # Gera o tabuleiro
                tabuleiro = gerarTabuleiro()

                # Gera o X ou O
                key = jogador()
                keyAut ='O' if key == 'X' else 'X'
                print(keyAut)

                # Decide quem vai começar o jogo
                vez = randint(1, 2)
                if vez == 1: # O cliente começa
                    vezAut = 2
                    client.send((str(vez) + " " + key).encode())
                    jogando = True
                else: # Servidor começa e avisa pro cliente que o servidor vai começar
                    vezAut = 1
                    client.send((str(vez) + " " + key).encode())
                    validAut = automatico(tabuleiro, keyAut)
                    if (validAut): # Enquanto não achar uma posição disponível, não permite o user jogar 
                        jogando = True
      
                time.sleep(0.3)
                while jogando:
                    sendTabuleiro(tabuleiro, client)
                    valid = recvPosicao(client, tabuleiro, key)
                    client.send(valid.encode())

                    if (valid == '0'):
                        print("posição válida!")
                        validAut = automatico(tabuleiro, keyAut)
                        if (validAut):
                            print(validAut)
                            jogando = True

            elif op == '2':
                print("2 jogadores")
                jogando = False
                
                if not clientes:
                    print("está vazio")
                    search = '1'
                else:
                    print("Não está vazio")
                    search = '0'
                    clientes[0].send('0'.encode()) # Avisa ao jogador q estava esperando
                
                clientes.append(client)
                client.send(search.encode())

                if search == '0':
                    # Gera o tabuleiro
                    tabuleiro = gerarTabuleiro()

                    # Gera o X ou O
                    key1 = jogador()
                    key2 ='O' if key1 == 'X' else 'X'

                    # Decide quem vai começar o jogo
                    vez = randint(1, 2)
                    if vez == 1: # O cliente[0] começa
                        clientes[0].send((str(vez) + " " + key1).encode())
                        clientes[1].send(('2' + " " + key2).encode())
                    else: # O cliente[1] começa
                        clientes[1].send(('1' + " " + key2).encode())
                        clientes[0].send((str(vez) + " " + key1).encode())
                    
                    jogando = True
                    time.sleep(0.5)
                    # while jogando:
                    for client in clientes:
                        sendTabuleiro(tabuleiro, client)
                        # valid = recvPosicao(client, tabuleiro, key)
                        # client.send(valid.encode())

                        # if (valid == '0'):
                        #     print("posição válida!")
                        #     validAut = automatico(tabuleiro, keyAut)
                        #     if (validAut):
                        #         print(validAut)
                        #         jogando = True

            elif op == '0':
                print("Encerrando!")
                client.close()
                sys.exit()
            else:
                print(" \nOpção inválida! Tente novamente.")
    except ConnectionResetError as erro:
        print(erro)

while True:
    try:
        client, addr = serversocket.accept()
        print("conexão aceita")
        threading.Thread(target=recebeOpcao, args=(client,)).start()
    except KeyboardInterrupt as erro:
        print(erro)