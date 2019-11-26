import socket
import os
import sys
import json
import time
from tabuleiro import menu, drawTabuleiro

host = socket.gethostname()
port = 10100

try:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as erro:
    print("Falha ao criar socket")
    print("Erro: %s" % str(erro))
    print("Socket criado!")

try:
    clientsocket.connect((host, port))
    print("Conectado!")
    while True:
        menu()
        op = input("Escolha uma opção: ")
        clientsocket.send(str(op).encode())
        os.system('cls')

        if op == '1':
            jogando = True
            play = True
            
            key = clientsocket.recv(1024)
            print(" Você é o ", key.decode())
            while jogando:
                try:
                    if (play):
                        tab = clientsocket.recv(20000)
                        tabuleiro = json.loads(tab.decode())
                        drawTabuleiro(tabuleiro)

                        letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')  
                        clientsocket.send((letra + " " + numero).encode())   

                        valid = clientsocket.recv(1024).decode()
                        print(valid)
                        # if (valid == '0'):
                            # print("Vez do computador! Espere!")
                            # time.sleep(0.5) # Só pra dá a sensação de espera

                except ValueError:
                    os.system('cls')
                    print("Entre com um a sequência de valores corretos!")

        if op == '0':
            print("Encerrando!")
            clientsocket.close()
            sys.exit()
        else:
            print(" \nOpção inválida! Tente novamente.")
except socket.error as erro:
    print("Falha ao conectar a %s na porta %s" % (host, port))
    print("Razão: %s" % str(erro))
finally:
    clientsocket.close()