class ServerPort:
    """Проверка валидности порта"""
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if int(value) > 65535 or int(value) < 1:
            raise ValueError('Incorrect port number')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
