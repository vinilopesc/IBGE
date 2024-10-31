import unittest
from unittest.mock import patch, Mock
from src.IBGE import RepositorioIBGE
import requests
import requests.exceptions
from urllib3.util import Retry


class TestRepositorioIBGE(unittest.TestCase):
    """
    Classe de teste para RepositorioIBGE, cobrindo todos os métodos principais.
    """

    def test_construir_API_com_nome_unico(self):
        """
        Testa se a URL é construída corretamente quando um único nome é fornecido.
        """
        repositorio = RepositorioIBGE()
        nomes = ["João"]
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/João"
        url_resultante = repositorio.construir_API(nomes)
        self.assertEqual(url_resultante, url_esperada)

    def test_construir_API_com_varios_nomes(self):
        """
        Testa se a URL é construída corretamente quando múltiplos nomes são fornecidos.
        """
        repositorio = RepositorioIBGE()
        nomes = ["João", "Maria", "José"]
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/João|Maria|José"
        url_resultante = repositorio.construir_API(nomes)
        self.assertEqual(url_resultante, url_esperada)

    def test_construir_API_sem_nomes(self):
        """
        Testa se a URL é construída corretamente quando nenhum nome é fornecido.
        """
        repositorio = RepositorioIBGE()
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking"
        url_resultante = repositorio.construir_API([None])
        self.assertEqual(url_resultante, url_esperada)

    @patch('src.IBGE.requests.Session.get')
    def test_consumir_API_sucesso(self, mock_get):
        """
        Testa o método consumir_API em um cenário de sucesso, verificando se retorna o resultado esperado.
        """
        repositorio = RepositorioIBGE()
        mock_response = Mock()
        expected_json = [{"nome": "João", "res": [{"periodo": "2000[", "frequencia": 1000}]}]
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = repositorio.consumir_API(nomes=["João"], localidade="33", sexo="M", decada=2000)
        self.assertEqual(resultado, expected_json)
        mock_get.assert_called_once()

    @patch('src.IBGE.requests.Session.get')
    def test_consumir_API_http_error(self, mock_get):
        """
        Testa o método consumir_API quando ocorre um erro HTTP.
        """
        repositorio = RepositorioIBGE()
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
        with self.assertRaises(requests.exceptions.HTTPError):
            repositorio.consumir_API(nomes=["João"])

    @patch('src.IBGE.requests.Session.get')
    def test_consumir_API_request_exception(self, mock_get):
        """
        Testa o método consumir_API quando ocorre uma exceção de requisição.
        """
        repositorio = RepositorioIBGE()
        mock_get.side_effect = requests.exceptions.RequestException("Request Exception")
        with self.assertRaises(requests.exceptions.RequestException):
            repositorio.consumir_API(nomes=["João"])

    @patch('src.IBGE.RepositorioIBGE.consumir_API')
    def test_obter_ranking_com_nome(self, mock_consumir_API):
        """
        Testa o método obter_ranking quando um nome é fornecido.
        """
        repositorio = RepositorioIBGE()
        expected_result = [{"nome": "Maria", "res": [{"periodo": "2000[", "frequencia": 1500}]}]
        mock_consumir_API.return_value = expected_result

        resultado = repositorio.obter_ranking(nome="Maria", sexo="F", decada=2000)
        self.assertEqual(resultado, expected_result)
        mock_consumir_API.assert_called_once_with(["Maria"], None, "F", 2000)

    @patch('src.IBGE.RepositorioIBGE.consumir_API')
    def test_obter_ranking_sem_nome(self, mock_consumir_API):
        """
        Testa o método obter_ranking quando nenhum nome é fornecido.
        """
        repositorio = RepositorioIBGE()
        expected_result = [{"nome": "Ranking Geral", "res": [{"periodo": "2000[", "frequencia": 5000}]}]
        mock_consumir_API.return_value = expected_result

        resultado = repositorio.obter_ranking()
        self.assertEqual(resultado, expected_result)
        mock_consumir_API.assert_called_once_with(None, None, None, None)

    @patch('src.IBGE.requests.Session.get')
    def test_obter_informacoes_estado_com_sigla(self, mock_get):
        """
        Testa o método obter_informacoes_estado fornecendo a sigla de um estado.
        """
        repositorio = RepositorioIBGE()
        mock_response = Mock()
        expected_json = {"id": 35, "nome": "São Paulo", "sigla": "SP"}
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = repositorio.obter_informacoes_estado("SP")
        self.assertEqual(resultado, expected_json)
        mock_get.assert_called_once_with("https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP")

    @patch('src.IBGE.requests.Session.get')
    def test_obter_informacoes_estado_com_id(self, mock_get):
        """
        Testa o método obter_informacoes_estado fornecendo o ID numérico de um estado.
        """
        repositorio = RepositorioIBGE()
        mock_response = Mock()
        expected_json = {"id": 33, "nome": "Rio de Janeiro", "sigla": "RJ"}
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = repositorio.obter_informacoes_estado(33)
        self.assertEqual(resultado, expected_json)
        mock_get.assert_called_once_with("https://servicodados.ibge.gov.br/api/v1/localidades/estados/33")

    @patch('src.IBGE.requests.Session.get')
    def test_obter_informacoes_estado_http_error(self, mock_get):
        """
        Testa o método obter_informacoes_estado quando ocorre um erro HTTP.
        """
        repositorio = RepositorioIBGE()
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
        with self.assertRaises(requests.exceptions.HTTPError):
            repositorio.obter_informacoes_estado("SP")

    @patch('src.IBGE.requests.Session.get')
    def test_obter_informacoes_estado_request_exception(self, mock_get):
        """
        Testa o método obter_informacoes_estado quando ocorre uma exceção de requisição.
        """
        repositorio = RepositorioIBGE()
        mock_get.side_effect = requests.exceptions.RequestException("Request Exception")
        with self.assertRaises(requests.exceptions.RequestException):
            repositorio.obter_informacoes_estado("SP")

    def test_construir_API_nomes_vazio(self):
        """
        Testa o método construir_API quando uma lista vazia de nomes é fornecida.
        """
        repositorio = RepositorioIBGE()
        nomes = []
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/"
        url_resultante = repositorio.construir_API(nomes)
        self.assertEqual(url_resultante, url_esperada)

    def test_construir_API_nomes_none(self):
        """
        Testa o método construir_API quando [None] é fornecido como nomes.
        """
        repositorio = RepositorioIBGE()
        url_esperada = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking"
        url_resultante = repositorio.construir_API([None])
        self.assertEqual(url_resultante, url_esperada)

    @patch('src.IBGE.requests.Session.get')
    def test_consumir_API_sem_parametros(self, mock_get):
        """
        Testa o método consumir_API sem parâmetros, verificando se retorna o resultado esperado.
        """
        repositorio = RepositorioIBGE()
        mock_response = Mock()
        expected_json = [{"nome": "Ranking Geral", "res": [{"periodo": "2000[", "frequencia": 5000}]}]
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = repositorio.consumir_API([None])
        self.assertEqual(resultado, expected_json)
        mock_get.assert_called_once()

    @patch('src.IBGE.requests.Session.get')
    def test_consumir_API_parametros_none(self, mock_get):
        """
        Testa o método consumir_API com todos os parâmetros como None.
        """
        repositorio = RepositorioIBGE()
        mock_response = Mock()
        expected_json = [{"nome": "Ranking Geral", "res": [{"periodo": "2000[", "frequencia": 5000}]}]
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        resultado = repositorio.consumir_API(nomes=[None], localidade=None, sexo=None, decada=None)
        self.assertEqual(resultado, expected_json)
        mock_get.assert_called_once()

    @patch('src.IBGE.requests.Session.get')
    def test_obter_informacoes_estado_parametro_invalido(self, mock_get):
        """
        Testa o método obter_informacoes_estado com um parâmetro inválido, esperando um erro HTTP.
        """
        repositorio = RepositorioIBGE()
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
        with self.assertRaises(requests.exceptions.HTTPError):
            repositorio.obter_informacoes_estado("ZZ")

    def test_timeout_configurado(self):
        """
        Verifica se o timeout da sessão está configurado corretamente.
        """
        repositorio = RepositorioIBGE()
        self.assertEqual(repositorio.sessao.timeout, 5)

    def test_url_base(self):
        """
        Verifica se a URL base da API está configurada corretamente.
        """
        repositorio = RepositorioIBGE()
        self.assertEqual(repositorio.url, "https://servicodados.ibge.gov.br/api/")

    def test_politica_reconexao_configurada(self):
        """
        Verifica se a política de reconexão está configurada corretamente na sessão.
        """
        repositorio = RepositorioIBGE()
        adapter = repositorio.sessao.get_adapter("https://")
        self.assertIsInstance(adapter.max_retries, Retry)
        self.assertEqual(adapter.max_retries.total, 3)
        self.assertEqual(adapter.max_retries.backoff_factor, 1)


if __name__ == "__main__":
    unittest.main()
