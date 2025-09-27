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
            print(f'Total de caixas no estoque: {gerenciar_total()}')

        elif aux1 == 2:
            quantidade = int(input('Digite a quantidade de caixas que deseja inserir: '))
            length = float(input('Digite o comprimento da caixa (m): '))
            width = float(input('Digite a largura da caixa (m): '))
            height = float(input('Digite a altura da caixa (m): '))
            material = str(input('Insira o material da caixa: '))

            volume_info = volume(length, width, height)
            if volume_info <= 15:
                tamanho_info = get_tamanho(length, width, height)
                material_info = get_material(material)

                for _ in range(quantidade):
                    inserir_caixa(tamanho_info, material_info)

                print(f'Caixas inseridas! Novo total: {gerenciar_total()}')

            elif volume_info > 15:
                print(f'A caixa com volume de {volume_info:.2f} m³ excede o limite máximo de 15 m³ e não será inserida.')

        elif aux1 == 3:
            quantidade = int(input('Digite a quantidade de caixas que deseja retirar: '))
            if quantidade > gerenciar_total():
                print(f'Você só tem {gerenciar_total()} caixas no estoque!')
            else:
                remover_caixas(quantidade)
                print(f'Caixas retiradas! Novo total: {gerenciar_total()}')

        else:
            print("Opção não reconhecida.")

run_menu()






