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
    print(x, y)

    # Se for 0 a posição é válida
    if not (jogada(tabuleiro, (x, y), key)):
        valid = '1'
    else:
        valid = '0'
    
    return valid

# def venceu(tabuleiro, key, x, y):
#     if not (velha(tabuleiro, key, x, y)):
#         venceu = '1'
#         jogando = False
#     elif (empate(tabuleiro, key) == 4):
#         venceu = '2'
#         jogando = False
#     else:
#         venceu = '0' #continua o jogo
    
#     return venceu

def recebeOpcao(client):
    try:
        while True:
            op = client.recv(1024).decode()
            print(type(op), op)
            if op == '1':
                print("Jogar no automatico")
                jogando = False
                venceu = ''

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

                    # time.sleep(0.3)
                    # client.send(venceu.encode())


            elif op == '2':
                print("cadastro")
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
        clientes.append(client)
        threading.Thread(target=recebeOpcao, args=(client,)).start()
    except KeyboardInterrupt as erro:
        print(erro)