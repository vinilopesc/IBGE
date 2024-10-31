import json

class Ranking:
    """
    Classe responsável por gerenciar e manipular um ranking de nomes baseado em objetos da classe `Item`.
    Fornece funcionalidades para adicionar itens ao ranking, ordenar o ranking com base na frequência dos nomes
    e exibir os resultados formatados no console.

    Atributos:
        itens (list of Item): Lista que armazena os itens adicionados ao ranking.
    """

    def __init__(self):
        """
        Inicializa uma instância da classe Ranking, criando uma lista vazia para armazenar os itens do ranking.
        """
        self.itens = []

    def adicionar_item(self, item):
        """
        Adiciona um novo item ao ranking.

        Args:
            item (Item): Instância da classe `Item` a ser adicionada ao ranking.
        """
        self.itens.append(item)

    def ordenar_ranking(self):
        """
        Ordena os itens do ranking em ordem decrescente com base na frequência dos nomes.

        A ordenação é feita in-place, modificando a lista `self.itens` diretamente.
        """
        self.itens.sort(key=lambda item: item.frequencia, reverse=True)

    def exibir_ranking(self):
        """
        Exibe o ranking formatado no console, mostrando as informações de cada item em colunas alinhadas.

        O cabeçalho inclui as colunas:
            - Nome
            - Localidade
            - Sexo
            - Década
            - Frequência
        """
        cabecalho = f"{'Nome':<15}{'Localidade':<15}{'Sexo':<15}{'Década':<15}{'Frequência'}"
        print(cabecalho)
        print('-' * len(cabecalho))
        for item in self.itens:
            print(item.exibir_informacoes())
