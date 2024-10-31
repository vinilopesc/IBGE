import psycopg2
import psycopg2.extras
import logging

class Postgre:
    def __init__(self, host, port, database, user, password):
        """
        Inicializa a conexão com o banco de dados PostgreSQL.
        """
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.create_table()
        except Exception as e:
            logging.error(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
            raise

    def create_table(self):
        """
        Cria a tabela 'nomes' se ela não existir, com uma restrição de unicidade.
        """
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS nomes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            localidade VARCHAR(100),
            sexo VARCHAR(10),
            decada VARCHAR(10),
            frequencia INTEGER,
            UNIQUE (nome, localidade, sexo, decada)
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data(self, items):
        """
        Insere uma lista de objetos Item na tabela do banco de dados.
        Evita duplicatas usando ON CONFLICT DO NOTHING.
        :param items: Lista de instâncias da classe Item.
        """
        insert_query = '''
        INSERT INTO nomes (nome, localidade, sexo, decada, frequencia)
        VALUES %s
        ON CONFLICT (nome, localidade, sexo, decada) DO NOTHING
        '''
        data = [
            (item.nome, item.localidade, item.sexo, str(item.decada), item.frequencia)
            for item in items
        ]
        try:
            psycopg2.extras.execute_values(self.cursor, insert_query, data)
            self.connection.commit()
        except Exception as e:
            logging.error(f"Erro ao inserir dados no PostgreSQL: {e}")
            self.connection.rollback()

    def close(self):
        """
        Encerra a conexão com o banco de dados.
        """
        self.cursor.close()
        self.connection.close()
