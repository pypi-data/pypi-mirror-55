from kakeibox_controllers.handlers.kakeibox_handler \
    import AbstractKakeiboxHandler


class KakeiboxExecutorUpdateHandler(AbstractKakeiboxHandler):

    def handle(self, request):
        if request and request.command and request.input_serialized:
            request.command_response = request.command.execute(
                **request.input_serialized)
        return super().handle(request)
