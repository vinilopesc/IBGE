import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from Redis import RedisCache
import logging
import json


class RepositorioIBGE:
    """
    Classe para acessar a API do Instituto Brasileiro de Geografia e Estatística (IBGE).
    Fornece métodos para obter informações sobre nomes, rankings e estados brasileiros.
    Implementa cache para melhorar a eficiência e reduzir a carga na API.
    """

    def __init__(self):
        """
        Inicializa a classe configurando a sessão HTTP com políticas de reconexão
        e prepara o cache para armazenar respostas da API.
        """
        politica_reconexao = Retry(total=3, backoff_factor=1)
        adaptador = HTTPAdapter(max_retries=politica_reconexao)

        self.cache = RedisCache()
        self.sessao = requests.Session()
        self.sessao.mount("https://", adaptador)
        self.sessao.timeout = 5
        self.url = "https://servicodados.ibge.gov.br/api/"

    def construir_API(self, nomes):
        """
        Constrói o endpoint da API do IBGE com base nos nomes fornecidos.

        Args:
            nomes (list): Lista de nomes para construir o endpoint da API.

        Returns:
            str: Endpoint da API construído para a consulta dos nomes fornecidos.
        """
        if len(nomes) == 1 and nomes[0] == None:
            return self.url + "v2/censos/nomes/ranking"
        else:
            nomes_concatenados = "|".join(nomes)
            return self.url + f"v2/censos/nomes/{nomes_concatenados}"

    def consumir_API(self, nomes=None, localidade=None, sexo=None, decada=None):
        """
        Realiza uma consulta à API do IBGE, retornando o ranking ou a frequência de nomes.

        Args:
            nomes (list, opcional): Lista de nomes para consulta.
            localidade (str, opcional): ID da localidade para filtrar a consulta.
            sexo (str, opcional): Sexo (M/F) para filtrar a consulta.
            decada (int, opcional): Década para filtrar a consulta.

        Returns:
            dict: Resposta da API em formato JSON com os dados solicitados.
        """
        endpoint = self.construir_API(nomes)
        parametros = {"localidade": localidade, "sexo": sexo, "decada": decada}
        parametros = {chave: valor for chave, valor in parametros.items() if valor is not None}
        try:
            resposta = self.sessao.get(endpoint, params=parametros)
            resposta.raise_for_status()
            return resposta.json()
        except Exception as e:
            logging.error(f"erro durante a solicitação HTTP: {str(e)}")
            raise

    def consumir_cache(self, cache_key):
        """
        Busca dados no cache usando a chave fornecida.

        Args:
            cache_key (str): Chave utilizada para buscar dados no cache.

        Returns:
            dict or None: Dados armazenados no cache ou None se não encontrados.
        """
        return self.cache.get(cache_key)

    def ler_arquivo_json(self,arquivo):
        """
        Lê um arquivo JSON e retorna seu conteúdo.

        Args:
            arquivo (str): Caminho do arquivo JSON a ser lido.

        Returns:
            dict: Conteúdo do arquivo JSON.
        """
        try:
            with open(arquivo, 'r') as arquivo:
                dados = json.load(arquivo)
            return dados
        except Exception as erro:
            return f"Ocorreu um erro: {erro}"

    def obter_ranking(self, nome=None, localidade=None, sexo=None, decada=None):
        """
        Obtém o ranking ou frequência de nomes, utilizando cache quando possível.

        Args:
            nome (str, opcional): Nome para a consulta.
            localidade (str, opcional): ID da localidade para a consulta.
            sexo (str, opcional): Sexo para a consulta.
            decada (int, opcional): Década para a consulta.

        Returns:
            dict: Resposta da API do IBGE contendo o ranking ou frequência dos nomes.
        """
        if self.cache.verificar_conexao():
            cache_key = f'{nome}:{localidade}:{sexo}:{decada}'
            resposta = self.consumir_cache(cache_key)
            if resposta:
                return resposta
            else:
                resposta = self.consumir_API(nome, localidade, sexo, decada)
                self.cache.set(cache_key, resposta)
                return resposta
        else:
            return self.consumir_API(nome, localidade, sexo, decada)

    def obter_informacoes_estado(self, sigla_id):
        """
        Obtém informações de um estado brasileiro a partir de sua sigla ou ID.

        Args:
            sigla_id (str): Sigla ou ID do estado brasileiro.

        Returns:
            dict: Informações sobre o estado consultado.
        """
        if isinstance(sigla_id, str):
            sigla_id = sigla_id.upper()

        try:
            endpoint = self.url + f"v1/localidades/estados/{sigla_id}"
            resposta = self.sessao.get(endpoint)
            return resposta.json()
        except Exception as e:
            logging.error(f"Erro durante a solicitação HTTP: {str(e)}")
            raise

