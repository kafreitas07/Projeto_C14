from flask import Flask
from src.painel.estoque import *

def run_menu():
    while True:
        print('1. Ver total armazenado\n2. Inserir caixas \n3. Retirar caixas\n4. Sair')

        try:
            aux1 = int(input('Escolha uma opção:'))
        except ValueError:
            print('Opção inválida. Digite um número.')
            continue

        if aux1 == 4:
            print('Saindo...')
            break

        if aux1 == 1:
            total = gerenciar_total(1, 0)
            print(f'Total de caixas no estoque: {total}')

        elif aux1 == 2:
            quantidade = int(input('Digite a quantidade de caixas que deseja inserir: '))
            length = float(input('Digite o comprimento da caixa (m): '))
            width = float(input('Digite a largura da caixa (m): '))
            height = float(input('Digite a altura da caixa (m): '))
            material = str(input('Insira o material da caixa: '))

            novo_total = gerenciar_total(2, quantidade)
            tamanho_info = get_tamanho(length, width, height)
            material_info = get_material(material)

            print(f'Caixas inseridas! Novo total: {novo_total}')

        elif aux1 == 3:
            quantidade = int(input('Digite a quantidade de caixas que deseja retirar: '))
            novo_total = gerenciar_total(3, quantidade)

            print(f'Caixas retiradas! Novo total: {novo_total}')

        else:
            print("Opção não reconhecida.")

run_menu()






