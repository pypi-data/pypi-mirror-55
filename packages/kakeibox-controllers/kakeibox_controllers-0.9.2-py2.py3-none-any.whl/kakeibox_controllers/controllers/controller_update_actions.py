from kakeibox_controllers.controllers.controller_base \
    import KakeiboxControllerBase
from kakeibox_controllers.handlers.kakeibox_request \
    import KakeiboxRequest
from kakeibox_controllers.handlers.kakeibox_serializer_handler \
    import KakeiboxSerializerHandler
from kakeibox_controllers.handlers.kakeibox_executor_update_handler\
    import KakeiboxExecutorUpdateHandler
from kakeibox_controllers.handlers.kakeibox_presenter_handler \
    import KakeiboxPresenterHandler
from kakeibox_serializer_json.serializer.json_update_input_serializer \
    import JsonUpdateInputSerializerFabric
from kakeibox_presenter_json.presenter.json_presenter import JsonPresenter


class KakeiboxControllerUpdate(KakeiboxControllerBase):

    def _create_request(self):
        request = KakeiboxRequest()
        request.input = self._input
        request.command = self._command
        request.input_serializer = JsonUpdateInputSerializerFabric()
        request.presenter = JsonPresenter()
        self._request = request
        return request


    def _prepare_chain_of_commands(self):
        serialize = KakeiboxSerializerHandler()
        executor = KakeiboxExecutorUpdateHandler()
        presenter = KakeiboxPresenterHandler()
        serialize.set_next(executor).set_next(presenter)
        return serialize
