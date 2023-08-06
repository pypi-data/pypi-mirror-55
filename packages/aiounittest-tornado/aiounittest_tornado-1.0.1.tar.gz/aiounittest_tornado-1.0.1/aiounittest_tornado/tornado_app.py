"""

只是简单的利用了aiounitest和学习了tornado本身的测试的代码
"""

import asyncio

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import bind_unused_port
from aiounittest import AsyncTestCase


class AsyncHTTPTest(AsyncTestCase):
    """
    支持tornado 的http 测试部分
    """
    def setUp(self):
        sock, port = bind_unused_port()
        self.__port = port
        self.app = self.get_app()
        self.http_server = self.app.listen(self.__port)
        self.http_server.add_sockets([sock])

    def tearDown(self):
        self.http_server.stop()
        self.http_server.stop()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.http_server.close_all_connections())
        del self.http_server
        del self.app
        super(AsyncHTTPTest, self).tearDown()

    def get_app(self):
        raise Exception("需要载入tornado 中的应用")

    def get_url(self, path: str) -> str:
        """Returns an absolute url for the given path on the test server."""
        return "%s://127.0.0.1:%s%s" % (self.get_protocol(), self.get_http_port(), path)

    def get_protocol(self) -> str:
        return "http"

    def get_http_port(self) -> int:
        """Returns the port used by the server.

        A new port is chosen for each test.
        """
        return self.__port

    def get_http_client(self) -> AsyncHTTPClient:
        return AsyncHTTPClient()

    def get_event_loop(self):
        return asyncio.get_event_loop()
