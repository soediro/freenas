import re


class ServiceBase(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(ServiceBase, cls).__new__
        if name == 'Service' and bases == ():
            return super_new(cls, name, bases, attrs)

        config = attrs.pop('Config', None)
        klass = super_new(cls, name, bases, attrs)

        namespace = klass.__name__
        if namespace.endswith('Service'):
            namespace = namespace[:-7]
        namespace = namespace.lower()

        config_attrs = {
            'namespace': namespace,
            'public': True,
        }
        if config:
            config_attrs.update({
                k: v
                for k, v in config.__dict__ if not k.startswith('_')
            })

        klass._config = type('Config', (), config_attrs)
        return klass


class Service(object):
    __metaclass__ = ServiceBase

    def __init__(self, middleware):
        self.middleware = middleware


class CoreService(Service):

    def get_services(self):
        """Returns a list of all registered services"""
        return self.middleware.get_services().keys()
