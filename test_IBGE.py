import unittest
from unittest.mock import patch, Mock, MagicMock
from IBGE import RepositorioIBGE
import requests
import requests.exceptions



class TestRepositorioIBGE(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioIBGE()
        self.repositorio.cache = MagicMock()
        self.repositorio.cache.verificar_conexao = MagicMock(return_value=True)
        self.repositorio.cache.get.return_value = 'Teste_valor'

    def test_consumir_cache_com_dados(self):
        resultado = self.repositorio.consumir_cache('chave_teste')
        self.assertEqual(resultado, 'Teste_valor')

    @patch("IBGE.requests.Session.get")
    def test_consumir_API_sem_parametros(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"Any": "any"}]
        mock_get.return_value = mock_response

        instancia = RepositorioIBGE()
        resultado = instancia.obter_ranking([None])

        mock_get.assert_called_once_with("https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking", params={})
        self.assertEqual(resultado, [{"Any": "any"}])

    @patch("IBGE.requests.Session.get")
    def test_consumir_API_parametro_sem_nome(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"localidade": "MG", "sexo": "M"}]
        mock_get.return_value = mock_response

        instancia = RepositorioIBGE()
        resultado = instancia.obter_ranking(nome=[None],localidade="MG", sexo="M")

        mock_get.assert_called_once_with("https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking", params={"localidade": "MG", "sexo": "M"})
        self.assertEqual(resultado, [{"localidade": "MG", "sexo": "M"}])

    def test_ler_arquivo_json_sucesso(self):
        teste = ["vinicius", "erika", "reinilson", "manoela", "alisson"]
        resultado = self.repositorio.ler_arquivo_json("teste.json")
        self.assertEqual(resultado, teste)

    def test_ler_arquivo_json_arquivo_inexistente(self):
        repositorio = RepositorioIBGE()
        resultado = repositorio.ler_arquivo_json('arquivo_inexistente.json')
        self.assertTrue("Ocorreu um erro:" in resultado)

    def test_obter_ranking_cache_conectado_dados_disponiveis(self):
        self.repositorio.cache.verificar_conexao.return_value = True
        with patch.object(self.repositorio, 'consumir_cache', return_value={"data": "cached_data"}):
            resultado = self.repositorio.obter_ranking("João")
            self.assertEqual(resultado, {"data": "cached_data"})

    def test_obter_ranking_cache_conectado_dados_indisponiveis(self):
        self.repositorio.cache.verificar_conexao.return_value = True
        with patch.object(self.repositorio, 'consumir_cache', return_value=None):
            with patch.object(self.repositorio, 'consumir_API', return_value={"data": "api_data"}):
                resultado = self.repositorio.obter_ranking("João")
                self.assertEqual(resultado, {"data": "api_data"})

    def test_obter_ranking_cache_desconectado(self):
        repositorio = RepositorioIBGE()
        repositorio.consumir_API = Mock()
        repositorio.cache.verificar_conexao = Mock()
        repositorio.cache.verificar_conexao.return_value = False
        repositorio.consumir_API.return_value = {"data": "api_data"}

        resultado = repositorio.obter_ranking("João")

        self.assertEqual(resultado, {"data": "api_data"})

    def test_construir_API_com_nome(self):
        nome = ["João"]
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/João"
        url_resultante = self.repositorio.construir_API(nome)
        self.assertEqual(url_resultante, url_esperada)

    def test_construir_API_sem_nomes(self):
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking"
        url_resultante = self.repositorio.construir_API([None])
        self.assertEqual(url_resultante, url_esperada)

    def test_obter_informacoes_estado_exception(self):
        with patch.object(self.repositorio.sessao, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("HTTP Request Error")
            with self.assertRaises(requests.exceptions.RequestException) as context:
                self.repositorio.obter_informacoes_estado('SP')
            self.assertEqual(str(context.exception), "HTTP Request Error")

    def test_consumir_API_exception(self):
        with patch.object(self.repositorio.sessao, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("HTTP Request Error")
            with self.assertRaises(requests.exceptions.RequestException) as context:
                self.repositorio.consumir_API('Joao')
            self.assertEqual(str(context.exception), "HTTP Request Error")


if __name__ == "__main__":
    unittest.main()
