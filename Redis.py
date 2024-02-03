import redis
import json
import logging


class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Inicializa o cache, conectando-se ao servidor Redis.
        :param host: Endereço do servidor Redis.
        :param port: Porta do servidor Redis.
        :param db: Número do banco de dados Redis.
        """
        try:
            self.redis = redis.Redis(host=host, port=port, db=db)
        except redis.ConnectionError:
            logging.error(f"Não foi possível conectar ao servidor Redis em {host}:{port}")
            raise

    def get(self, key):
        """
        Obtém um valor do Redis pela chave fornecida.

        :param key: A chave para buscar o valor.
        :return: O valor associado à chave ou None se a chave não existir.
        """
        try:
            value = self.redis.get(key)
            if value:
                value = value.decode('utf-8')
                return json.loads(value)
            else:
                return None
        except redis.RedisError as e:
            logging.error(f"Erro ao obter valor da chave {key} no Redis: {e}")
            return None

    def set(self, key, value, expiration=600):
        """
        Define um valor no cache com uma chave e uma expiração.

        :param key: Chave para definir no cache.
        :param value: Valor para definir no cache.
        :param expiration: Tempo de expiração da chave em segundos.
        """
        try:
            value = json.dumps(value)
            self.redis.setex(key, expiration, value)
        except (redis.RedisError, TypeError) as e:
            logging.error(f"Erro ao definir chave {key} no Redis: {e}")

    def verificar_conexao(self):
        """
        Verifica se a conexão com o Redis está funcionando.

        :return: True se a conexão estiver funcionando, False caso contrário.
        """
        try:
            return self.redis.ping()
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            return False
