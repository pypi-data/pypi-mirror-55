class KakeiboxHandler(object):
    def set_next_handler(self, kakeibox_handler):
        raise Exception("Method is not implemented")

    def handle(self, request):
        raise Exception("Method is not implemented")


class AbstractKakeiboxHandler(KakeiboxHandler):
    _next_handler= None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return request
