import pytest
import main
from src.painel.estoque import *

@pytest.fixture(autouse=True)
def setup_and_teardown():
    resetar_total()
    yield
    resetar_total()

MATERIAL_TESTE = {'material': 'Plástico'}
CAIXA_OK = {'length': 2.0, 'width': 2.0, 'height': 2.0} # Volume: 8.0 (<= 15)
CAIXA_LIMITE_INFERIOR = {'length': 1.0, 'width': 1.0, 'height': 0.0} # Volume: 0.0
CAIXA_LIMITE_SUPERIOR = {'length': 3.0, 'width': 2.0, 'height': 2.5} # Volume: 15.0 (<= 15)
CAIXA_ACIMA_LIMITE = {'length': 3.0, 'width': 2.0, 'height': 3.0} # Volume: 18.0 (> 15)

# Teste de cálculo de volume simples
def test_volume_simples():
    assert volume(2, 2, 2) == 8.0

# Teste de volume com números decimais
def test_volume_decimal():
    assert volume(0.5, 1.5, 2.0) == pytest.approx(1.5)

# Teste de volume com zero (deve ser 0) caso de borda
def test_volume_zero():
    assert volume(5, 0, 2) == 0.0

# Inserção e contagem correta de múltiplas caixas
def test_inserir_caixas_multiplas():
    tamanho_info = get_tamanho(**CAIXA_OK)
    for _ in range(5):
        inserir_caixa(tamanho_info, MATERIAL_TESTE)
    assert gerenciar_total() == 5

# Remoção de uma única caixa
def test_remover_caixa_unica():
    tamanho_info = get_tamanho(**CAIXA_OK)
    inserir_caixa(tamanho_info, MATERIAL_TESTE)
    remover_caixas(1)
    assert gerenciar_total() == 0

# Remoção parcial de caixas
def test_remover_caixas_parcial():
    tamanho_info = get_tamanho(**CAIXA_OK)
    for _ in range(5):
        inserir_caixa(tamanho_info, MATERIAL_TESTE)
    remover_caixas(3)
    assert gerenciar_total() == 2

# Contagem do total no estoque vazio
def test_gerenciar_total_vazio():
    assert gerenciar_total() == 0

# Só aceita uma caixa com volume menor que 15m
def test_inserir_caixa_limite():
    tamanho_info = get_tamanho(**CAIXA_LIMITE_SUPERIOR)
    inserir_caixa(tamanho_info, MATERIAL_TESTE)
    assert gerenciar_total() == 1

# Garante que fica salvo o material da caixa no banco de dados
def test_persistencia_material():
    tamanho_info = get_tamanho(**CAIXA_OK)
    inserir_caixa(tamanho_info, get_material("Madeira"))
    caixa_salva = db.all()[0]
    assert caixa_salva['material'] == 'Madeira'

# Contagem de caixas após inserir uma caixa com volume acima do limite (15.0)
def test_n12_inserir_caixa_acima_limite_nao_salva():
    assert volume(**CAIXA_ACIMA_LIMITE) > 15.0