from kakeibox_controllers.handlers.kakeibox_handler \
    import AbstractKakeiboxHandler


class KakeiboxPresenterHandler(AbstractKakeiboxHandler):

    def handle(self, request):
        if request and request.presenter and request.command_response:
            presenter = request.presenter
            request.presenter_output = presenter.show(
                request.command_response.value)
        return super().handle(request)
