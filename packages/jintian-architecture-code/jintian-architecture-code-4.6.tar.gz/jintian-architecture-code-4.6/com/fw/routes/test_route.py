import com.fw.base.base_route as base_route
import threading
from com.fw.base.base_service import BaseService

class TestService(BaseService):
    def __init__(self):
        BaseService.__init__(self, "test")

    def test(self):
        self.system.socket.send_message("PO1563507614eehTMv","test")

test_service = TestService()

class TestRoute():
    def __init__(self):
        self.path = "/test"
        self.suffix = ["hello","hello2","word"]

    @base_route.route_result
    def on_get_word(self, param):
        return test_service.test()


    @base_route.route_result
    def on_get_hello(self, param):
        return "hello"

    @base_route.route_result
    def on_get_hello2(self, param):
        return "hello2"

route = TestRoute()

