from __future__ import absolute_import, division, print_function

del absolute_import, division, print_function


class FactoryMeta(object):
    def __init__(self, f, types):
        self._f = f
        self._types = types
        self.__doc__ = f.__doc__

    def __call__(self, *args, **kwargs):
        return self._f(*args, **kwargs)

    def __instancecheck__(self, other):
        return isinstance(other, self._types)


class KWArgs(object):
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.kwargs:
            raise TypeError("Keyword(s) {} not expected".format(", ".join(self.kwargs)))

    def required(self, name):
        if name in self.kwargs:
            self.kwargs.pop(name)
        else:
            raise KeyError("{0} is required".format(name))

    def optional(self, name, default=None):
        if name in self.kwargs:
            return self.kwargs.pop(name)
        else:
            return default

    def options(self, **options):
        return {option for option in options if self.optional(option, options[option])}
