class KakeiboxControllerBase(object):
    def __init__(self):
        self._request = None
        self._input = None
        self._command = None
        self._request = None

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = input

    @property
    def request(self):
        return self._input

    @request.setter
    def request(self, request):
        self._request = request

    def execute(self):
        if not self._command or not self._input:
            raise Exception("The request command and input are required")

        if not self._request:
            request = self._create_request()
        chain_commands = self._prepare_chain_of_commands()
        chain_commands.handle(request)
        return request.presenter_output

    def _create_request(self):
        raise Exception("Method is not implemented")

    def _prepare_chain_of_commands(self):
        raise Exception("Method is not implemented")
