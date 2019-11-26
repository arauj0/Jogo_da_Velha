import socket
import sys
import json
import threading
import time
from tabuleiro import gerarTabuleiro, editInput, jogador, jogada, automatico

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
        return '1'
    else:
        return '0'

def recebeOpcao(client):
    try:
        while True:
            op = client.recv(1024).decode()
            print(type(op), op)
            if op == '1':
                print("Jogar no automatico")
                jogando = True

                key = jogador()
                client.send(key.encode())
                keyAut ='O' if key == 'X' else 'X'
                print(keyAut)
                time.sleep(0.3)

                tabuleiro = gerarTabuleiro()
                sendTabuleiro(tabuleiro, client)

                # while jogando:
                # sendTabuleiro(tabuleiro, client)
                valid = recvPosicao(client, tabuleiro, key)
                client.send(valid.encode())
                if (valid == '1'):
                    sendTabuleiro(tabuleiro, client)


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