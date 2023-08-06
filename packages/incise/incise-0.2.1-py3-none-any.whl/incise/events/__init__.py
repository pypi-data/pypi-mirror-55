
"""
This extension utilizes :mod:`wrapio` to accomodate for event-based applications
as well as :mod:`lineopt` for creating command parsing and invoking frameworks.
"""

import asyncio
import wrapio
import lineopt
import collections

import incise


__all__ = ('Client', 'load', 'drop', 'call', 'wait', 'sub', 'origin')


_Asset = collections.namedtuple('Asset', 'track names')


class Client(incise.Client):

    """
    See superclass documentation for more information.

    :param asyncio.AbstractEventLoop loop:
        Used for :class:`wrapio.Track` creation.

    :var lineopt.State state:
        The universal commands mapping.
    """

    __slots__ = ('_state', '_assets', '_loop')

    def __init__(self, loop = None):

        super().__init__()

        self._state = lineopt.State()

        self._assets = {}

        self._loop = loop or asyncio.get_event_loop()

    @property
    def state(self):

        return self._state

    def invoke(self, name, *values):

        """
        Call the respective method for all tracks.
        """

        for asset in self._assets.values():

            asset.track.invoke(name, *values)

    def _load(self, module):

        track = wrapio.Track(loop = self._loop)

        self._assets[module] = _Asset(track, {})

    def _drop(self, module):

        asset = self._assets.pop(module)

        for name in asset.flags:

            del self._state[name]


load = incise.load


drop = incise.drop


def _origin():

    (client, module) = wrapio.origin(True)

    asset = client.assets[module]

    return (client, asset)


def origin(full = False):

    """
    Get the client for the source module.
    """

    values = _origin()

    return values if full else values[0]


def call(name):

    """
    Works the same as :meth:`wrapio.Track.call`.

    .. code-block::

        @call('message create')
        async def listen(event):
            print(event.message.author.username, 'said', event.message.content)
    """

    (client, asset) = _origin()

    return asset.track.call(name)


def wait(name):

    """
    Works the same as :meth:`wrapio.Track.wait`.

    .. code-block::

        @wait('message create')
        async def waiter_0(event):
            if not event.message.content == 'agreed':
                return
            waiter_0.set()
        await waiter_0.wait()
        print('agreed to the rules')
    """

    (client, asset) = _origin()

    return asset.track.wait(name)


def sub(name, *args, **kwargs):

    """
    Works the same as :meth:`lineopt.State.sub`.

    .. code-block::

        flags = {'-u': User}

        @sub('pat', flags)
        async def command_0(event, context):
            user = context.arguments['-u']
            response = f'*pat {user.username}*'
            await client.create_message(event.channel.id, content = response)

        @command_0.sub('hard')
        def comand_0_0(event, context):
            # ...
    """

    (client, asset) = _origin()

    asset.flags[name] = flags

    return client.state.sub(name, *args, **kwargs)
