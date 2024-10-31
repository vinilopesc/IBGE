import unittest
from unittest.mock import patch, MagicMock
from src.Postgre import Postgre
from src.Item import Item
import psycopg2
import psycopg2.extras
import logging


class TestPostgre(unittest.TestCase):
    """
    Classe de testes para a classe Postgre, cobrindo todos os métodos principais.
    """

    @patch('psycopg2.connect')
    def test_init_conexao_sucesso(self, mock_connect):
        """
        Testa se a conexão com o banco de dados é estabelecida com sucesso.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')

        mock_connect.assert_called_once_with(
            host='host',
            port='port',
            database='database',
            user='user',
            password='password'
        )
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called()  # Verifica se create_table foi chamado
        mock_connection.commit.assert_called_once()

    @patch('psycopg2.connect')
    def test_init_conexao_falha(self, mock_connect):
        """
        Testa o tratamento de exceção quando a conexão com o banco de dados falha.
        """
        mock_connect.side_effect = Exception("Erro de conexão")
        with self.assertRaises(Exception) as context:
            Postgre('host', 'port', 'database', 'user', 'password')
        self.assertIn("Erro de conexão", str(context.exception))

    @patch('psycopg2.connect')
    def test_create_table(self, mock_connect):
        """
        Testa se o método create_table cria a tabela corretamente.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        mock_cursor.execute.assert_called()
        mock_connection.commit.assert_called()

    @patch('psycopg2.connect')
    def test_insert_data_erro(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        items = [Item(nome='Teste', frequencia=100)]

        with patch('psycopg2.extras.execute_values', side_effect=Exception("Erro ao inserir dados")):
            with self.assertLogs(level='ERROR') as log:
                postgre.insert_data(items)
                self.assertIn("Erro ao inserir dados no PostgreSQL: Erro ao inserir dados", log.output[0])
            mock_connection.rollback.assert_called_once()

    @patch('psycopg2.connect')
    def test_close(self, mock_connect):
        """
        Testa se a conexão com o banco de dados é fechada corretamente.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        postgre.close()

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_insert_data_item_invalido(self, mock_connect):
        """
        Testa o método insert_data quando um item inválido é fornecido.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        items = [None]  # Item inválido

        with self.assertRaises(AttributeError):
            postgre.insert_data(items)

    @patch('psycopg2.connect')
    def test_insert_data_rollback(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        items = [Item(nome='Teste', frequencia=100)]

        with patch('psycopg2.extras.execute_values', side_effect=Exception("Erro ao inserir dados")):
            with self.assertLogs(level='ERROR') as log:
                postgre.insert_data(items)
                self.assertIn("Erro ao inserir dados no PostgreSQL: Erro ao inserir dados", log.output[0])
            mock_connection.rollback.assert_called_once()

    @patch('psycopg2.connect')
    def test_close_exception(self, mock_connect):
        """
        Testa o tratamento de exceção ao fechar a conexão com o banco de dados.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.close.side_effect = Exception("Erro ao fechar cursor")
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.close.side_effect = Exception("Erro ao fechar conexão")
        mock_connect.return_value = mock_connection

        postgre = Postgre('host', 'port', 'database', 'user', 'password')
        with self.assertRaises(Exception) as context:
            postgre.close()
        self.assertIn("Erro ao fechar cursor", str(context.exception))

    @patch('psycopg2.connect')
    def test_create_table_commit(self, mock_connect):
        """
        Testa se o commit é chamado após a criação da tabela.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        Postgre('host', 'port', 'database', 'user', 'password')

        mock_connection.commit.assert_called_once()

    def test_insert_data_frequencia_none(self):
        """
        Testa se o método insert_data lida corretamente quando o atributo frequencia é None.
        """
        with self.assertRaises(ValueError):
            Item(nome='Pedro', localidade='SP', sexo='M', decada=1990, frequencia=None)

    @patch('psycopg2.connect')
    def test_insert_data_com_excecao_generica(self, mock_connect):
        """
        Testa o tratamento de uma exceção genérica ao inserir dados.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        item = Item(nome='Erro', localidade='SP', sexo='M', decada=1990, frequencia=100)
        items = [item]

        with patch('psycopg2.extras.execute_values', side_effect=Exception("Erro desconhecido")):
            postgre = Postgre('host', 'port', 'database', 'user', 'password')
            with self.assertLogs(level='ERROR') as log:
                postgre.insert_data(items)
                self.assertIn("Erro ao inserir dados no PostgreSQL: Erro desconhecido", log.output[0])
            mock_connection.rollback.assert_called_once()

    @patch('psycopg2.connect')
    def test_insert_data_com_dados_invalidos(self, mock_connect):
        """
        Testa o comportamento ao tentar inserir dados inválidos no banco.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        item = "Dado inválido"
        items = [item]

        postgre = Postgre('host', 'port', 'database', 'user', 'password')

        with self.assertRaises(AttributeError):
            postgre.insert_data(items)


if __name__ == '__main__':
    unittest.main()