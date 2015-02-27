import websocket
import unittest
from multiprocessing import Process
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import time
import os
import json
import redis
import requests
os.environ['HIPOCHAT_PUSH_NOTIFICATION_URL'] = "http://localhost:8194/push_notification_url"
os.environ['HIPOCHAT_PROFILE_URL'] = "http://localhost:8194/profile_url"
os.environ['HIPOCHAT_REDIS_DB'] = "3"

import hipochat.chat
import json


class TestChat(unittest.TestCase):

    def setUp(self):
        self.redis_conn = redis.StrictRedis(db=3)
        self.redis_conn.flushdb()
        self.process = Process(target=hipochat.chat.run)
        self.process.start()
        time.sleep(2)

    def test_client(self):
        # websocket.enableTrace(True)
        ws = websocket.create_connection("ws://127.0.0.1:8888/talk/chat/room_hipo/?token=TOKEN_1234")
        # TODO: wait until authorization
        time.sleep(2)
        d = json.dumps(dict(
            body="hello world",
            type="message"

        ))
        ws.send(d)
        result = ws.recv()
        print "result --- ", result
        ws.close()
        resp = requests.get(
            'http://127.0.0.1:8888/talk/history/room_hipo,room_foo?token=TOKEN_1234'
        )
        data = json.loads(resp.content)
        assert data['results'][0]['messages'][0]["body"] == "hello world"
        assert len(data['results'][1]["messages"]) == 0

    def tearDown(self):
        self.process.terminate()

if __name__ == '__main__':
    unittest.main()