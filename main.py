from tabuleiro import gerarTabuleiro, editInput, play, velha, drawTabuleiro

tabuleiro = gerarTabuleiro()

try:
    while True:
        drawTabuleiro(tabuleiro)
        
        letra, numero = input("Entre com uma letra (coluna) e um número (linha) separados por espaço: ").split(' ')

        x, y = editInput(letra, numero)

        if (play(tabuleiro, (x, y), 'X')):
            print('disponive')
        else:
            print('indisponive')

        velha(tabuleiro, 'X', x, y)
except KeyboardInterrupt as erro:
    print(erro)
