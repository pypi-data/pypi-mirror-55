# -*- coding: utf-8 -*-

"""
aiopb module provides a publisher/subscriptor pattern based on
asyncio library.

Implements:

- asyncio hubs where agents can attach and/or publish messages.
- priority queues.
- Uses enhanced Singleton patten wint Xingleton class.

"""
import sys
import re
import inspect
import types
import asyncio
import functools
from asyncio import futures
from asyncio.queues import Queue
from weakref import WeakValueDictionary

from gutools.tools import Xingleton, parse_uri, _call
from gutools.colors import *

def run(*awaitables, timeout: float = None, loop=None):
    """
    By default run the event loop forever.

    When awaitables (like Tasks, Futures or coroutines) are given then
    run the event loop until each has completed and return their results.

    An optional timeout (in seconds) can be given that will raise
    asyncio.TimeoutError if the awaitables are not ready within the
    timeout period.
    """
    loop = loop or asyncio.get_event_loop()
    if awaitables:
        if len(awaitables) == 1:
            future = awaitables[0]
        else:
            future = asyncio.gather(*awaitables)
        if timeout:
            future = asyncio.wait_for(future, timeout)
        result = loop.run_until_complete(future)
    else:
        if loop.is_running():
            return
        loop.run_forever()
        f = asyncio.gather(*asyncio.Task.all_tasks())
        f.cancel()
        result = None
        try:
            loop.run_until_complete(f)
        except asyncio.CancelledError:
            pass
    return result


def sleep(delay=0.05, loop=None):
    loop = loop or asyncio.events.get_event_loop()
    run(asyncio.sleep(delay, loop=loop))

# class Singleton(object):
    # _instance = None
    # def __new__(cls, *args, **kwargs):
        # if not cls._instance:
            # cls._instance = super(Singleton, cls).__new__(
                # cls, *args, **kwargs)
        # return cls._instance


class PriorityQueue(Queue):
    """"A priority message queue."""

    def _init(self, maxsize):
        self._queue = []

    def _put(self, item):
        """Insert the item in place. Priority is the 1st element
        of item.

        Usually items is is the form of tuple (priority, message).
        """
        queue = self._queue
        p = item[0]
        a, n = 0, len(queue)
        b = n
        while a < b:
            pos = int((a + b) / 2)
            if queue[pos][0] <= p:
                a = pos + 1
            else:
                b = pos
        else:
            if a == len(queue):
                queue.append(item)
            else:
                queue.insert(a, item)

    def _get(self):
        """Return the next element in queue."""
        return self._queue.pop(0)



class BaseHub(object, metaclass=Xingleton):
    """The Hub class holds messages in a priority queue and
    dispatch them using a Reactor pattern.

    The *life* can be gave by asyncio task, single thread, etc.

    Inherits from Xingleton, so only one Hub is created for same
    init arguments.
    """
    def __init__(self, realm=''):
        self.realm = realm
        "The realm that control the scope of the messages."

        self._subscriptions = dict()
        "subscriptions in this Hub"

        self._timers = dict()
        self.locked_keys = set()

        # start main loop
        # self.start()

    def __str__(self):
        return '<{}: {}>[{}]'.format(self.__class__.__name__, self.realm, self._queue.qsize())

    def __repr__(self):
        return str(self)



    def subscribe(self, pattern, callback, duplicate=False, single=False):
        """Add a new subscription pattern with  callback.

        Special pattern for timers could be defined as:

        - timer://localhost/each/5
        - timer://localhost/at/20190601/140030

        """
        regexp, callbacks = self._subscriptions.setdefault(pattern,
                            (re.compile(pattern, re.DOTALL), list()))
        if single and callbacks:
            # only 1 callback is allowed for this pattern
            return

        if duplicate or callback not in callbacks:
            # avoid call twice to the same callback
            callbacks.append(callback)

        uri_ = parse_uri(pattern)
        if uri_['scheme'] in ('timer', ):
            path_ = uri_['path'].split('/')
            if path_[1] in ('each', ):
                freq = int(path_[2])
                # publish pattern = [countdown, restar, ]
                self._timers[pattern] = [0, freq]
            elif path_[1] in ('at', ):
                raise NotImplementedError('not implemented yet')

    def unsubscribe(self, pattern=None, callback=None):
        """Remove a subscription."""
        pattern = re.compile(pattern or '.*')

        for regexp, (_, callbacks) in list(self._subscriptions.items()):
            if pattern.match(regexp):
                # retire callback
                if callbacks:
                    if callback in callbacks:
                        callbacks.remove(callback)
                else:
                    callbacks.clear()

                # if regexp has no callbacks, check if is a timer
                # to remove from timer loop
                if not callbacks:
                    self._subscriptions.pop(regexp)
                    uri_ = parse_uri(regexp)
                    if uri_['scheme'] in ('timer', ):
                        path_ = uri_['path'].split('/')
                        if path_[1] in ('each', ):
                            self._timers.pop(regexp, None)
                        elif path_[1] in ('at', ):
                            raise NotImplementedError('not implemented yet')
        foo = 1

    def detach(self, instance):
        """Remove ALL subscriptions from a instance, so the instance will not
        receive any further notification and can be free by garbage collector
        """
        for _, (regexp, callbacks) in list(self._subscriptions.items()):
            for callback in list(callbacks):
                if getattr(callback, '__self__', None) == instance:
                    callbacks.remove(callback)

    async def publish_sync(self, key, message, priority=1, duplicate=True, join=None):
        """Publish something and wait until someone set the result."""
        result = asyncio.Future(loop=self._loop)

        message = [result, message]
        self.publish(key, message, priority, duplicate, join)

        await result
        return result.result()

    def publish(self, key, message, priority=1, duplicate=True, join=None):
        """Publish a (key, message) pair with priority.

        If duplicate is False, then it will check to avoid add an already
        event in queue.
        """
        # TODO: remove this debug print
        # if not re.search(
            # r"""maintenance|contract_details|time|open_orders|bars|"""
            # r"""ib/fills|ib/comm"""
            # , key, re.DOTALL|re.MULTILINE|re.I):
            # print(f"**[{self.realm}] >> [{priority}] {key} {message}")

        if key in self.locked_keys:  # avoid re-entrant events
            return

        # check duplicated items when is required
        # NOTE: message must be hashable!
        assert join is None or isinstance(join, asyncio.Event)
        activity = (priority, key, message, join)
        if duplicate == False:
            if activity in self._queue._queue:
                return

        self._queue.put_nowait(activity)

    def block_key(self, key):
        if 'timer://' in key:
            print(f"{BLUE}>> LOCKING   {key}{RESET}")
            self.locked_keys.add(key)

    def release_key(self, key):
        if key in self.locked_keys:
            print(f"{BLUE}<< RELEASING {key}{RESET}")
            self.locked_keys.remove(key)

    def start(self):
        raise NotImplementedError("Must be overriden")

    def stop(self):
        raise NotImplementedError("Must be overriden")

