import os
from random import randint

# Interface
def menu(): 
    menu = '''
|================================================|
|                 JOGO DA VELHA                  |
|================================================|
| 1 - 1 jogador                                  |
| 2 - 2 jogadores                                |
| 0 - Sair                                       |
|================================================|                             
    '''
    print(menu, end="")

def drawTabuleiro(tab):
    tabuleiro = '''
|================================================|
|                                                |
|                 A     B     C                  |
|              +-----+-----+-----+               |
|          1   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|          2   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|          3   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|                                                |
|================================================|
    ''' .format(tab[0][0], tab[0][1], tab[0][2], tab[1][0], tab[1][1], tab[1][2], tab[2][0], tab[2][1], tab[2][2])
    
    print(tabuleiro)

# Gera uma matriz 3x3 
def gerarTabuleiro():
    tabuleiro = [ [' ' for i in range(3)] for j in range(3)]
    return tabuleiro

# Escolhe aleatoriamente a key do jogador
def jogador():
    return 'X' if randint(1, 2) == 1 else 'O'

# Transforma as letras no index correto.  
# Diminui 1 do número, pois a matriz é de 0-3 
def editInput(letra, numero):
    if (letra == "A" or letra == 'a'):
        letra = 0
    elif (letra == "B" or letra == 'b'):
        letra = 1
    elif (letra == "C" or letra == 'c'):
        letra = 2

    x = int(numero) - 1
    y = int(letra)

    return x, y

# Verifica se a posição que o usuário entrou está disponível.
def posicaoDisponivel(matriz, x, y): 
    disponivel = True

    if matriz[x][y] != ' ':
        disponivel = False
    return disponivel

# Atribui um X ou O à posição que o usuário jogou.
def jogada(matriz, pos, key):
    if posicaoDisponivel(matriz, pos[0], pos[1]):
        matriz[pos[0]][pos[1]] = str(key)
        return True
    else:
        return False

# Verifica se deu velha, a key é X ou O.
def velha(tabuleiro, key, x, y):
    jogando = True
    dp = 0
    ds = 0
    l1 = 0
    l2 = 0
    l3 = 0
    c1 = 0
    c2 = 0
    c3 = 0

    for i in range(3):
        # # # diagonal principal # # #
        if (tabuleiro[i][i] == key):
            dp += 1
    
        # # # diagonal secundária # # #
        if (tabuleiro[i][3-1-i] == key):
            ds += 1

        # # # linhas # # #
        if (x == 0):
            if (tabuleiro[0][i] == key):
                l1 += 1
        elif (x == 1):
            if (tabuleiro[1][i] == key):
                l2 += 1
        elif (x == 2):
            if (tabuleiro[2][i] == key):
                l3 += 1
    
        # # # colunas # # #
        if (y == 0):
            if (tabuleiro[i][0] == key):
                c1 += 1
        elif (y == 1):
            if (tabuleiro[i][1] == key):
                c2 += 1
        elif (y == 2):
            if (tabuleiro[i][2] == key):
                c3 += 1

    # # # Se o contador for == 3, deu velha # # #
    if (dp == 3 or ds == 3 or l1 == 3 or l2 == 3 or l3 == 3 or c1 == 3 or c2 == 3 or c3 == 3):
        jogando = False
    
    return jogando

# Se a soma for igual a 4 e não tiver ganhado, deu empate
def empate(tabuleiro, key):
    soma = 0
    for i in range(3):
        for j in range(3):
            if (tabuleiro[i][j] == key):
                soma += 1
    return soma

# Fica testando uma posição disponível, até retornar True
def automatico(matriz, key, key2):
    valid = ''

    x = randint(0, 2)
    y = randint(0, 2)

    print(x, y)
    
    if jogada(matriz, (x, y), key):
        print("há vaga")
        matriz[x][y] = str(key)
        if not (velha(matriz, str(key), x, y)):
            print("Automático Venceu!")
            valid = '2'
        elif (empate(matriz, key) == 4 and empate(matriz, key2) == 4):
            print("Empate!")
            valid = '3'
        else:
            valid = '0'
    else:
        valid = '1'
        
    return valid

# Menu Principal
# Gera o Tabuleiro e escolhe o jogador uma vez
# Pede a letra e o número até alguém vencer ou dá empate,
# então jogando = False 
def main():
    on = True
    tabuleiro = gerarTabuleiro()

    while on:
        menu()
        op = int(input("Escolha uma opção: "))

        # # # automático # # #
        if (op == 1):
            jogando = True
            valid = True
            key = 'O'

            os.system('cls')
            while jogando:
                drawTabuleiro(tabuleiro)
                try:
                    if (valid):
                        letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')
                        x, y = editInput(letra, numero)
                        valid = False

                        if not (jogada(tabuleiro, (x, y), key)):
                            os.system('cls')
                            print('Posição inválida! Tente outra vez')
                            valid = True
                        else:
                            os.system('cls')
                            valid = automatico(tabuleiro, 'X')
                    
                    if not (velha(tabuleiro, key, x, y)):
                        os.system('cls')
                        drawTabuleiro(tabuleiro)
                        print("Você venceu!")
                        jogando = False
                    elif (empate(tabuleiro, key) == 4):
                        os.system('cls')
                        drawTabuleiro(tabuleiro)
                        print("Empate!")
                        jogando = False
                            
                except ValueError:
                    os.system('cls')
                    print("Entre com um a sequência de valores corretos!")
                    valid = True

        # # # 2 jogadores # # #
        elif (op == 2):
            jogando = True

            os.system('cls')
            while jogando:
                drawTabuleiro(tabuleiro)
                try:
                    key = jogador()
                    print(key)

                    letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')
                    x, y = editInput(letra, numero)

                    if not (jogada(tabuleiro, (x, y), key)):
                        os.system('cls')
                        print('Posição inválida! Tente outra vez')
                    else :
                        os.system('cls')
                        # no else tem q passar a vez

                    if not (velha(tabuleiro, key, x, y)):
                        os.system('cls')
                        drawTabuleiro(tabuleiro)
                        print("Você venceu!")
                        jogando = False
                    elif (empate(tabuleiro, key) == 4):
                        os.system('cls')
                        drawTabuleiro(tabuleiro)
                        print("Empate!")
                        jogando = False
                            
                except ValueError:
                    os.system('cls')
                    print("Entre com um a sequência de valores corretos!")

        # # # Sair # # # 
        elif (op == 0):
            on = False
        else:
            os.system('cls')
            print(" \nOpção inválida! Tente novamente.")