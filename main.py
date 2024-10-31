import argparse
import logging
from itertools import product
from multiprocessing import Pool
from time import time
import os
from src.IBGE import RepositorioIBGE
from src.Ranking import Ranking
from src.Item import Item
from src.Postgre import Postgre
import credenciais


class Main:
    """
    Classe principal que orquestra a interação com a API do IBGE para obter rankings de nomes.
    Responsável por processar os argumentos de entrada, preparar os parâmetros para consulta,
    executar as consultas em paralelo, coletar e armazenar os resultados, e exibir o ranking.

    Atributos:
        repositorio_ibge (RepositorioIBGE): Instância para acessar a API do IBGE.
        ranking (Ranking): Instância para gerenciar o ranking de nomes.
        postgre (Postgre): Instância para interagir com o banco de dados PostgreSQL.
        nomes_argumento (list): Lista de nomes recebidos como argumento de linha de comando.
        localidade_argumento (list): Lista de localidades recebidas como argumento.
        sexo_argumento (list): Lista de sexos recebidos como argumento.
        decada_argumento (list): Lista de décadas recebidas como argumento.
        nomes (list): Lista de listas de nomes processados.
        localidades (list): Lista de localidades processadas.
        sexos (list): Lista de sexos processados.
        decadas (list): Lista de décadas processadas.
    """

    def __init__(self):
        """
        Inicializa uma instância da classe Main, configurando o repositório IBGE,
        a classe Ranking e a conexão com o banco de dados PostgreSQL.
        """
        self.repositorio_ibge = RepositorioIBGE()
        self.ranking = Ranking()
        self.postgre = Postgre(
            host=credenciais.host,
            port=credenciais.port,
            database=credenciais.database,
            user=credenciais.user,
            password=credenciais.password
        )
        self.nomes_argumento = []
        self.localidade_argumento = []
        self.sexo_argumento = []
        self.decada_argumento = []
        self.nomes = []
        self.localidades = []
        self.sexos = []
        self.decadas = []

    def tratar_nome(self, nome):
        """
        Trata e formata o nome fornecido, capitalizando a primeira letra.

        Args:
            nome (str): O nome a ser tratado e formatado.

        Returns:
            str ou None: Nome tratado com a primeira letra em maiúscula,
            ou None se o nome for inválido.
        """
        if nome:
            nome = str(nome)
            return nome.capitalize()
        else:
            return None

    def tratar_sexo(self, sexo):
        """
        Valida e formata a entrada do sexo para 'M', 'F' ou '-'.

        Args:
            sexo (str): Letra representando o sexo.

        Returns:
            str: Sexo validado ('M', 'F' ou '-').

        Observações:
            - Se 'sexo' for None ou inválido, retorna '-'.
            - Converte a entrada para maiúsculas.
        """
        if sexo is None:
            return '-'
        sexo = sexo.upper()
        if sexo not in ["M", "F", "-"]:
            logging.error(f"A letra '{sexo}' não corresponde a nenhum sexo válido.")
            return '-'
        return sexo

    def tratar_localidade(self, localidade):
        """
        Valida e transforma a entrada da localidade em um ID numérico válido.

        Args:
            localidade (str): Sigla ou ID da localidade.

        Returns:
            str: ID da localidade validado ou 'BR' se não fornecido ou inválido.

        Observações:
            - Se 'localidade' for None, retorna 'BR' (Brasil).
            - Se 'localidade' for 'BR', retorna 'BR'.
            - Tenta obter o ID da localidade através da API do IBGE.
            - Se a localidade não for encontrada, retorna 'BR' e registra um erro.
        """
        if localidade is None:
            return "BR"
        elif localidade.upper() == "BR":
            return "BR"
        else:
            try:
                info_estado = self.repositorio_ibge.obter_informacoes_estado(localidade)
                if info_estado:
                    return str(info_estado["id"])
                else:
                    logging.error(f"Localidade com ID ou sigla '{localidade}' não encontrada.")
                    return "BR"
            except Exception as e:
                logging.error(f"Erro ao obter informações da localidade '{localidade}': {e}")
                return "BR"

    def tratar_decada(self, decada):
        """
        Valida e arredonda a década fornecida para o múltiplo de 10 mais próximo.

        Args:
            decada (str ou int): Década a ser arredondada.

        Returns:
            int ou None: Década arredondada para o início da década,
            ou None se a entrada for inválida.

        Observações:
            - Se 'decada' for None ou vazio, retorna None.
            - Converte 'decada' para inteiro e arredonda para baixo (ex: 1995 -> 1990).
            - Se a conversão falhar, registra um erro e retorna None.
        """
        if decada:
            try:
                decada_tratada = int(decada)
                decada_arredondada = decada_tratada // 10 * 10
                return decada_arredondada
            except ValueError:
                logging.error(f"Década inválida: '{decada}'")
                return None
        else:
            return None

    def args(self):
        """
        Configura e analisa os argumentos de linha de comando para o programa,
        armazenando-os nos atributos correspondentes.
        """
        parser = argparse.ArgumentParser(description="Ranking de Nomes do IBGE")
        parser.add_argument("--nomes", nargs='+', help="Nomes para gerar ranking")
        parser.add_argument("--local", nargs='+', help="Localidade para o ranking")
        parser.add_argument("--sexo", nargs='+', help="Sexo para o ranking ('M', 'F' ou '-')")
        parser.add_argument("--decada", nargs='+', help="Década para buscar o ranking (formato YYYY)")
        args = parser.parse_args()
        self.nomes_argumento = args.nomes
        self.localidade_argumento = args.local
        self.sexo_argumento = args.sexo
        self.decada_argumento = args.decada

    def tratar_args(self):
        """
        Processa os argumentos de linha de comando previamente analisados,
        aplicando as funções de tratamento e validando os dados.
        Prepara as listas de parâmetros para as consultas à API.
        """
        self.nomes = [[self.tratar_nome(nome) for nome in self.nomes_argumento or ['']]]
        self.localidades = [self.tratar_localidade(loc) for loc in self.localidade_argumento or ['BR']]
        self.sexos = [self.tratar_sexo(sexo) for sexo in self.sexo_argumento or ['-']]
        self.decadas = [self.tratar_decada(decada) for decada in self.decada_argumento or ['']]

    @staticmethod
    def processar_combinacao(combinacao):
        """
        Processa uma combinação específica de parâmetros para consultar a API do IBGE.

        Args:
            combinacao (tuple): Tupla contendo (nomes, localidade, sexo, decada).

        Returns:
            list of Item: Lista de objetos `Item` com os dados obtidos da API.

        Observações:
            - Se 'nomes' for [None], obtém o ranking geral.
            - Cada item retornado pela API é transformado em uma instância de `Item`.
        """
        nomes, localidade, sexo, decada = combinacao
        repositorio = RepositorioIBGE()
        try:
            resposta = repositorio.obter_ranking(nomes, localidade, sexo, decada)
            itens = []
            if len(nomes) == 1 and nomes[0] is None:
                for dado in resposta[0]["res"]:
                    item = Item(
                        nome=dado["nome"],
                        localidade=localidade,
                        sexo=sexo,
                        decada=decada,
                        frequencia=dado["frequencia"]
                    )
                    itens.append(item)
            else:
                for dado in resposta:
                    item = Item(
                        nome=dado["nome"],
                        sexo=sexo,
                        localidade=localidade,
                        decada=decada,
                        resposta_api=dado["res"]
                    )
                    itens.append(item)
            return itens
        except Exception as e:
            logging.error(f"Erro ao processar a combinação {combinacao}: {e}")
            return []

    def mult_ranking(self, nomes, localidades, sexos, decadas):
        """
        Executa consultas paralelas à API do IBGE para todas as combinações possíveis
        dos parâmetros fornecidos. Coleta todos os itens resultantes, elimina duplicatas
        e os insere no banco de dados em uma única operação.

        Args:
            nomes (list of list of str): Lista de listas de nomes a serem consultados.
            localidades (list of str): Lista de localidades (IDs ou 'BR') para a consulta.
            sexos (list of str): Lista de sexos ('M', 'F' ou '-') para a consulta.
            decadas (list of int): Lista de décadas (ex: 1990) para a consulta.

        Observações:
            - Utiliza multiprocessing para executar as consultas em paralelo.
            - Deduplica os itens em memória usando a chave única gerada por cada `Item`.
            - Armazena os itens únicos no ranking e no banco de dados.
        """
        combinacoes = list(product(nomes, localidades, sexos, decadas))
        num_processos = min(len(combinacoes), os.cpu_count())
        with Pool(processes=num_processos) as pool:
            todos_itens = pool.map(self.processar_combinacao, combinacoes)

        # Achatar a lista de listas em uma única lista
        itens_para_inserir = [item for sublist in todos_itens for item in sublist]

        # Deduplicar itens usando get_unique_key
        itens_unicos = {}
        for item in itens_para_inserir:
            chave = item.get_unique_key()
            if chave not in itens_unicos:
                itens_unicos[chave] = item
                self.ranking.adicionar_item(item)

        # Inserir todos os itens únicos no banco de dados de uma vez
        self.postgre.insert_data(list(itens_unicos.values()))


if __name__ == "__main__":
    start_time = time()
    main = Main()
    main.args()
    main.tratar_args()
    main.mult_ranking(main.nomes, main.localidades, main.sexos, main.decadas)
    main.ranking.ordenar_ranking()
    main.ranking.exibir_ranking()
    main.postgre.close()
    end_time = time()
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time} segundos")
