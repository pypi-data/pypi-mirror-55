
import pytest
import asyncio
import random
import functools
from aiopb import aiopb

def test_queue_sorting():
    queue = aiopb.PriorityQueue()
    queue._put((9, 'A'))
    queue._put((7, 'B'))
    queue._put((8, 'C'))
    queue._put((9, 'A.2'))
    queue._put((7, 'B.2'))
    queue._put((8, 'C.2'))
    queue._put((5, 'E'))
    queue._put((1, 'a'))

    assert queue._get() == (1, 'a')
    assert queue._get() == (5, 'E')
    assert queue._get() == (7, 'B')
    assert queue._get() == (7, 'B.2')
    assert queue._get() == (8, 'C')
    assert queue._get() == (8, 'C.2')
    assert queue._get() == (9, 'A')
    assert queue._get() == (9, 'A.2')

def test_subscription():
    loop =  asyncio.get_event_loop()
    hits = dict()
    when = list()
    # B_hits = 0

    async def main(hub):
        i = 0
        while len(hits) < 10:
            i += 1

            print("main: {i}".format(**locals()))
            await asyncio.sleep(0.01)
            if True or random.random() < 0.3:
                print(">> {i}".format(**locals()))
                B_hits = 0
                hub.publish('hello', i)

            if random.random() < 0.1:
                print("+ print_message_B".format(**locals()))
                hub.subscribe('hello', print_message_B, unique=True)

            if random.random() < 0.1:
                hub.subscribe('hello', functools.partial(print_message, i))
                when.append(i)


    def print_message_A(message):
        print("<< A: {message}".format(**locals()))

    def print_message_B(message):
        global B_hits
        print("<< B: {message}".format(**locals()))
        # B_hits += 1
        # assert B_hits <= 1, "found a duplicated subscription"

    def print_message(instance, message):
        print("<< {instance}: {message}".format(**locals()))
        hits[instance] = hits.get(instance, 0) + 1

    hub = aiopb.Hub()
    hub.subscribe('hello', print_message_A)
    # hub.subscribe('hello', functools.partial(print_message, 'Z'))

    hub.start()

    loop.run_until_complete(main(hub))

    # assertions
    k0 = h0 = 0
    for k1 in when:
        h1 = hits[k1]
        if h0:
            d = k1 - k0
            assert h1 == h0 - d
        k0, h0 = k1, h1

    hub.stop()

    loop.run_until_complete(asyncio.sleep(0.5))

    loop.stop()

    foo = 1

def test_priority_queue():
    loop =  asyncio.get_event_loop()
    hits = dict()
    when = list()
    # B_hits = 0

    class Foo():
        def __init__(self, hub):
            self.order = []
            hub.subscribe('foo', self.foo)
            hub.subscribe('bar', self.bar)
            hub.subscribe('buzz', self.buzz)

        def reset(self):
            self.order.clear()

        def foo(self, msg):
            self.order.append(('foo', msg))

        def bar(self, msg):
            self.order.append(('bar', msg))

        def buzz(self, msg):
            self.order.append(('buzz', msg))

    async def main(hub):
        foo = Foo(hub)
        opts = ['foo', 'bar', 'buzz']
        for r in range(30):
            print('- Round {} {}'.format(r, '-' * 40))
            foo.reset()
            sequence = dict()
            n = 0
            # create a random priority work
            for i in range(random.randint(3, 20)):
                priority = random.randint(1, 10)
                call = random.choice(opts)
                hub.publish(call, i, priority=priority)
                sequence.setdefault(priority, list()).append((call, i))
                print("gen:[{priority}] {call}({i})".format(**locals()))
                n += 1

            await hub.join()
            assert len(foo.order) == n

            # check fired order
            unwrapped = list()
            seq = list(sequence.keys())
            seq.sort()
            for p in seq:
                unwrapped.extend(sequence[p])

            assert foo.order == unwrapped
            _ = 1

    hub = aiopb.Hub()
    hub.start()
    loop.run_until_complete(main(hub))

    hub.stop()
    loop.stop()
    foo = 1

def test_unsubscribe():
    foo = 1

