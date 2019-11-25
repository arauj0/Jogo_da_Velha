import socket
from threading import Thread

host = socket.gethostname()
port = 10100

# while True:
try:
    socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as erro:
    print("Falha ao criar socket")
    print("Erro: %s" % str(erro))
    print("Socket criado!")

try:
    socketclient.connect((host, port))
    print("Conectado!")
    socketclient.send('ola'.encode())
except socket.error as erro:
    print("Falha ao conectar a %s na porta %s" % (host, port))
    print("Razão: %s" % str(erro))
finally:
    socketclient.close()