import unittest
from src.Ranking import Ranking
from src.Item import Item
from unittest.mock import patch
import io

class TestRanking(unittest.TestCase):
    """
    Classe de testes para a classe Ranking, cobrindo todos os métodos.
    """

    def test_init(self):
        """
        Testa se o construtor (__init__) inicializa corretamente a lista de itens como vazia.
        """
        ranking = Ranking()
        self.assertEqual(ranking.itens, [])

    def test_adicionar_item(self):
        """
        Testa se o método adicionar_item adiciona um item ao ranking corretamente.
        """
        ranking = Ranking()
        item = Item(nome='João', frequencia=100)
        ranking.adicionar_item(item)
        self.assertIn(item, ranking.itens)
        self.assertEqual(len(ranking.itens), 1)

    def test_ordenar_ranking(self):
        """
        Testa se o método ordenar_ranking ordena os itens corretamente em ordem decrescente de frequência.
        """
        ranking = Ranking()
        item1 = Item(nome='Maria', frequencia=50)
        item2 = Item(nome='José', frequencia=150)
        item3 = Item(nome='Ana', frequencia=100)
        ranking.adicionar_item(item1)
        ranking.adicionar_item(item2)
        ranking.adicionar_item(item3)
        ranking.ordenar_ranking()
        self.assertEqual(ranking.itens[0], item2)  # Frequência 150
        self.assertEqual(ranking.itens[1], item3)  # Frequência 100
        self.assertEqual(ranking.itens[2], item1)  # Frequência 50

    def test_ordenar_ranking_frequencias_iguais(self):
        """
        Testa se o método ordenar_ranking mantém a ordem estável quando itens têm a mesma frequência.
        """
        ranking = Ranking()
        item1 = Item(nome='Carlos', frequencia=100)
        item2 = Item(nome='Pedro', frequencia=100)
        ranking.adicionar_item(item1)
        ranking.adicionar_item(item2)
        ranking.ordenar_ranking()
        # Verifica se a ordem original é mantida
        self.assertEqual(ranking.itens[0], item1)
        self.assertEqual(ranking.itens[1], item2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_ranking(self, mock_stdout):
        """
        Testa se o método exibir_ranking exibe o ranking formatado corretamente no console.
        """
        ranking = Ranking()
        item1 = Item(nome='João', sexo='M', localidade='SP', decada=1990, frequencia=100)
        item2 = Item(nome='Maria', sexo='F', localidade='RJ', decada=2000, frequencia=150)
        ranking.adicionar_item(item1)
        ranking.adicionar_item(item2)
        ranking.ordenar_ranking()
        ranking.exibir_ranking()
        output = mock_stdout.getvalue()
        cabecalho = f"{'Nome':<15}{'Localidade':<15}{'Sexo':<15}{'Década':<15}{'Frequência'}\n"
        separador = '-' * len(cabecalho.strip()) + '\n'
        linha_item2 = item2.exibir_informacoes() + '\n'  # item2 tem maior frequência
        linha_item1 = item1.exibir_informacoes() + '\n'
        expected_output = cabecalho + separador + linha_item2 + linha_item1
        self.assertEqual(output, expected_output)

    def test_exibir_ranking_sem_itens(self):
        """
        Testa se o método exibir_ranking funciona corretamente quando não há itens no ranking.
        """
        ranking = Ranking()
        ranking.exibir_ranking()
        output = io.StringIO()
        with patch('sys.stdout', new=output):
            ranking.exibir_ranking()
        expected_output = f"{'Nome':<15}{'Localidade':<15}{'Sexo':<15}{'Década':<15}{'Frequência'}\n" + '-' * 70 + '\n'
        self.assertEqual(output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
