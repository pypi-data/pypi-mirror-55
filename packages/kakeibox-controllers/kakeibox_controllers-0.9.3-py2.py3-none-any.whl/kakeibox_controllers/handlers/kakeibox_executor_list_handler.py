from kakeibox_controllers.handlers.kakeibox_handler \
    import AbstractKakeiboxHandler


class KakeiboxExecutorListHandler(AbstractKakeiboxHandler):

    def handle(self, request):
        if request and request.command:
            request.command_response = request.command.execute()
        return super().handle(request)
