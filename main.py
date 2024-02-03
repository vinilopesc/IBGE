import argparse
import logging
from Ranking import Ranking
from IBGE import RepositorioIBGE
from itertools import product
from multiprocessing import Pool
from Item import Item
from time import time
import os



class Main:
    """
        Classe principal que interage com a API do IBGE para obter rankings de nomes.
        Inclui funcionalidades para tratar e processar dados, bem como para executar
        consultas paralelas usando multiprocessing.
    """
    def __init__(self):
        """
        Inicializa a classe Main configurando o repositório IBGE e a classe Ranking.
        """
        self.repositorio_ibge = RepositorioIBGE()
        self.ranking = Ranking()

    def tratar_nome(self, nome):
        """
        Trata e formata o nome fornecido, capitalizando-o.

        Args:
            nome (str): O nome a ser tratado e formatado.

        Returns:
            str: Nome tratado e formatado, ou None se inválido.
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
        """
        if sexo is None:
            return '-'
        if sexo == '-':
            return '-'
        else:
            sexo = sexo.upper()
            if len(sexo) != 1:
                logging.error("Digite apenas uma letra, M (Masculino) ou F (Feminino)")
                return '-'
            if sexo != "M" and sexo != "F":
                logging.error(f"A letra {sexo} não corresponde a nenhum sexo.")
                return '-'
            return sexo

    def tratar_localidade(self, localidade):
        """
        Valida e transforma a entrada da localidade em um ID numérico.

        Args:
            localidade (str): Sigla ou ID da localidade.

        Returns:
            str: ID da localidade validado ou 'BR' se não fornecido.
        """
        if localidade is None:
            return "BR"
        elif localidade == "BR":
            return localidade
        else:
            info_estado = self.repositorio_ibge.obter_informacoes_estado(localidade)
            if info_estado:
                return info_estado["id"]
            else:
                logging.error(f"Localidade com ID ou sigla {localidade} não encontrada.")
                return "BR"

    def tratar_decada(self, decada):
        """
        Arredonda a década fornecida para o múltiplo de 10 mais próximo.

        Args:
            decada (str): Década a ser arredondada.

        Returns:
            int: Década arredondada.
        """
        if decada:
            try:
                decada_tratada = int(decada)
                decada_arredondada = decada_tratada // 10 * 10
                return decada_arredondada
            except:
                logging.error("Erro ao tratar decada")
                return None

    def args(self):
        """
        Configura e analisa os argumentos de linha de comando para o programa.
        """

        parser = argparse.ArgumentParser(description="Ranking de Nomes do IBGE")
        parser.add_argument("--nomes", nargs='+', help="Nomes para gerar ranking")
        parser.add_argument("--local", nargs='+', help="Localidade para o ranking")
        parser.add_argument("--sexo", nargs='+', help="Sexo para o ranking")
        parser.add_argument("--decada", nargs='+', help="Decada para buscar o ranking")
        parser.add_argument("--json", nargs='?', help="Nomes recebidos por um arquivo json")
        args = parser.parse_args()
        self.nomes_argumento = args.nomes
        self.localidade_argumento = args.local
        self.sexo_argumento = args.sexo
        self.decada_argumento = args.decada
        self.nomes_json = args.json

    def tratar_args(self):
        """
        Processa os argumentos de linha de comando e os prepara para uso no programa.
        """
        if self.nomes_json:
            self.nomes = [self.repositorio_ibge.ler_arquivo_json(self.nomes_json)]
        else:
            self.nomes = [[self.tratar_nome(nome) for nome in self.nomes_argumento or ['']]]
        self.localidades = [self.tratar_localidade(loc) for loc in self.localidade_argumento or ['BR']]
        self.sexos = [self.tratar_sexo(sexo) for sexo in self.sexo_argumento or ['-']]
        self.decadas = [self.tratar_decada(decada) for decada in self.decada_argumento or ['']]

    @staticmethod
    def processar_combinacao(combinacao):
        """
        Processa uma combinação específica de parâmetros para consultar a API do IBGE.

        Args:
            combinacao (tuple): Combinação de nomes, localidade, sexo e década.

        Returns:
            list: Lista de itens `Item` com os dados obtidos da API.
        """
        nomes, localidade, sexo, decada = combinacao
        repositorio = RepositorioIBGE()
        resposta = repositorio.obter_ranking(nomes, localidade, sexo, decada)
        itens = []
        if len(nomes) == 1 and nomes[0] == None:
            for dado in resposta[0]["res"]:
                item = Item(dado["nome"], localidade=localidade, sexo=sexo, decada=decada, frequencia=dado["frequencia"])
                itens.append(item)
            return itens
        else:
            for dado in resposta:
                item = Item(nome=dado["nome"], sexo=sexo, localidade=localidade, decada=decada,resposta_api=dado["res"])
                itens.append(item)
            return itens

    def mult_ranking(self, nomes, localidades, sexos, decadas):
        """
        Executa consultas paralelas à API do IBGE para várias combinações de parâmetros.

        Args:
            nomes (list): Lista de nomes para a consulta.
            localidades (list): Lista de localidades para a consulta.
            sexos (list): Lista de sexos para a consulta.
            decadas (list): Lista de décadas para a consulta.
        """
        combinacoes = list(product(nomes, localidades, sexos, decadas))
        num_processos = os.cpu_count()
        with Pool(processes=num_processos) as pool:
            todos_itens = pool.map(self.processar_combinacao, combinacoes)
        for itens in todos_itens:
            for item in itens:
                self.ranking.adicionar_item(item)



if __name__ == "__main__":
    start_time = time()
    main = Main()
    main.args()
    main.tratar_args()
    main.mult_ranking(main.nomes, main.localidades, main.sexos, main.decadas)
    main.ranking.ordenar_ranking()
    main.ranking.exibir_ranking()
    main.ranking.exportar_para_json("ranking.json")
    end_time = time()
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time} segundos")
