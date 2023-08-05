import dis


class ClientVerifier(type):
    """Проверка, что клиент не использует серверных функций"""
    def __init__(self, instance, bases, class_dict):
        methods = list()
        attributes = list()
        deny_commands = ('accept', 'listen', 'socket')
        for f in class_dict:
            try:
                ret = dis.get_instructions(class_dict[f])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_GLOBAL':
                        if i.argval not in attributes:
                            attributes.append(i.argval)
        for method in methods:
            if method in deny_commands:
                raise TypeError('Using forbidden method "{method}" in '
                                'client class'.format(method=method))
        if not ('SOCK_STREAM' in attributes and 'AF_INET' in attributes):
            raise TypeError("Incorrect socket parameters: {attributes}".
                            format(attributes=attributes))
        super().__init__(instance, bases, class_dict)
