from kakeibox_controllers.controllers.controller_base \
    import KakeiboxControllerBase
from kakeibox_controllers.handlers.kakeibox_request \
    import KakeiboxRequest
from kakeibox_controllers.handlers.kakeibox_serializer_handler \
    import KakeiboxSerializerHandler
from kakeibox_controllers.handlers.kakeibox_executor_list_periods_handler \
    import KakeiboxExecutorListPeriodsHandler
from kakeibox_controllers.handlers.kakeibox_presenter_handler \
    import KakeiboxPresenterHandler
from kakeibox_presenter_json.presenter.json_presenter import JsonPresenter
from kakeibox_serializer_json.serializer.json_serializer \
    import JsonInputSerializer


class KakeiboxControllerListPeriod(KakeiboxControllerBase):

    def _create_request(self):
        request = KakeiboxRequest()
        request.input = self._input
        request.command = self._command
        request.input_serializer = JsonInputSerializer()
        request.presenter = JsonPresenter()
        self._request = request
        return request

    def _prepare_chain_of_commands(self):
        serialize = KakeiboxSerializerHandler()
        executor = KakeiboxExecutorListPeriodsHandler()
        presenter = KakeiboxPresenterHandler()
        serialize.set_next(executor).set_next(presenter)
        return serialize
