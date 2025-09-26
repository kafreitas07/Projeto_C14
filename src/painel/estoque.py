total = int()

def gerenciar_total(opcao, quantidade):
    global total
    if opcao == 1:
        return total
    elif opcao == 2:
        total += quantidade
        return total
    elif opcao == 3:
        total -= quantidade
        return total

def resetar_total():
    global total
    total = 0

def get_tamanho(length, width, height):
    return {'length': length, 'width': width, 'height': height}

def get_material(material):
    return {'material': material}