import unittest
from Item import Item
from unittest.mock import Mock,patch
from Ranking import Ranking
import sys
import os
import json
from io import StringIO


class TesteRanking(unittest.TestCase):

    def setUp(self):
        self.repositorio_ibge_mock = Mock()
        self.repositorio_ibge_mock.obter_ranking.return_value = [
            {'nome': 'JOAO', 'sexo': None, 'localidade': 'BR', 'res': [
                {'periodo': '1930[', 'frequencia': 60155}, {'periodo': '[1930,1940[', 'frequencia': 141772},
                {'periodo': '[1940,1950[', 'frequencia': 256001},
                {'periodo': '[1950,1960[', 'frequencia': 396438}, {'periodo': '[1960,1970[', 'frequencia': 429148},
                {'periodo': '[1970,1980[', 'frequencia': 279975},
                {'periodo': '[1980,1990[', 'frequencia': 273960}, {'periodo': '[1990,2000[', 'frequencia': 352552},
                {'periodo': '[2000,2010[', 'frequencia': 794118}]}]
        self.repositorio_ibge_mock.obter_informacoes_estado.return_value = {"id":31,"sigla":"MG","nome":"Minas Gerais","regiao":{"id":3,"sigla":"SE","nome":"Sudeste"}}
        self.ranking = Ranking(self.repositorio_ibge_mock)
        self.nome = "João"
        self.localidade = 31
        self.sexo = "M"
        self.decada = 1990
        self.frequencia = 5000

    def test_ordenar_ranking(self):
        repositorio_ibge_mock = Mock()
        ranking = Ranking(repositorio_ibge_mock)

        item1 = Item(nome="João", frequencia=5000)
        item2 = Item(nome="Maria", frequencia=10000)
        item3 = Item(nome="Ana", frequencia=3000)

        ranking.itens = [item1, item2, item3]

        ranking.ordenar_ranking()

        self.assertEqual(ranking.itens[0].nome, "Maria")
        self.assertEqual(ranking.itens[0].frequencia, 10000)
        self.assertEqual(ranking.itens[1].nome, "João")
        self.assertEqual(ranking.itens[1].frequencia, 5000)
        self.assertEqual(ranking.itens[2].nome, "Ana")
        self.assertEqual(ranking.itens[2].frequencia, 3000)

    def test_exportar_para_json(self):
        repositorio_ibge_mock = Mock()
        ranking = Ranking(repositorio_ibge_mock)

        item_teste = Item(nome="João", sexo="M", localidade="BR", decada=1990, frequencia=5000)
        ranking.itens.append(item_teste)

        nome_arquivo_teste = "teste_ranking.json"
        ranking.exportar_para_json(nome_arquivo_teste)

        self.assertTrue(os.path.exists(nome_arquivo_teste))

        with open(nome_arquivo_teste, "r") as arquivo:
            dados = json.load(arquivo)
            self.assertEqual(len(dados), 1)
            self.assertEqual(dados[0]["nome"], "João")
            self.assertEqual(dados[0]["sexo"], "M")
            self.assertEqual(dados[0]["localidade"], "BR")
            self.assertEqual(dados[0]["decada"], 1990)
            self.assertEqual(dados[0]["frequencia"], 5000)
        os.remove(nome_arquivo_teste)

    @patch('IBGE.RepositorioIBGE.obter_ranking')
    def teste_processar_resposta(self, mock_obter_ranking):
        mock_obter_ranking.return_value = [
            {"nome": "João", "res": "algum_dado", "frequencia": 100},
            {"nome": "Maria", "res": "outro_dado", "frequencia": 200}
        ]
        args_simulados = (['João'], 'SP', 'M', 1990)
        self.ranking.processar_resposta(args_simulados)
        self.assertEqual(self.ranking.itens[0].nome, 'JOAO')

    def mock_exibir_informacoes(self):
        output = f"{self.nome:<15}{self.localidade:<15}{self.sexo:<15}{self.decada:<15}{self.frequencia}"
        return output

    def test_exibir_ranking_caminho_feliz(self):
        item = self.ranking._criar_item(nome=self.nome, localidade=self.localidade, sexo=self.sexo, decada=self.decada, frequencia=self.frequencia)
        item.exibir_informacoes = self.mock_exibir_informacoes
        self.ranking.itens.append(item)
        original_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        self.ranking.exibir_ranking()
        sys.stdout = original_stdout
        resultado = buffer.getvalue()
        self.assertIn(self.nome, resultado, "O nome 'João' deve estar presente na saída do ranking.")

    def test_exibir_ranking_caminho_triste(self):
        self.ranking.itens = []
        resultado = self.ranking.exibir_ranking()
        mensagem_esperada = "Ranking vazio."
        self.assertEqual(resultado, mensagem_esperada, "A saída deve indicar um ranking vazio.")


if __name__ == "__main__":
    unittest.main()
