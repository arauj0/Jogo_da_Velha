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

        if op == '1':
            jogando = False
            suavez = False
            oponente = False
            
            init = clientsocket.recv(5000).decode().split(' ', 1)
            if (init[0] == '1'):
                print("Você começa o jogo!")
                print("Sua letra é", init[1])
                suavez = True
                jogando = True
            else:
                print("O automático começa!")
                print("Sua letra é", init[1])
                oponente = True
                jogando = True

            while jogando:
                while suavez:
                    tab = clientsocket.recv(20000)
                    tabuleiro = json.loads(tab.decode())
                    os.system('cls')
                    print("Sua vez!")
                    print("Sua letra é", init[1])
                    drawTabuleiro(tabuleiro)

                    letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ') 
                    clientsocket.send((letra + " " + numero).encode())

                    valid = clientsocket.recv(1024).decode()
                    if (valid == '0'):
                        os.system('cls')
                        print("Vez do automático! Espere!")
                        oponente = True
                        suavez = False
                    elif (valid == '2'):
                        os.system('cls')
                        print("Você Venceu!")
                        oponente = False
                        suavez = False
                        jogando = False
                    elif (valid == '3'):
                        os.system('cls')
                        print("Empate!")
                        oponente = False
                        suavez = False
                        jogando = False
                    else:
                        os.system('cls')
                        print("Posição inválida! Tente outra vez!")
                        print("Sua letra é", init[1])
                        time.sleep(0.5)
                        oponente = False
                        suavez = True
                        jogando = True
                    
                    
                while oponente:
                    validAut = clientsocket.recv(1024).decode()
                    if (validAut == '2'):
                        os.system('cls')
                        print("Você Perdeu!")
                        oponente = False
                        suavez = False
                        jogando = False
                    elif (validAut == '3'):
                        os.system('cls')
                        print("Empate!")
                        oponente = False
                        suavez = False
                        jogando = False
                    else:
                        oponente = False
                        suavez = True

        elif op == '2':
            search = clientsocket.recv(1024).decode()

            if search == '1':
               os.system('cls') 
               print("Procurando Jogador...")
               espera = True
               while espera:
                   resposta = clientsocket.recv(1024).decode()
                   if resposta == '0':
                       print("Jogador Encontrado! Sorteando quem vai começar!")
                       espera = False
            else:
                os.system('cls')
                print("A partida já vai começar! Sorteando quem vai começar!")

            time.sleep(1)
            suavez = False
            oponente = False
            jogando = False
            init = clientsocket.recv(5000).decode().split(' ', 1)
            if (init[0] == '1'):
                os.system('cls')
                print("Você começa o jogo!")
                print("Sua letra é", init[1])
                time.sleep(1)
                suavez = True
                jogando = True
            else:
                os.system('cls')
                print("O outro jogador vai começar!")
                print("Sua letra é", init[1])
                time.sleep(1)
                oponente = True
                jogando = True

            while jogando:
                while suavez:
                    tab = clientsocket.recv(20000)
                    tabuleiro = json.loads(tab.decode())
                    os.system('cls')
                    print("Sua vez!")
                    print("Sua letra é", init[1])
                    drawTabuleiro(tabuleiro)
                    letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')  
                    clientsocket.send((letra + " " + numero).encode())

                    valid = clientsocket.recv(1024).decode()
                    if (valid == '0'):
                        os.system('cls')
                        print("Vez do oponente! Espere!")
                        clientsocket.send('3'.encode())
                        oponente = True
                        suavez = False
                    elif (valid == '2'):
                        os.system('cls')
                        print("Você Venceu!")
                        oponente = False
                        suavez = False
                        jogando = False
                    elif (valid == '3'):
                        os.system('cls')
                        print("Empate!")
                        oponente = False
                        suavez = False
                        jogando = False
                    else:
                        os.system('cls')
                        print("Posição inválida! Tente outra vez!")
                        print("Sua letra é", init[1])
                        time.sleep(0.5)
                        oponente = False
                        suavez = True   

                while oponente:
                    minhavez = clientsocket.recv(1024).decode()
                    if minhavez == '3':
                        oponente = False
                        suavez = True
                    elif minhavez == '4':
                        os.system('cls')
                        print("Você Perdeu!")
                        suavez = False
                        oponente = False
                        jogando = False
                    elif minhavez == '5':
                        os.system('cls')
                        print("Empate!")
                        suavez = False
                        oponente = False
                        jogando = False

        elif op == '0':
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