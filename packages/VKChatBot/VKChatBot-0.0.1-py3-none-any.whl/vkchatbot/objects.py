class Keyboard:
    def __init__(self):
        pass


class SendableMessage:
    def __init__(self, message: str, keyboard: Keyboard = None):
        self.message = message,
        self.keyboard = keyboard

    def to_dict(self):
        if self.keyboard is None:
            return {'message': self.message}
        else:
            raise NotImplemented()
