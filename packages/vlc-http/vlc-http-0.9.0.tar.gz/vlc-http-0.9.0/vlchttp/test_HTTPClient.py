import random
from vlchttp import Client
from unittest import TestCase

client = Client('127.0.0.1', 8080, 'password')


class TestHTTPClient(TestCase):
    def test_get_status(self):
        status = client.get_status()
        self.assertEqual(status['apiversion'], 3)

    def test_get_playlist(self):
        playlist = client.get_playlist()
        self.assertEqual(playlist['type'], 'node')

    def test_command(self):
        random_volume = random.randint(0, 10)
        client.command('volume', ['val=%d' % random_volume])
        status = client.get_status()
        self.assertEqual(random_volume, status['volume'])
