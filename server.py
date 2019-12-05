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

def sendTabuleiro(tabul, cliente):
    tab = json.dumps(tabul)
    cliente.send(tab.encode())

def recvPosicao(cliente, tabuleiro, chave1, chave2):
    posicao = cliente.recv(5000).decode().split(' ', 1)
    x, y = editInput(posicao[0], posicao[1])
    print(x, y)

    # Se for 0 a posição é válida
    if not (jogada(tabuleiro, (x, y), chave1)):
        valid = '1'
    else:
        valid = '0'
        if not (velha(tabuleiro, chave1, x, y)):
            print(x, y)
            print("Você venceu!")
        elif (empate(tabuleiro, chave1) == 4 and empate(tabuleiro, chave2) == 4):
            print("Empate")
    
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
                    valid = recvPosicao(client, tabuleiro, key, keyAut) # Adicionei a chave 2
                    client.send(valid.encode())

                    if (valid == '0'):
                        print("posição válida!")
                        validAut = automatico(tabuleiro, keyAut)
                        if (validAut):
                            print(validAut)
                            jogando = True

            elif op == '2':
                print("2 jogadores")
                
                if not clientes:
                    search = '1'
                else:
                    search = '0'
                    clientes[0].send('0'.encode()) # Avisa ao jogador q estava esperando
                
                clientes.append(client)
                client.send(search.encode())

                if search == '1': # MISERAAAAAAAAAAAAA
                    time.sleep(120) # espera 2 min, se não conectar nenhum jogador, ele avisa
                else:
                    jogando1 = False
                    jogando2 = False
                    jogo = False

                    # Gera o tabuleiro
                    tabuleiro = gerarTabuleiro()

                    # Gera o X ou O
                    key1 = jogador()
                    key2 ='O' if key1 == 'X' else 'X'

                    # Decide quem vai começar o jogo
                    vez1 = randint(1, 2)
                    vez2 = 2 if vez1 == 1 else 1

                    print("Jogador 1: ", key1, vez1)
                    print("Jogador 2: ", key2, vez2)

                    clientes[0].send((str(vez1) + " " + key1).encode())
                    clientes[1].send((str(vez2) + " " + key2).encode())

                    if vez1 == 1:
                        print("O jogador 1 vai começar!")
                        jogador1 = clientes[0]
                        jogador2 = clientes[1] 
                        key_1 = key1
                        key_2 = key2
                    else:
                        print("O jogador 2 vai começar!")
                        jogador1 = clientes[1]
                        jogador2 = clientes[0]
                        key_1 = key2
                        key_2 = key1
        
                    time.sleep(0.9)
                    jogando1 = True
                    jogando2 = False
                    jogo = True

                    while jogo:
                        while jogando1:
                            time.sleep(0.5)
                            sendTabuleiro(tabuleiro, jogador1)
                            print("Recebendo dados do jogador1")
                            valid = recvPosicao(jogador1, tabuleiro, key_1, key_2)
                            jogador1.send(valid.encode())

                            if (valid == '0'):
                                print("posição válida!")
                                passarvez = jogador1.recv(1024).decode()
                                if passarvez == '3':
                                    print("Passou a vez")
                                    time.sleep(0.5)
                                    jogador2.send("3".encode())
                                    # time.sleep(0.5)
                                    jogando2 = True
                                    jogando1 = False
                        
                        while jogando2:
                            time.sleep(0.5)
                            sendTabuleiro(tabuleiro, jogador2)
                            print("Recebendo dados do jogador2")
                            valid = recvPosicao(jogador2, tabuleiro, key_2, key_1)
                            jogador2.send(valid.encode())

                            if (valid == '0'):
                                print("posição válida!")
                                passarvez = jogador2.recv(1024).decode()
                                if passarvez == '3':
                                    print("Passou a vez")
                                    time.sleep(0.5)
                                    jogador1.send("3".encode())
                                    # time.sleep(0.5)
                                    jogando1 = True
                                    jogando2 = False

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