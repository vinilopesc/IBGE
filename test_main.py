import unittest
from Ranking import Ranking
from IBGE import RepositorioIBGE
from main import Main
from unittest.mock import Mock, patch, MagicMock
import argparse
from multiprocessing import Process


class TesteMain(unittest.TestCase):
    def setUp(self):
        self.IBGE = RepositorioIBGE()
        self.ranking = Ranking(self.IBGE)
        self.main = Main()

    def test_tratar_nome(self):
        assert self.main.tratar_nome("joão") == "João"
        assert self.main.tratar_nome("MARIA") == "Maria"
        assert self.main.tratar_nome("") is None
        assert self.main.tratar_nome(None) is None
        assert self.main.tratar_nome("123") == "123"
        assert self.main.tratar_nome("lucas") == "Lucas"

    def test_tratar_localidade(self):
        Fake_IBGE = Mock(RepositorioIBGE)
        Fake_IBGE.obter_informacoes_estado.return_value = {"id": 31, "sigla": "MG","nome": "Minas Gerais", "regiao": {"id": 3, "sigla": "SE", "nome": "Sudeste"}}
        assert self.main.tratar_localidade(None) == "BR"
        assert self.main.tratar_localidade("BR") == "BR"
        assert self.main.tratar_localidade("MG") == 31
        assert self.main.tratar_localidade("XX") == "BR"

    def test_tratar_decada(self):
        assert self.main.tratar_decada("1989") == 1980
        assert self.main.tratar_decada("2000") == 2000
        assert self.main.tratar_decada("1955") == 1950
        assert self.main.tratar_decada("abc") is None
        assert self.main.tratar_decada(None) is None
        assert self.main.tratar_decada("2022") == 2020

    def test_tratar_sexo(self):
        assert self.main.tratar_sexo("M") == "M"
        assert self.main.tratar_sexo("f") == "F"
        assert self.main.tratar_sexo("X") == "-"
        assert self.main.tratar_sexo(None) == "-"
        assert self.main.tratar_sexo("-") == "-"
        assert self.main.tratar_sexo("MF") == "-"

    @patch('argparse.ArgumentParser.parse_args')
    def teste_com_argumentos_validos(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(nomes=['João', 'Maria'], local=['SP', 'RJ'], sexo=['M', 'F'], decada=['1990', '2000'], json=None)

        instancia = self.main
        instancia.args()

        self.assertEqual(instancia.nomes_argumento, ['João', 'Maria'])
        self.assertEqual(instancia.localidade_argumento, ['SP', 'RJ'])
        self.assertEqual(instancia.sexo_argumento, ['M', 'F'])
        self.assertEqual(instancia.decada_argumento, ['1990', '2000'])
        self.assertIsNone(instancia.nomes_json)

    @patch('argparse.ArgumentParser.parse_args')
    def teste_tratar_args(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            nomes= ['Joao','Maria'],
            local=['SP', 'RJ'],
            sexo=['M', 'F'],
            decada=['1990', '2000'],
            json=None)
        self.main.args()
        self.main.tratar_args()
        self.assertEqual(self.main.nomes, [['Joao', "Maria"]])
        self.assertEqual(self.main.localidades, [35, 33])
        self.assertEqual(self.main.sexos, ['M', 'F'])
        self.assertEqual(self.main.decadas, [1990, 2000])

    @patch('main.Process', autospec=True)
    def teste_mult_ranking(self, mock_process):
        processo_mock = MagicMock(spec=Process)
        mock_process.return_value = processo_mock
        self.main.nomes = [['Vinicius'], ['Joao']]
        self.main.localidades = ['MG', 'SP']
        self.main.sexos = ['M', 'F']
        self.main.decadas = [1990, 2000]

        self.main.mult_ranking()

        self.assertEqual(mock_process.call_count,
                         len(self.main.nomes) * len(self.main.localidades) * len(self.main.sexos) * len(
                             self.main.decadas))
        processo_mock.start.assert_called()
        processo_mock.join.assert_called()


if __name__ == '__main__':
    unittest.main()