import socket
import os
import sys
import json
import time
from tabuleiro import menu, drawTabuleiro

host = socket.gethostname()
port = 10100

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientsocket.connect((host, port))
    while True:
        menu()
        op = input("Escolha uma opção: ")
        clientsocket.send(op.encode())
        os.system('cls')

        if op == '1':
            jogando = False
            
            init = clientsocket.recv(5000).decode().split(' ', 1)
            if (init[0] == '1'):
                print("Você começa o jogo!")
                print("Sua letra é", init[1])
                jogando = True
            else:
                print("O automático começa!")
                print("Sua letra é", init[1])
                time.sleep(0.7)
                jogando = True

            while jogando:
                os.system('cls')
                print("Sua vez!")
                print("Sua letra é", init[1])

                tab = clientsocket.recv(20000)
                tabuleiro = json.loads(tab.decode())
                drawTabuleiro(tabuleiro)

                letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')  
                clientsocket.send((letra + " " + numero).encode())   

                valid = clientsocket.recv(1024).decode()
                if (valid == '0'):
                    os.system('cls')
                    print("Vez do computador! Espere!")
                    time.sleep(0.7)
                    jogando = True
                else:
                    os.system('cls')
                    print(valid)
                    print("Posição inválida! Tente outra vez!")
                    print("Sua letra é", init[1])
                    time.sleep(0.5)
                    jogando = True

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