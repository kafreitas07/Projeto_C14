from flask import Flask

total = int()

def Options():
    global total
    if aux1 == 1:
        print('Total: ', total)
    elif aux1 == 2:
        total += int(input('Digite a quantidade de pacotes que deseja inserir: '))
    elif aux1 == 3:
        total -= int(input('Digite a quantidade de pacotes que deseja retirar: '))

while True:
    print('1. Ver total armazenado\n2. Inserir pacotes \n3. Retirar pacote\n4. Sair')
    aux1 = int(input('Escolha uma opção: ')) 
    if aux1 == 4: 
        break
    Options()

