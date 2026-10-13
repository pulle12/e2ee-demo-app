import asyncio

from receiver import Receiver


class FakeWebSocket:
    def __init__(self, payload):
        self.payload = payload
        self.remote_address = ("127.0.0.1", 12345)
        self.sent = []

    def __aiter__(self):
        self._iter = iter([self.payload])
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

    async def send(self, message):
        self.sent.append(message)


def test_get_public_key_returns_key_without_blocking():
    receiver = Receiver()
    public_key = asyncio.run(asyncio.wait_for(receiver.get_public_key(), timeout=0.5))

    assert public_key is not None


def test_echo_decrypts_message_before_echo():
    receiver = Receiver()
    payload = '{"encrypted_key":"abc","encrypted_message":"def"}'
    websocket = FakeWebSocket(payload)
    called = {"value": None}

    def fake_decrypt(message):
        called["value"] = message

    receiver.decrypt_message = fake_decrypt

    asyncio.run(receiver.echo(websocket))

    assert called["value"] == payload
    assert websocket.sent == [f"Server-Echo: {payload}"]
