import unittest
from unittest.mock import MagicMock, patch
from Redis import RedisCache
from redis.exceptions import RedisError
import redis

class TestRedisCache(unittest.TestCase):

    @patch('redis.Redis')
    def test_init(self, mock_redis):
        cache = RedisCache()
        mock_redis.assert_called_once()

    @patch('Redis.logging.error')
    @patch('redis.Redis')
    def test_init_connection_error(self, mock_redis, mock_logging_error):
        mock_redis.side_effect = redis.ConnectionError("Connection Error")
        with self.assertRaises(redis.ConnectionError):
            RedisCache()
        mock_logging_error.assert_called_once_with("Não foi possível conectar ao servidor Redis em localhost:6379")

    @patch('redis.Redis')
    def test_init_exception(self, mock_redis):
        mock_redis.side_effect = RedisError("Connection Error")
        with self.assertRaises(RedisError):
            RedisCache()

    @patch('redis.Redis')
    def test_get_key_exists(self, mock_redis):
        cache = RedisCache()
        cache.redis.get.return_value = b'"value"'
        value = cache.get('key')
        self.assertEqual(value, 'value')

    @patch('redis.Redis')
    def test_get_key_not_exists(self, mock_redis):
        cache = RedisCache()
        cache.redis.get.return_value = None
        value = cache.get('key')
        self.assertIsNone(value)

    @patch('redis.Redis')
    def test_get_exception(self, mock_redis):
        cache = RedisCache()
        cache.redis.get.side_effect = RedisError("Error getting key")
        value = cache.get('key')
        self.assertIsNone(value)

    @patch('redis.Redis')
    def test_set(self, mock_redis):
        cache = RedisCache()
        cache.set('key', 'value')
        cache.redis.setex.assert_called_once()

    @patch('redis.Redis')
    def test_set_exception(self, mock_redis):
        cache = RedisCache()
        cache.redis.setex.side_effect = RedisError("Error setting key")
        cache.set('key', 'value')

    @patch('redis.Redis')
    def test_verificar_conexao_success(self, mock_redis):
        cache = RedisCache()
        cache.redis.ping.return_value = True
        self.assertTrue(cache.verificar_conexao())

    @patch('redis.Redis')
    def test_verificar_conexao_failure(self, mock_redis):
        cache = RedisCache()
        cache.redis.ping.return_value = False
        self.assertFalse(cache.verificar_conexao())


if __name__ == '__main__':
    unittest.main()
