from flask import Flask

total = int()

def Options():
    global total
    if aux1 == 1:
        print('Total: ', total)
    elif aux1 == 2:
        total += int(input('Digite a quantidade de caixas que deseja inserir: '))
        size()
        material()
    elif aux1 == 3:
        total -= int(input('Digite a quantidade de caixas que deseja retirar: '))


def size():
    length = float(input('Digite a comprimento da caixa(m): '))
    width = float(input('Digite a largura da caixa(m): '))
    height = float(input('Digite a altura da caixa(m): '))

def material():
    tipo = input('Insira o material da caixa: ')
    return tipo



while True:
    print('1. Ver total armazenado\n2. Inserir caixas \n3. Retirar caixas\n4. Sair')
    aux1 = int(input('Escolha uma opção: ')) 
    if aux1 == 4: 
        break
Options()