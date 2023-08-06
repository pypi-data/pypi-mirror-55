from kakeibox_controllers.controllers.controller_base \
    import KakeiboxControllerBase
from kakeibox_controllers.handlers.kakeibox_request \
    import KakeiboxRequest
from kakeibox_controllers.handlers.kakeibox_executor_handler \
    import KakeiboxExecutorHandler
from kakeibox_controllers.handlers.kakeibox_presenter_handler \
    import KakeiboxPresenterHandler
from kakeibox_presenter_json.presenter.json_presenter import JsonPresenter


class KakeiboxControllerGet(KakeiboxControllerBase):

    def _create_request(self):
        request = KakeiboxRequest()
        request.command = self._command
        request.presenter = JsonPresenter()
        request.input_serialized = self._input
        self._request = request
        return request

    def _prepare_chain_of_commands(self):
        executor = KakeiboxExecutorHandler()
        presenter = KakeiboxPresenterHandler()
        executor.set_next(presenter)
        return executor
