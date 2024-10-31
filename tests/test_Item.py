import unittest
from src.Item import Item


class TestItem(unittest.TestCase):
    """
    Suíte de testes para a classe Item, cobrindo todos os métodos e vários cenários.

    Cada método de teste inclui uma docstring explicando o propósito do teste.
    """

    def test_init_com_frequencia(self):
        """
        Testa a inicialização do Item com a frequência fornecida diretamente.
        """
        item = Item(nome='João', sexo='M', localidade='33', frequencia=1000, decada=2000)
        self.assertEqual(item.nome, 'João')
        self.assertEqual(item.sexo, 'M')
        self.assertEqual(item.localidade, '33')
        self.assertEqual(item.frequencia, 1000)
        self.assertEqual(item.decada, 2000)

    def test_init_com_resposta_api(self):
        """
        Testa a inicialização do Item com 'resposta_api' fornecida; frequência calculada a partir dela.
        """
        resposta_api = [
            {"periodo": "[2000,2010[", "frequencia": 500},
            {"periodo": "[2010,2020[", "frequencia": 300}
        ]
        item = Item(nome='Maria', sexo='F', localidade='35', resposta_api=resposta_api, decada=2000)
        self.assertEqual(item.nome, 'Maria')
        self.assertEqual(item.sexo, 'F')
        self.assertEqual(item.localidade, '35')
        self.assertEqual(item.frequencia, 500)
        self.assertEqual(item.decada, 2000)

    def test_init_com_resposta_api_sem_decada(self):
        """
        Testa a inicialização do Item com 'resposta_api' fornecida, sem especificar a década.
        A frequência deve ser a soma total.
        """
        resposta_api = [
            {"periodo": "[2000,2010[", "frequencia": 500},
            {"periodo": "[2010,2020[", "frequencia": 300}
        ]
        item = Item(nome='Ana', sexo='F', localidade='35', resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 800)  # Frequência total

    def test_init_sem_frequencia_e_resposta_api(self):
        """
        Testa a inicialização do Item sem fornecer 'frequencia' ou 'resposta_api'.
        Deve lançar ValueError.
        """
        with self.assertRaises(ValueError):
            Item(nome='Pedro')

    def test_get_unique_key(self):
        """
        Testa o método 'get_unique_key' para garantir que retorna o identificador único correto.
        """
        item = Item(nome='João', sexo='M', localidade='33', frequencia=1000, decada=2000)
        chave_esperada = 'João_33_M_2000'
        self.assertEqual(item.get_unique_key(), chave_esperada)

    def test_buscar_frequencia_com_decada(self):
        """
        Testa o método '_buscar_frequencia' quando a década é especificada.
        Deve retornar a frequência para a década especificada.
        """
        resposta_api = [
            {"periodo": "[1990,2000[", "frequencia": 400},
            {"periodo": "[2000,2010[", "frequencia": 600}
        ]
        item = Item(nome='Carlos', decada=2000, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 600)

    def test_buscar_frequencia_sem_decada(self):
        """
        Testa o método '_buscar_frequencia' quando a década é None.
        Deve somar todas as frequências.
        """
        resposta_api = [
            {"periodo": "[1990,2000[", "frequencia": 400},
            {"periodo": "[2000,2010[", "frequencia": 600}
        ]
        item = Item(nome='Carlos', resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 1000)

    def test_buscar_frequencia_decada_nao_encontrada(self):
        """
        Testa o método '_buscar_frequencia' quando a década especificada não é encontrada em 'resposta_api'.
        Deve retornar 0.
        """
        resposta_api = [
            {"periodo": "[1990,2000[", "frequencia": 400}
        ]
        item = Item(nome='Luiza', decada=2000, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 0)

    def test_buscar_frequencia_resposta_api_invalida(self):
        """
        Testa o método '_buscar_frequencia' quando 'resposta_api' é None.
        Deve lançar ValueError.
        """
        with self.assertRaises(ValueError):
            Item(nome='Pedro', resposta_api=None)

    def test_exibir_informacoes(self):
        """
        Testa o método 'exibir_informacoes' para garantir que retorna a string formatada corretamente.
        """
        item = Item(nome='João', sexo='M', localidade='SP', frequencia=1000, decada=2000)
        saida_esperada = f"João              SP            M            2000            1000"
        self.assertEqual(item.exibir_informacoes(), saida_esperada)

    def test_exibir_informacoes_com_valores_none(self):
        """
        Testa o método 'exibir_informacoes' quando alguns atributos são None.
        Deve lidar com valores None adequadamente.
        """
        item = Item(nome='Ana', frequencia=500)
        saida_esperada = f"Ana               {'':<14}{'-':<13}{'Geral':<16}500"
        self.assertEqual(item.exibir_informacoes(), saida_esperada)

    def test_exibir_informacoes_localidade_dict(self):
        """
        Testa 'exibir_informacoes' quando 'localidade' é um dicionário com a chave 'sigla'.
        """
        item = Item(nome='Maria', sexo='F', localidade={'sigla': 'RJ'}, frequencia=800, decada=1990)
        saida_esperada = f"Maria             RJ            F            1990            800"
        self.assertEqual(item.exibir_informacoes(), saida_esperada)

    def test_decada_antes_de_1930(self):
        """
        Testa '_buscar_frequencia' quando a década é antes de 1930.
        Deve verificar o período '1930['.
        """
        resposta_api = [
            {"periodo": "1930[", "frequencia": 200},
            {"periodo": "[1930,1940[", "frequencia": 300}
        ]
        item = Item(nome='Antônio', decada=1920, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 200)

    def test_decada_exata_1930(self):
        """
        Testa '_buscar_frequencia' quando a década é exatamente 1930.
        Deve encontrar o período '[1930,1940['.
        """
        resposta_api = [
            {"periodo": "1930[", "frequencia": 200},
            {"periodo": "[1930,1940[", "frequencia": 300}
        ]
        item = Item(nome='Antônio', decada=1930, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 300)

    def test_decada_nao_em_resposta_api(self):
        """
        Testa '_buscar_frequencia' quando a década não está em 'resposta_api'.
        Deve retornar 0.
        """
        resposta_api = [
            {"periodo": "[1940,1950[", "frequencia": 400}
        ]
        item = Item(nome='José', decada=1930, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 0)


    def test_init_com_nome_none(self):
        """
        Testa a inicialização do Item com 'nome' como None.
        Deve permitir 'nome' como None.
        """
        item = Item(nome=None, frequencia=1000)
        self.assertIsNone(item.nome)

    def test_buscar_frequencia_resposta_api_none(self):
        """
        Testa o método _buscar_frequencia quando 'resposta_API' é None.
        Deve levantar ValueError.
        """
        item = Item(nome='Teste', decada=2000, resposta_api=[])
        with self.assertRaises(ValueError):
            item._buscar_frequencia(None)

    def test_buscar_frequencia_continue_executado(self):
        """
        Testa o cenário onde o 'continue' é executado dentro do loop em '_buscar_frequencia'.
        """
        resposta_api = [
            {"periodo": "[1940,1950[", "frequencia": 400},
            {"periodo": "[1950,1960[", "frequencia": 500}
        ]
        item = Item(nome='Teste', decada=1920, resposta_api=resposta_api)
        self.assertEqual(item.frequencia, 0)

    def test_init_com_frequencia_negativa(self):
        """
        Testa a inicialização do Item com frequência negativa.
        Deve aceitar frequências negativas.
        """
        item = Item(nome='João', frequencia=-1000)
        self.assertEqual(item.frequencia, -1000)

    def test_get_unique_key_com_valores_none(self):
        """
        Testa 'get_unique_key' quando alguns atributos são None.
        Deve lidar com valores None na chave.
        """
        item = Item(nome='Ana', frequencia=500)
        chave_esperada = 'Ana_None_None_None'
        self.assertEqual(item.get_unique_key(), chave_esperada)

if __name__ == '__main__':
    unittest.main()
