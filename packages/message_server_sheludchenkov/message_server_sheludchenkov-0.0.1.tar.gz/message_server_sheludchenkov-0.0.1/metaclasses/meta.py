import dis


class ServerVerifier(type):
    """Проверка сервера на вызов допустимых функций"""
    def __init__(self, instance, bases, class_dict):
        methods = list()
        attributes = list()
        for f in class_dict:
            try:
                ret = dis.get_instructions(class_dict[f])
            except TypeError:
                pass
            else:
                for i in ret:
                    # print(f'I: {i}')
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_GLOBAL':
                        if i.argval not in attributes:
                            attributes.append(i.argval)
        if 'connect' in methods:
            raise TypeError("Method 'connect' is not allowed in server class")
        if not ('SOCK_STREAM' in attributes and 'AF_INET' in attributes):
            raise TypeError("Incorrect socket parameters: "
                            "{attributes}".format(attributes=attributes))
        super().__init__(instance, bases, class_dict)
