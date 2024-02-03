class Item:
    """
    Representa um item no ranking de nomes do IBGE, contendo informações detalhadas.

    Atributos:
        nome (str): Nome da pessoa.
        sexo (str, opcional): Sexo da pessoa.
        localidade (str, opcional): Localidade de origem do nome.
        frequencia (int, opcional): Frequência do nome.
        decada (int, opcional): Década de referência para a frequência do nome.
    """
    def __init__(self, nome, sexo=None, localidade=None, frequencia=None,resposta_api=None, decada=None):
        """
        Inicializa um objeto Item com os dados fornecidos ou calcula a frequência com base na resposta da API.

        Args:
            nome (str): Nome da pessoa.
            sexo (str, opcional): Sexo da pessoa.
            localidade (str, opcional): Localidade de origem do nome.
            frequencia (int, opcional): Frequência do nome. Se não fornecida, é calculada usando resposta_api.
            resposta_api (list, opcional): Resposta da API do IBGE para calcular a frequência.
            decada (int, opcional): Década de referência para a frequência do nome.
        """
        self.nome = nome
        self.sexo = sexo
        self.localidade = localidade
        self.decada = decada
        self.frequencia = frequencia if frequencia else self._buscar_frequencia(resposta_api)

    def dicionario(self):
        """
        Converte as informações do item em um dicionário para fácil acesso e manipulação.

        Returns:
            dict: Dicionário contendo as informações do item.
        """
        return {
            "nome": self.nome,
            "sexo": self.sexo,
            "localidade": self.localidade,
            "decada": self.decada,
            "frequencia": self.frequencia
        }

    def _definir_nome(self, nome):
        """
        Valida o nome fornecido para garantir que não seja nulo ou vazio.

        Args:
            nome (str): Nome a ser validado.

        Returns:
            str: Nome validado.

        Raises:
            ValueError: Se o nome for nulo ou uma string vazia.
        """
        if nome is None or nome.strip() == "":
            raise AttributeError("Nome inválido.")
        return nome

    def _buscar_frequencia(self, resposta_API):
        """
        Calcula a frequência do nome com base na resposta da API do IBGE.

        Args:
            resposta_API (list): Resposta da API contendo dados de frequência.

        Returns:
            int: Frequência calculada do nome.
        """

        if self.decada is None:
            return sum(periodo['frequencia'] for periodo in resposta_API)
        else:
            for periodo in resposta_API:
                if self.decada < 1930:
                    if periodo["periodo"] == '1930[':
                        return periodo['frequencia']
                    else:
                        return 0
                if periodo["periodo"] == f"[{self.decada},{self.decada + 10}[":
                    return periodo["frequencia"]
            return 0

    def exibir_informacoes(self):
        """
        Formata as informações do item para exibição em uma string legível.

        Returns:
            str: String formatada com as informações do item.
        """
        if isinstance(self.localidade, dict):
            local = self.localidade['sigla']
        else:
            local = self.localidade
        if self.decada:
            decada = self.decada
        else:
            decada = "Geral"
        nome = self.nome
        sexo = self.sexo
        frequencia = self.frequencia
        return f"{nome:<18}{local:<14}{sexo:<13}{decada:<16}{frequencia}"

