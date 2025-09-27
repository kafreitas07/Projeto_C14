from tinydb import TinyDB
total = int()

db = TinyDB('estoque.json')

def inserir_caixa(tamanho_info, material_info):
    caixa_data = {**tamanho_info, **material_info}
    db.insert(caixa_data)

def remover_caixas(quantidade):
    docs_to_remove = db.all()[:quantidade]
    doc_ids_to_remove = [doc.doc_id for doc in docs_to_remove]
    db.remove(doc_ids=doc_ids_to_remove)

def gerenciar_total():
    total_caixas = len(db.all())
    return total_caixas

def volume(length, width, height):
    return length * width * height

def get_tamanho(length, width, height):
    return {'length': length, 'width': width, 'height': height}

def get_material(material):
    return {'material': material}

def resetar_total():
    db.truncate()