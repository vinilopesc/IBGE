class Item:
    """
    Representa um registro individual no ranking de nomes do IBGE, contendo informações detalhadas sobre o nome, frequência, localidade, sexo e década.

    Atributos:
        nome (str): Nome consultado.
        sexo (str ou None): Sexo associado ao nome ('M', 'F' ou '-'). Pode ser None se não especificado.
        localidade (str ou None): Localidade (ID ou sigla) onde o nome foi consultado. Pode ser None se não especificado.
        decada (int ou None): Década de referência para a frequência do nome. Pode ser None se não especificado.
        frequencia (int): Frequência do nome, calculada com base na resposta da API ou fornecida diretamente.
    """

    def __init__(self, nome, sexo=None, localidade=None, frequencia=None, resposta_api=None, decada=None):
        """
        Inicializa uma instância da classe Item com os dados fornecidos. Se a frequência não for fornecida, ela é calculada a partir da resposta da API.

        Args:
            nome (str): Nome consultado.
            sexo (str, opcional): Sexo associado ao nome ('M', 'F' ou '-'). Padrão é None.
            localidade (str, opcional): Localidade (ID ou sigla) onde o nome foi consultado. Padrão é None.
            frequencia (int, opcional): Frequência do nome. Se fornecida, será usada diretamente; caso contrário, será calculada a partir de `resposta_api`. Padrão é None.
            resposta_api (list de dict, opcional): Lista de dicionários contendo os dados de frequência retornados pela API do IBGE. Necessário se `frequencia` não for fornecida. Padrão é None.
            decada (int, opcional): Década de referência para a frequência do nome. Se None, a frequência total será calculada. Padrão é None.

        Raises:
            ValueError: Se `frequencia` e `resposta_api` não forem fornecidos.
        """
        self.nome = nome
        self.sexo = sexo
        self.localidade = localidade
        self.decada = decada
        if frequencia is not None:
            self.frequencia = frequencia
        elif resposta_api is not None:
            self.frequencia = self._buscar_frequencia(resposta_api)
        else:
            raise ValueError("É necessário fornecer 'frequencia' ou 'resposta_api' para calcular a frequência.")

    def get_unique_key(self):
        """
        Gera uma chave única baseada nos atributos do item, útil para identificação ou deduplicação.

        Returns:
            str: String única que combina `nome`, `localidade`, `sexo` e `decada`.
        """
        return f"{self.nome}_{self.localidade}_{self.sexo}_{self.decada}"

    def _buscar_frequencia(self, resposta_API):
        """
        Calcula a frequência do nome com base na resposta da API do IBGE.

        Args:
            resposta_API (list de dict): Lista de dicionários contendo os períodos e frequências retornados pela API.

        Returns:
            int: Frequência calculada do nome para a década especificada ou frequência total se a década não for especificada.

        Raises:
            ValueError: Se `resposta_API` for None ou não contiver os dados esperados.
        """
        if resposta_API is None:
            raise ValueError("A 'resposta_API' não pode ser None ao calcular a frequência.")

        if self.decada is None:
            return sum(periodo['frequencia'] for periodo in resposta_API)
        else:
            for periodo in resposta_API:
                if self.decada < 1930:
                    if periodo["periodo"] == '1930[':
                        return periodo['frequencia']
                    else:
                        continue  # Continua a busca até encontrar o período correto
                if periodo["periodo"] == f"[{self.decada},{self.decada + 10}[":
                    return periodo["frequencia"]
            return 0  # Retorna 0 se a década não for encontrada nos dados

    def exibir_informacoes(self):
        """
        Formata as informações do item para exibição em uma string legível, com colunas alinhadas.

        Returns:
            str: String formatada contendo `nome`, `localidade`, `sexo`, `decada` e `frequencia`.
        """
        if isinstance(self.localidade, dict):
            local = self.localidade.get('sigla', '')
        else:
            local = self.localidade or ''
        decada = self.decada if self.decada else "Geral"
        nome = self.nome
        sexo = self.sexo or '-'
        frequencia = self.frequencia
        return f"{nome:<18}{local:<14}{sexo:<13}{decada:<16}{frequencia}"
