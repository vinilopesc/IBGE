import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import logging


class RepositorioIBGE:
    """
    Classe responsável por interagir com a API do Instituto Brasileiro de Geografia e Estatística (IBGE),
    fornecendo métodos para obter informações sobre nomes, rankings e detalhes de estados brasileiros.

    Esta classe encapsula operações para construir endpoints apropriados,
    realizar requisições HTTP e tratar as respostas da API do IBGE.
    """

    def __init__(self):
        """
        Inicializa uma instância de RepositorioIBGE, configurando uma sessão HTTP com políticas de reconexão
        para garantir resiliência em caso de falhas temporárias na conexão.

        Atributos:
            sessao (requests.Session): Sessão HTTP configurada para reutilização de conexões e políticas de reconexão.
            url (str): URL base da API do IBGE.
        """
        politica_reconexao = Retry(total=3, backoff_factor=1)
        adaptador = HTTPAdapter(max_retries=politica_reconexao)

        self.sessao = requests.Session()
        self.sessao.mount("https://", adaptador)
        self.sessao.timeout = 5
        self.url = "https://servicodados.ibge.gov.br/api/"

    def construir_API(self, nomes):
        """
        Constrói o endpoint da API do IBGE com base nos nomes fornecidos.

        Args:
            nomes (list of str): Lista de nomes para construir o endpoint da API.

        Returns:
            str: Endpoint da API construído para a consulta dos nomes fornecidos.

        Exemplos:
            - Se 'nomes' for [None], retorna o endpoint para o ranking geral de nomes.
            - Se 'nomes' for ['Maria', 'José'], retorna o endpoint específico para esses nomes.
        """
        if len(nomes) == 1 and nomes[0] is None:
            return self.url + "v2/censos/nomes/ranking"
        else:
            nomes_concatenados = "|".join(nomes)
            return self.url + f"v2/censos/nomes/{nomes_concatenados}"

    def consumir_API(self, nomes=None, localidade=None, sexo=None, decada=None):
        """
        Realiza uma consulta à API do IBGE, retornando o ranking ou a frequência de nomes
        com base nos parâmetros fornecidos.

        Args:
            nomes (list of str, opcional): Lista de nomes para consulta. Se None, obtém o ranking geral.
            localidade (str, opcional): ID numérico da localidade (estado) para filtrar a consulta. Se None, considera todo o Brasil.
            sexo (str, opcional): Sexo ('M', 'F' ou '-') para filtrar a consulta. Se None, considera ambos os sexos.
            decada (int, opcional): Década (formato YYYY) para filtrar a consulta. Se None, considera todas as décadas.

        Returns:
            list of dict: Lista de dicionários com os dados retornados pela API.

        Raises:
            requests.exceptions.HTTPError: Se a resposta HTTP indicar um erro.
            Exception: Para outros erros durante a solicitação HTTP.

        Exemplo de Resposta:
            [
                {
                    "nome": "Maria",
                    "localidade": "1",
                    "res": [
                        {"periodo": "1930[", "frequencia": 12345},
                        {"periodo": "[2000,2010[", "frequencia": 6789},
                        ...
                    ]
                },
                ...
            ]
        """
        endpoint = self.construir_API(nomes)
        parametros = {"localidade": localidade, "sexo": sexo, "decada": decada}
        parametros = {chave: valor for chave, valor in parametros.items() if valor is not None}
        try:
            resposta = self.sessao.get(endpoint, params=parametros)
            resposta.raise_for_status()
            return resposta.json()
        except Exception as e:
            logging.error(f"Erro durante a solicitação HTTP: {str(e)}")
            raise

    def obter_ranking(self, nome=None, localidade=None, sexo=None, decada=None):
        """
        Obtém o ranking ou frequência de nomes diretamente da API, usando os parâmetros fornecidos.

        Args:
            nome (str ou list of str, opcional): Nome ou lista de nomes para a consulta. Se None, obtém o ranking geral.
            localidade (str, opcional): ID numérico da localidade (estado) para a consulta. Se None, considera todo o Brasil.
            sexo (str, opcional): Sexo ('M', 'F' ou '-') para a consulta. Se None, considera ambos os sexos.
            decada (int, opcional): Década (formato YYYY) para a consulta. Se None, considera todas as décadas.

        Returns:
            list of dict: Lista de dicionários com os dados retornados pela API.

        Exemplos:
            - `obter_ranking(nome='Maria', sexo='F', decada=2000)`
            - `obter_ranking(nome=['Maria', 'José'], localidade='33')`

        Raises:
            requests.exceptions.HTTPError: Se a resposta HTTP indicar um erro.
            Exception: Para outros erros durante a solicitação HTTP.
        """
        if nome is not None and not isinstance(nome, list):
            nomes = [nome]
        else:
            nomes = nome
        return self.consumir_API(nomes, localidade, sexo, decada)

    def obter_informacoes_estado(self, sigla_id):
        """
        Obtém informações detalhadas de um estado brasileiro a partir de sua sigla (e.g., 'SP') ou ID numérico.

        Args:
            sigla_id (str ou int): Sigla (duas letras) ou ID numérico do estado brasileiro.

        Returns:
            dict: Dicionário contendo as informações do estado, como 'id', 'nome', 'sigla', etc.

        Raises:
            requests.exceptions.HTTPError: Se a resposta HTTP indicar um erro.
            Exception: Para outros erros durante a solicitação HTTP.

        Exemplos:
            - `obter_informacoes_estado('SP')`
            - `obter_informacoes_estado(35)`
        """
        if isinstance(sigla_id, str):
            sigla_id = sigla_id.upper()

        try:
            endpoint = self.url + f"v1/localidades/estados/{sigla_id}"
            resposta = self.sessao.get(endpoint)
            resposta.raise_for_status()
            return resposta.json()
        except Exception as e:
            logging.error(f"Erro durante a solicitação HTTP: {str(e)}")
            raise
