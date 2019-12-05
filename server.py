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

# Envia o tabuleiro atual
def sendTabuleiro(tabul, cliente):
    tab = json.dumps(tabul)
    cliente.send(tab.encode())

# Recebe a x e y, edita a letra para número
# Se a jogada for inválida retorna 1
# Se for válida retorna 0, verifica se alguém venceu,
# Se ninguém tiver vencido até o contador do jogador 1 e 2 
# forem iguais a 4, dá empate e o jogo termina
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
            print("Alguém Venceu!")
            valid = '2'
        elif (empate(tabuleiro, chave1) == 4 and empate(tabuleiro, chave2) == 4):
            print("Empate!")
            valid = '3'
    
    return valid

# Recebe as opções do menu do cliente
def recebeOpcao(client):
    try:
        while True:
            op = client.recv(1024).decode()
            print(type(op), op)

            if op == '1':
                jogando = False
                cli = False
                aut = False

                # Gera o tabuleiro
                tabuleiro = gerarTabuleiro()

                # Gera o X ou O
                key = jogador()
                keyAut ='O' if key == 'X' else 'X'

                # Decide quem vai começar o jogo
                vez = randint(1, 2)
                vezAut = 2 if vez == 1 else 1

                print("Jogador: ", key, vez)
                print("Automatico: ", keyAut, vezAut)

                # Envia a vez e a key do cliente
                client.send((str(vez) + " " + key).encode())

                # Define os casos quando cada jogador vai começar
                if vez == 1:
                    print("O cliente vai começar!")
                    cli = True
                else:
                    print("O jogador 2 vai começar!")
                    aut = True

                # time.sleep(0.3)
                jogando = True
                while jogando:
                    while cli:
                        time.sleep(0.4)
                        sendTabuleiro(tabuleiro, client)
                        print("Recebendo dados do cliente")
                        valid = recvPosicao(client, tabuleiro, key, keyAut)
                        client.send(valid.encode())

                        if (valid == '0'):
                            print("posição válida!")
                            aut = True
                            cli = False
                        elif (valid == '2'): # Venceu
                            aut = False
                            cli = False
                            jogando = False
                            break
                        elif (valid == '3'): # Empate
                            aut = False
                            cli = False
                            jogando = False
                            break


                    while aut:
                        validAut = automatico(tabuleiro, keyAut, key)
                        client.send(validAut.encode())
                        if (validAut == '0'):
                            cli = True
                            aut = False
                        elif (validAut == '2'):
                            print("Automático venceu!")
                            cli = False
                            aut = False
                            jogando = False
                        elif (validAut == '3'):
                            print("Empate!")
                            cli = False
                            aut = False
                            jogando = False
                        else:
                            cli = False
                            aut = True


            elif op == '2':
                # Se a lista ainda estiver vazia, envia 1 para avisar ao jogador1
                # Que está procurando um oponente.
                # Quando o jogador2 se conecta, envia para o jogador1 que achou 
                # um oponente.
                if not clientes:
                    search = '1'
                else:
                    search = '0'
                    clientes[0].send('0'.encode()) # Avisa ao jogador q estava esperando
                
                clientes.append(client)
                client.send(search.encode())

                # Quando os 2 jogadores estiverem conectados, entra no else
                if search == '1': 
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

                    # Envia quem vai começar e sua letra
                    clientes[0].send((str(vez1) + " " + key1).encode())
                    clientes[1].send((str(vez2) + " " + key2).encode())

                    # Define os casos quando cada jogador vai começar
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
        
                    # Começa o jogo
                    # Já que sempre o jogador1 vai começar, o loop dele é True
                    time.sleep(0.8)
                    jogando1 = True
                    jogando2 = False
                    jogo = True
                    while jogo:
                        while jogando1:
                            time.sleep(0.4)
                            sendTabuleiro(tabuleiro, jogador1)
                            print("Recebendo dados do jogador1")
                            valid = recvPosicao(jogador1, tabuleiro, key_1, key_2)
                            jogador1.send(valid.encode())

                            # Se a jogada for válida passa a vez para o oponente
                            if (valid == '0'):
                                print("posição válida!")
                                passarvez = jogador1.recv(1024).decode()
                                if passarvez == '3':
                                    print("Passou a vez")
                                    # time.sleep(0.5)
                                    jogador2.send("3".encode())
                                    # time.sleep(0.5)
                                    jogando2 = True
                                    jogando1 = False
                            elif (valid == '2'): # Venceu
                                jogador2.send('4'.encode())
                                jogando2 = False
                                jogando1 = False
                                jogo = False
                                break
                            elif (valid == '3'): # Empate
                                jogador2.send('5'.encode())
                                jogando2 = False
                                jogando1 = False
                                jogo = False
                                break
                        
                        while jogando2:
                            time.sleep(0.4)
                            sendTabuleiro(tabuleiro, jogador2)
                            print("Recebendo dados do jogador2")
                            valid = recvPosicao(jogador2, tabuleiro, key_2, key_1)
                            jogador2.send(valid.encode())

                            # Se a jogada for válida passa a vez para o oponente
                            if (valid == '0'):
                                print("posição válida!")
                                passarvez = jogador2.recv(1024).decode()
                                if passarvez == '3':
                                    print("Passou a vez")
                                    # time.sleep(0.5)
                                    jogador1.send("3".encode())
                                    # time.sleep(0.5)
                                    jogando1 = True
                                    jogando2 = False
                            elif (valid == '2'): # Venceu
                                jogador1.send('4'.encode())
                                jogando1 = False
                                jogando2 = False
                                jogo = False
                                break
                            elif (valid == '3'): # Empate
                                jogador1.send('5'.encode())
                                jogando1 = False
                                jogando2 = False
                                jogo = False
                                break

            elif op == '0':
                print("Encerrando!")
                client.close()
                sys.exit()
            else:
                print(" \nOpção inválida! Tente novamente.")
    except ConnectionResetError as erro:
        print(erro)

# Aceita os clientes, a thread chama a função recebeOpção e manda o cliente como argumento
while True:
    try:
        client, addr = serversocket.accept()
        print("conexão aceita")
        threading.Thread(target=recebeOpcao, args=(client,)).start()
    except KeyboardInterrupt as erro:
        print(erro)