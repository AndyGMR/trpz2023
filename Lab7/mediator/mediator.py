class Mediator:
    def __init__(self, server, observer):
        self.server = server
        self.observer = observer

    def handle_command(self, command):
        response = self.server.handle_command(command)
        return response
