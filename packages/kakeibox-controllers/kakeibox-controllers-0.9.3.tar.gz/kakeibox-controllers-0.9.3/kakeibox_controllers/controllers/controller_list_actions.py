from kakeibox_controllers.controllers.controller_base \
    import KakeiboxControllerBase
from kakeibox_controllers.handlers.kakeibox_request \
    import KakeiboxRequest
from kakeibox_controllers.handlers.kakeibox_executor_list_handler \
    import KakeiboxExecutorListHandler
from kakeibox_controllers.handlers.kakeibox_presenter_handler \
    import KakeiboxPresenterHandler
from kakeibox_presenter_json.presenter.json_presenter import JsonPresenter


class KakeiboxControllerList(KakeiboxControllerBase):

    def execute(self):
        if not self._command:
            raise Exception("The request command and input are required")

        if not self._request:
            request = self._create_request()
        chain_commands = self._prepare_chain_of_commands()
        chain_commands.handle(request)
        return request.presenter_output

    def _create_request(self):
        request = KakeiboxRequest()
        request.command = self._command
        request.presenter = JsonPresenter()
        self._request = request
        return request

    def _prepare_chain_of_commands(self):
        executor = KakeiboxExecutorListHandler()
        presenter = KakeiboxPresenterHandler()
        executor.set_next(presenter)
        return executor
