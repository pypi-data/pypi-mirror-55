from kakeibox_controllers.handlers.kakeibox_handler \
    import AbstractKakeiboxHandler


class KakeiboxSerializerHandler(AbstractKakeiboxHandler):

    def handle(self, request):
        if request and request.input_serializer and request.input:
            serializer = request.input_serializer
            request.input_serialized = serializer.serialize(request.input)
        return super().handle(request)
