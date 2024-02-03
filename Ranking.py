import json


class Ranking:
    """
        Classe para gerenciar e manipular um ranking de nomes.
        Fornece funcionalidades para adicionar itens, ordenar o ranking,
        exportar os dados para um arquivo JSON e exibir o ranking.
    """
    def __init__(self):
        """
        Inicializa a classe Ranking criando uma lista vazia para armazenar os itens do ranking.
        """
        self.itens = []

    def adicionar_item(self, item):
        """
        Adiciona um novo item ao ranking.

        Args:
            item (Item): O item a ser adicionado ao ranking.
        """
        self.itens.append(item)

    def ordenar_ranking(self):
        """
        Ordena os itens do ranking em ordem decrescente com base na frequência.
        """
        self.itens.sort(key=lambda item: item.frequencia, reverse=True)

    def exportar_para_json(self, nome_arquivo="ranking.json"):
        """
        Exporta o ranking atual para um arquivo JSON.

        Args:
            nome_arquivo (str, opcional): Nome do arquivo JSON para salvar o ranking.
                                          Padrão é 'ranking.json'.
        """
        dados_exportados = [{
            "nome": item.nome,
            "localidade": item.localidade,
            "sexo": item.sexo,
            "decada": item.decada,
            "frequencia": item.frequencia
        } for item in self.itens]

        with open(nome_arquivo, "w") as arquivo:
            json.dump(dados_exportados, arquivo, indent=4)

    def exibir_ranking(self):
        """
        Exibe o ranking de forma formatada no console.
        """
        cabecalho = f"{'Nome':<15}{'Localidade':<15}{'Sexo':<15}{'Decada':<15}{'Frequencia'}\n"
        print(cabecalho)
        for item in self.itens:
            print(item.exibir_informacoes())

