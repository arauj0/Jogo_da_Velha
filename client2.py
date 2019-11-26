import socket
import os
import sys
from tabuleiro import menu

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