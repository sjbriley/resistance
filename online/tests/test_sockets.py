from django.test import TestCase
from channels.testing import HttpCommunicator
from ..online_consumers import GameConsumer

# class SocketTests(TestCase):
#     async def test_my_consumer(self):
#         communicator = HttpCommunicator(GameConsumer, "GET", "/test/")
#         response = await communicator.get_response()
#         self.assertEqual(response["body"], b"test response")
#         self.assertEqual(response["status"], 200)