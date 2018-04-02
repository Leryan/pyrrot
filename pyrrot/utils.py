from importlib import import_module

def type_check(obj, cls):
    if not issubclass(obj, cls):
        raise TypeError('object does not subclass {}'.format(cls.__name__))

def get_class(mod_path, typeof):
    mp = mod_path.split('.')

    mod_path = '.'.join(mp[:-1])
    class_name = mp[-1]

    module = import_module(mod_path)

    the_class = getattr(module, class_name, None)

    if the_class is None:
        raise Exception('class {} not found in {}'.format(class_name, mod_path))

    type_check(the_class, typeof)

    return the_class
