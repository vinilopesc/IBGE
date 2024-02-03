import unittest
from unittest.mock import Mock,patch
from IBGE import RepositorioIBGE
import unittest
from Item import Item
from unittest.mock import patch, Mock

class TestItem(unittest.TestCase):

    def setUp(self):
        self.nome = "João"
        self.localidade = "BR"
        self.sexo = "M"
        self.decada = 1990
        self.frequencia = 1000
        self.repositorio_ibge_mock = Mock()
        self.resposta_api = [{"periodo":"1930[","frequencia":59996},{"periodo":"[1930,1940[","frequencia":141530},{"periodo":"[1940,1950[","frequencia":255582},
                            {"periodo":"[1950,1960[","frequencia":395857},{"periodo":"[1960,1970[","frequencia":428482},{"periodo":"[1970,1980[","frequencia":279445},
                            {"periodo":"[1980,1990[","frequencia":272896},{"periodo":"[1990,2000[","frequencia":350409},{"periodo":"[2000,2010[","frequencia":787738}]
        self.item = Item(nome=self.nome,localidade=self.localidade,sexo= self.sexo,decada=self.decada,frequencia=self.frequencia)

    def test_dicionario(self):
        esperado = {
            "nome": "João",
            "sexo": "M",
            "localidade": "BR",
            "decada": 1990,
            "frequencia": 1000
        }
        resultado = self.item.dicionario()
        self.assertEqual(resultado, esperado)

    def test_inicializacao_com_frequencia(self):
        self.assertEqual(self.item.nome, self.nome)
        self.assertEqual(self.item.localidade, self.localidade)
        self.assertEqual(self.item.sexo, self.sexo)
        self.assertEqual(self.item.decada, self.decada)
        self.assertEqual(self.item.frequencia, self.frequencia)

    def test_inicializacao_sem_frequencia(self):
        item = Item(nome=self.nome, sexo=self.sexo,localidade=self.localidade ,decada=self.decada, resposta_api=self.resposta_api)
        self.assertEqual(item.nome, self.nome)
        self.assertEqual(item.localidade, self.localidade)
        self.assertEqual(item.sexo, self.sexo)
        self.assertEqual(item.decada, self.decada)
        self.assertEqual(item.frequencia, 350409)

    def test_definir_nome_caminho_feliz(self):
        nome = "João"
        resultado = Item._definir_nome(self, nome)
        self.assertEqual(resultado, nome, "O nome definido deveria ser igual ao fornecido.")

    def test_definir_nome_caminho_triste_nome_vazio(self):
        nome = ""
        with self.assertRaises(AttributeError) as context:
            Item._definir_nome(self, nome)
        self.assertEqual(str(context.exception), "Nome inválido.")

    def test_definir_nome_caminho_triste_nome_none(self):
        nome = None
        with self.assertRaises(AttributeError) as context:
            Item._definir_nome(self, nome)
        self.assertEqual(str(context.exception), "Nome inválido.")

    def test_exibir_informacoes(self):
        item = Item(nome=self.nome, localidade=self.localidade, sexo=self.sexo, decada=self.decada,
                    frequencia=self.frequencia)
        info = item.exibir_informacoes()
        str(info)
        self.assertIn(self.nome, info)
        self.assertIn(self.localidade, info)
        self.assertIn(self.sexo, info)
        self.assertIn(str(self.decada), info)
        self.assertIn(str(self.frequencia), info)

    def test_exibir_informacoes_sem_decada(self):
        item = Item(nome=self.nome, localidade=self.localidade, sexo=self.sexo, decada=None,
                    frequencia=self.frequencia)
        info = item.exibir_informacoes()
        str(info)
        self.assertIn(self.nome, info)
        self.assertIn(self.localidade, info)
        self.assertIn(self.sexo, info)
        self.assertIn("Geral", info)
        self.assertIn(str(self.frequencia), info)

    def test_exibir_informacoes_com_local_dict(self):
        item = Item(nome=self.nome, localidade={"id": 31, "sigla": "MG", "nome": "Minas Gerais"}, sexo=self.sexo,decada=None,frequencia=self.frequencia)
        info = item.exibir_informacoes()
        esperado = f"{self.nome:<18}{'MG':<14}{self.sexo:<13}{'Geral':<16}{self.frequencia}"
        self.assertEqual(info, esperado)

    def test_soma_todas_frequencias(self):
        item_busca = Item(nome="Joao",sexo="M",localidade="BR",resposta_api=self.resposta_api)
        frequencia = item_busca._buscar_frequencia(resposta_API=self.resposta_api)
        self.assertEqual(frequencia,2971935)

    def test_busca_decada_especifica(self):
        item_busca = Item(nome="Joao",sexo="M",localidade="BR",resposta_api=self.resposta_api,decada=1930)
        frequencia = item_busca._buscar_frequencia(resposta_API=self.resposta_api)
        self.assertEqual(frequencia, 141530)

    def test_decada_anterior_1930(self):
        item_busca = Item(nome="Joao", sexo="M", localidade="BR", resposta_api=self.resposta_api, decada=1920)
        frequencia = item_busca._buscar_frequencia(resposta_API=self.resposta_api)
        self.assertEqual(frequencia, 59996)

    def test_decada_anterior_1930_nao_encontrada(self):
        resposta_api = [{"periodo":"[1930,1940[","frequencia":141530},{"periodo":"[1940,1950[","frequencia":255582},
                            {"periodo":"[1950,1960[","frequencia":395857},{"periodo":"[1960,1970[","frequencia":428482},{"periodo":"[1970,1980[","frequencia":279445},
                            {"periodo":"[1980,1990[","frequencia":272896},{"periodo":"[1990,2000[","frequencia":350409},{"periodo":"[2000,2010[","frequencia":787738}]
        item_busca = Item(nome="Joao", sexo="M", localidade="BR", resposta_api=resposta_api, decada=1920)
        frequencia = item_busca._buscar_frequencia(resposta_API=resposta_api)
        self.assertEqual(frequencia, 0)

    def test_decada_nao_encontrada(self):
        item_busca = Item(nome="Joao", sexo="M", localidade="BR", resposta_api=self.resposta_api, decada=2020)
        frequencia = item_busca._buscar_frequencia(resposta_API=self.resposta_api)
        self.assertEqual(frequencia, 0)

if __name__ == '__main__':
    unittest.main()
