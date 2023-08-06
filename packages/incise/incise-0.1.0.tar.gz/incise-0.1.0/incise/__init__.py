import os
import sys
import types
import itertools
import importlib
import collections
import weakref
import inspect

from . import helpers


__all__ = ('Client', 'load', 'drop', 'origin')


_cache = weakref.WeakValueDictionary()


def _register(unique, module):

    try:

        store = _cache[unique]

    except KeyError:

        store = _cache[unique] = weakref.WeakValueDictionary()

    store[module.__name__] = module


class Client:

    """
    Main means of interacting with the segmentation API.

    Upon creation, a fake module will be created and inserted into
    ``sys.modules`` with a unique numerical identifier appended to it. This is
    the base for loading any subsequent modules.
    """

    __slots__ = ('_modules', '_name')

    _uniques = set()

    _lead = helpers.virtual(__spec__, '_')

    def __init__(self):

        self._modules = {}

        indexes = itertools.count(0)

        identities = map(str, indexes)

        check = self._uniques.__contains__

        generate = itertools.filterfalse(check, identities)

        unique = next(generate)

        self._uniques.add(unique)

        self._name = f'{self._lead}.{unique}'

    @property
    def modules(self):

        return self._modules

    def _load(self, module):

        pass

    def load(self, path):

        """
        Create and track a new module.

        .. note::

            Must be called directly at least once before the global
            :func:`load` can be used.
        """

        base = os.path.basename(path)

        (name, extension) = os.path.splitext(base)

        path = helpers.parental(path)

        name = f'{self._name}.{name}'

        spec = importlib.util.spec_from_file_location(name, path)

        module = importlib.util.module_from_spec(spec)

        self._load(module)

        self._modules[path] = module

        _register(self, module)

        sys.modules[name] = module

        module.__spec__.loader.exec_module(module)

        return module

    def _drop(self, module):

        pass

    def drop(self, path):

        path = helpers.parental(path)

        module = self._modules.pop(path)

        self._drop(module)

        for key in tuple(sys.modules):

            if not key.startswith(module.__name__):

                continue

            sys.modules[key]

        return module

    def __del__(self):

        parts = self._name.rsplit('.', 1)

        unique = parts[-1]

        self._uniques.remove(unique)


def _origin():

    for info in inspect.stack():

        space = info.frame.f_globals

        name = space['__name__']

        for (unique, modules) in _cache.items():

            try:

                module = modules[name]

            except KeyError:

                continue

            if not space is module.__dict__:

                continue

            break

        else:

            continue

        break

    else:

        raise ModuleNotFoundError('Source is not an internally loaded module.')

    return (unique, module)


def load(path, *args, **kwargs):

    """
    Find the client for the source module and load the path.

    .. warning::

        :meth:`Client.load` must be called at least once before this is used.
    """

    (client, module) = _origin()

    path = helpers.filial(module, path)

    module = client.load(path)

    name = inspect.stack()[0].function

    result = helpers.findcall(module, name, args = args, kwargs = kwargs)

    return result


def drop(path, *args, **kwargs):

    """
    Find the client for the source module and drop the path.
    """

    (client, module) = _origin()

    path = helpers.filial(module, path)

    client.drop(path)

    name = inspect.stack()[0].function

    result = helpers.findcall(module, name, args = args, kwargs = kwargs)

    return result


def origin(full = False):

    """
    Get the client holding the loaded module this is called from.
    """

    assets = _origin()

    return assets if full else assets[0]
