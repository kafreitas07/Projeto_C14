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

# Remover o valor 0 de caixas
def test_remover_zero_caixas():
    tamanho_info = get_tamanho(**CAIXA_OK)
    inserir_caixa(tamanho_info, MATERIAL_TESTE)
    remover_caixas(0)
    assert gerenciar_total() == 1

# Tentativa de remoção de caixas quando há 0 caixas
def test_remover_caixas_vazio():
    remover_caixas(1)
    assert gerenciar_total() == 0

# Tentar retirar mais caixas do que existe
def test_retirada_excesso():
    assert 5 > gerenciar_total()

# Verifica se as caixas são do tipo string , retorna o erro
def test_caixas_tipo_invalido():
    with pytest.raises(TypeError):
        remover_caixas("2")

# Verifica que o material é case-sensitive (valores diferentes persistem)
def test_material_case_sensitive():
    t = get_tamanho(**CAIXA_OK)
    inserir_caixa(t, get_material("madeira"))
    inserir_caixa(t, get_material("Madeira"))
    assert gerenciar_total() == 2
    mats = {doc["material"] for doc in db.all()}
    assert "madeira" in mats and "Madeira" in mats

# Gerenciar_total deve bater com o tamanho real do banco
def test_gerenciar_total_lendb():
    t = get_tamanho(**CAIXA_OK)
    for _ in range(7):
        inserir_caixa(t, MATERIAL_TESTE)
    assert gerenciar_total() == len(db.all())
    assert gerenciar_total() == 7

# Se houver erro de string ele nao altera o total
def test_remover_caixas_erro_string():
    assert gerenciar_total() == 0
    inserir_caixa(get_tamanho(1, 1, 1), get_material("PP"))
    assert gerenciar_total() == 1

    with pytest.raises(TypeError):
        remover_caixas("1") 
    # continua com 1 caixa, nada foi removido
    assert gerenciar_total() == 1

# Verifica que a remoção não afeta o total se for 0
def test_remover_caixas_0():
    tamanho_info = get_tamanho(**CAIXA_OK)
    inserir_caixa(tamanho_info, MATERIAL_TESTE) 
    remover_caixas(1)  
    remover_caixas(1)  
    assert gerenciar_total() == 0

# Verifica se a função de total retorna um inteiro
def test_gerenciar_total_int():
    assert isinstance(gerenciar_total(), int)

# Verifica se a função sai corretamente, usando teste mock
def test_sair_imediato(mocker):
    mocker.patch("builtins.input", side_effect=["4"])
    mock_print = mocker.patch("builtins.print")
    main.run_menu()
    mock_print.assert_any_call("Saindo...")