class Hub(BaseHub):
    """This class implements BaseHub using ``asyncio`` module.
    """

    KEY_START = '/system/start'
    KEY_STOP = '/system/stop'

    def __init__(self, realm='', loop=None):
        super().__init__(realm)
        self._loop = loop
        self._is_running = asyncio.Event()

        self._queue = PriorityQueue(loop=self._loop)  # loop=self._loop)
        "The queue that holds the messages by priority"

        self._task_run = None
        self._task_timers = None

    # ------------------------------------------------
    # asyncio
    # ------------------------------------------------
    async def start(self, loop) -> None:
        """Start the dispatching process."""
        assert self._loop is None or not self._loop.is_running()

        self._loop = loop
        self._queue._loop = loop

        if self._is_running.is_set():
            assert (self._task_run is None or
                    self._task_run.done()) and \
                   (self._task_timers is None or
                    self._task_timers.done()), \
                "You must stop Hub before reusing same instance"
        else:
            self._is_running.set()
            self._task_run = self._loop.create_task(self._run())
            self._task_timers = self._loop.create_task(self._timers_loop())

        self.publish(self.KEY_START, self._loop.time())

    async def stop(self) -> None:
        """Stop dispatching messages."""
        # flush current queue
        assert self._is_running.is_set()
        while self._queue.qsize() > 0:
            await asyncio.sleep(0.05)

        # kindly request tasks to stop
        # publish a STOP message to all listeners
        # it also unlock the running queue so can exiting from while loop
        self.publish(self.KEY_STOP, self._loop.time())
        self._is_running.clear()

        # wait for them to stop
        for task in [self._task_run, self._task_timers]:
            for _ in range(100):
                if task.done():
                    break
                await asyncio.sleep(0.1)
            else:
                print(f'Forcing {task} to STOP !')
                task.cancel()

        self._task_run = None
        self._task_timers = None
        self._subscriptions.clear()

    async def _run(self):
        """Main loop of reactor pattern using asyncio library.

        - Get the next message in queue.
        - Iterate for all matching subscriptions.
        - Add callback in the loop to be executed ASAP.
        """
        foo = 1
        while self._is_running.is_set():
            # print(f"{GREEN}>> queue GET{RESET}")
            (priority, key, message, join) = activity = await self._queue.get()
            # print(f"{GREEN}<< queue GET: {key}{RESET}")
            for pat, (regexp, callbacks) in self._subscriptions.items():
                if regexp.match(key):
                    lock_list = list()
                    def relase_reentry_key(lock_list, join, done_task):
                        key = lock_list.pop()
                        if not lock_list:
                            self.release_key(key)
                            join and join.set()

                    release_callback = functools.partial(relase_reentry_key, lock_list, join)

                    for cb in callbacks:
                        # ensure we handle always a coroutine
                        # in order to add done callbacks
                        if not cb.__func__.__code__.co_flags & 0x0080:
                            cb = asyncio.coroutine(cb)
                        try:
                            cb = cb(key, message)
                        except Exception as why:
                            foo = 1
                            continue
                        task = self._loop.create_task(cb)
                        task.add_done_callback(release_callback)
                        lock_list.append(key)
                    self.block_key(key)
                else:
                    join and join.set()  # just in case none is listening to this publication

    async def _timers_loop(self):
        """Provide timers.
        It tries not shifting in time by accumulative errors."""
        foo = 1
        while self._is_running.is_set():
            t0 = self._loop.time()
            for key, timer in self._timers.items():
                timer[0] -= 1
                if timer[0] < 0:
                    timer[0] = timer[1]  # restart timer
                    self.publish(key, None)

            t1 = self._loop.time()
            await asyncio.sleep(1 - t1 + t0)
        foo = 1



# TODO: use Xingleton
# default_hub = None
# def get_hub(loop=None) -> Hub:
    # mod = sys.modules[__name__]
    # hub = getattr(mod, 'default_hub')
    # if hub is None:
        # hub = Hub(loop=loop)
        # setattr(mod, 'default_hub', hub)
        # hub.start()

    # return hub



