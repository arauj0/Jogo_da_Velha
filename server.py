import socket
import threading

def chat(clientsocket):
    while True:
        mensagem = clientsocket.recv(1024)
        if clientsocket==clientes[0]:
            clientes[1].send(mensagem)
        elif clientsocket==clientes[1]:
            clientes[0].send(mensagem)

clientes = []

host = socket.gethostname()
port = 10100

socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketserver.bind((host,port))
socketserver.listen(2)

for i in range(2):
    clientsocket, addr = socketserver.accept()
    print("conexão aceita")
    clientes.append(clientsocket)

threading.Thread(target=chat, args=(clientes[0],)).start()
threading.Thread(target=chat,args=(clientes[1],)).start()

socketserver.close()