import asyncio
import random
import re
import os
import threading
import traceback
from itertools import chain
from collections import OrderedDict
from time import time, sleep
from select import select
import socket
import operator
from weakref import WeakKeyDictionary, WeakValueDictionary

# renders
import graphviz
from jinja2 import Environment, PackageLoader, select_autoescape

# mine
from gutools.tools import _call, walk, rebuild, merge, parse_uri, flatten, \
    IntrospCaller
from gutools.utests import speed_meter

CO_COROUTINE = 128

STATE_INIT = 'INIT'
STATE_READY = 'READY'
STATE_END = 'END'
EVENT_TERM = '<term>'  # term alike
EVENT_QUIT = '<quit>'  # kill alike, but a chance to do something before die

MERGE_ADD = 'add'
MERGE_REPLACE_EXISTING = 'replace_existing'
MERGE_REPLACE_ALL = 'replace_all'

NO_STATE = []
QUITE_STATE = [[], [], []]

GROUP_ENTRY = 0
GROUP_DO = 1
GROUP_EXIT = 2

def bind(func_name, context):
    func = func_name and context[func_name]
    # TODO: assert is calleable
    # func.__binded__ = True  # just a tag for now
    return func

def precompile(exp):
    code = compile(exp, '<input>', mode='eval')
    return code

def _merge(states, transitions, mode=MERGE_ADD):
    """Merge states and transitions to create hierarchies of layers"""
    _states = states.pop(0) if states else dict()
    _transitions = transitions.pop(0) if transitions else dict()

    if mode in (MERGE_ADD, ):
        pass
    elif mode in (MERGE_REPLACE_EXISTING, ):
        for st in states:
            for state, new_functions in st.items():
                _states.pop(state, None)

        for tr in transitions:
            for source, new_info in tr.items():
                info = _transitions.setdefault(source, dict())
                for event, new_trx in new_info.items():
                    trx = info.setdefault(event, list())
                    for new_t in new_trx:
                        for i, t in reversed(list(enumerate(trx))):
                            if t[:1] == new_t[:1]:
                                trx.pop(i)

    elif mode in (MERGE_REPLACE_ALL, ):
        states.clear()
        for tr in transitions:
            for source, new_info in tr.items():
                _transitions.pop(source, None)
    else:
        raise RuntimeError(f"Unknown '{mode}' MERGE MODE")

    # merge states
    for st in states:
        for state, new_functions in st.items():
            functions = _states.setdefault(state, list([[], [], []]))
            for i, func in enumerate(new_functions):
                for f in func:
                    if f not in functions[i]:
                        functions[i].append(f)

    # merge transitions
    for tr in transitions:
        for source, new_info in tr.items():
            info = _transitions.setdefault(source, dict())
            for event, new_trx in new_info.items():
                trx = info.setdefault(event, list())
                for new_t in new_trx:
                    for t in trx:
                        if t[:2] == new_t[:2]:
                            t[-1].extend(new_t[-1])
                            break
                    else:
                        trx.append(new_t)




    return _states, _transitions

DEFAULT_STYLES = {
    'invisible': {'color': 'grey', 'shape': 'point'},
    'timer': {'color': 'darkgreen', 'fontcolor': 'darkgreen', 'style': 'dashed'},
    'rotation': [{'color': 'red', 'style': 'solid', }, {'color': 'orange', 'style': 'solid', }],
    'no_precond': {'color': 'blue', 'fontcolor': 'blue', 'style': 'solid'},
    'no_label': {'color': 'gray', 'style': 'dashed'},
}

class Layer(IntrospCaller):
    """
    States:

    [entry, do, each, exit ]'85t4ºrº<ZASCEF4ºQZ<scs3SE>>

    Trasition:
      [ state, new_state, preconditions, functions ]

    """

    def __init__(self, states=None, transitions=None, context=None):
        super().__init__(context)

        # self._state = None
        self.states = states if states is not None else dict()
        self.transitions = transitions if transitions is not None else dict()

        self.reactor = None
        self.state = None

        # Setup layer logic
        for name, states, transitions, mode, _ in self._get_layer_setups():
            self._merge(states, transitions, mode)

    def start(self, **kw):
        """Call when layer starts"""

    def bye(self, **kw):
        """Request the layer to term sending a EVENT_TERM event"""
        self.reactor.publish(EVENT_TERM, None)

    def term(self, key, **kw):
        """Request the layer to quit sending a EVENT_QUIT event"""
        self.reactor.publish(EVENT_QUIT, None)

    def quit(self, key, **kw):
        print(f" > Forcing {self.__class__.__name__} fo QUIT. Detaching from Reactor")
        self.reactor.detach(self)

    def _compile(self, states=None, transitions=None):
        """Precompile preconditions expressions and function calls as possible.
        """
        states = self.states if states is None else states
        transitions = self.transitions if transitions is None else transitions

        # prepare context with function as well
        context = dict([(k, getattr(self, k)) for k in [k for k in dir(self) if k[0] != '_']])

        # bind transitions functions
        for source, info in transitions.items():
            for event, trans in info.items():
                if len(trans) > 3:
                    continue  # it's already compiled
                for trx in trans:
                    trx.append(list())
                    target, precond, functions, comp_precond = trx
                    for i, func in enumerate(precond):
                        comp_precond.append(precompile(func))
                    for i, func in enumerate(functions):
                        functions[i] = bind(func, context)

        # bind state functions
        for grp_functions in states.values():
            for group, functions in enumerate(grp_functions):
                for i, func in enumerate(functions):
                    functions[i] = bind(func, context)
        foo = 1

    def _merge(self, states, transitions, mode=MERGE_ADD):
        """Merge states and transitions to create hierarchies of layers"""
        _merge([self.states, states], [self.transitions, transitions], mode=mode)

    def _trx_iterator(self):
        """evaluate all(event, state) pairs that the layer can process"""
        for source, info in self.transitions.items():
            for event, transitions in info.items():
                yield source, event, transitions

    def graph(self, graph_cfg=None, styles=None, isolated=True, view=False, include=None, skip=None, name=None, format='svg', path=None):
        """Create a graph of the layer definition"""

        nodes = set()
        include = include or []
        skip = skip or []
        path = path or os.path.join(os.path.abspath(os.curdir), 'stm')
        os.makedirs(path, exist_ok=True)
        name = name or f"{self.__class__.__name__}"

        def new_aux_node(style):
            aux_node = random.randint(0, 10**8)
            name = f"aux_{aux_node}"
            node = dg.node(name, **style)
            return name

        def next_style(stls):
            st = stls.pop(0)
            stls.append(st)
            return st

        def new_node(key, functions=None):
            key_ = f"{prefix}_{key}"
            if key_ not in nodes:
                nodes.add(key_)
                return dg.node(name=key_, label=key)

        def edge_attrs(source, event, target, precond, functions):

            if event is None:
                label = []
            else:
                label = [f"{event} ->"]

            for i, exp in enumerate(precond):
                label.append(f"[{exp}]")
            for i, func in enumerate(functions):
                if not isinstance(func, str):
                    func = func.__name__
                label.append(f"{i}: {func}()")
            label = '\n'.join(label)

            if label.startswith('each'):
                style = styles['timer']
            elif not precond:
                if label:
                    style = styles['no_precond']
                else:
                    style = styles['no_label']
            else:
                style = next_style(styles['rotation'])
            style['label'] = label
            return style

        def render_logics(self):
            # render logic definitions

            for name, functions in states.items():
                new_node(name, functions)

            for source, info in transitions.items():
                new_node(source, )  # assure node (with prefix) exists

                s = f"{prefix}_{source}"
                for event, trxs in info.items():
                    for trx in trxs:
                        target, precond, functions = z = trx[:3]

                        for zz in self.transitions.get(source, dict()).get(event, list()):
                            if zz[:2] == z[:2]:
                                break
                        else:
                            continue

                        new_node(target, )  # assure node (with prefix) exists

                        t = f"{prefix}_{target}"
                        attrs = edge_attrs(source, event, target, precond, functions)
                        if source == target:
                            aux_node = new_aux_node(styles['invisible'])
                            dg.edge(s, aux_node, **attrs)
                            attrs.pop('label', None)
                            dg.edge(aux_node, t, '', **attrs)
                            foo = 1
                        else:
                            dg.edge(s, t, **attrs)

            return dg

        # Default Graph configuration
        if graph_cfg is None:
            graph_cfg = dict(
                graph_attr=dict(
                    # splines="line",
                    splnes="compound",
                    model="subset",
                    # model="circuit",
                    # ranksep="1",
                    # model="10",
                    # mode="KK",  # gradient descend
                    mindist="2.5",
                ),
                edge_attr=dict(
                    # len="1",
                    # ranksep="1",
                ),
                # engine='sfdp',
                # engine='neato',
                # engine='dot',
                # engine='twopi',
                # engine='circo',
                engine='dot',
            )

        # Styles
        if styles is None:
            styles = dict()

        for key, st in DEFAULT_STYLES.items():
            styles.setdefault(key, st)

        dg = graph = graphviz.Digraph(name=name, **graph_cfg)
        prefix = f"{self.__class__.__name__}"
        graph.body.append(f'\tlabel="Layer: {prefix}"\n')

        for logic, states, transitions, mode, _ in self._get_layer_setups():
            if logic in skip:
                continue

            if include and logic not in include:
                continue

            if isolated:
                prefix = f"{self.__class__.__name__}_{logic}"
                dg = graphviz.Digraph(name=f"cluster_{logic}", **graph_cfg)

            render_logics(self)

            if isolated:
                dg.body.append(f'\tlabel="Logic: {logic}"')
                graph.subgraph(dg)

        graph.rendered = graph.render(filename=name,
                     directory=path, format=format, view=view, cleanup=True)

        return graph




    # -----------------------------------------------
    # Layer definitions
    # -----------------------------------------------
    def _get_layer_setups(self, include=None, skip=None):
        include = include or []
        skip = skip or []

        match = re.compile('_setup_(?P<name>.*)').match
        names = [name for name in dir(self) if match(name)]
        names.sort()
        for name in names:
            logic = match(name).groupdict()['name']

            if logic in skip:
                continue
            if include and logic not in include:
                continue

            func = getattr(self, name)
            states, transitions, mode = _call(func, **self.context)
            yield logic, states, transitions, mode, func.__doc__

    def _setup_term(self):
        """Set TERM and QUIT logic for the base layer."""
        states = {
            STATE_INIT: [[], [], ['start']],
            STATE_READY: [[], [], []],
            STATE_END: [[], ['bye'], []],
        }
        transitions = {
            STATE_INIT: {
                None: [
                    [STATE_READY, [], []],
                ],
            },
            STATE_READY: {
                EVENT_TERM: [
                    [STATE_READY, [], ['term']],
                ],
                EVENT_QUIT: [
                    [STATE_END, [], ['quit']],
                ],
            },
            STATE_END: {
            },
        }
        return states, transitions, MERGE_ADD


class STM(object):
    """Gather many Layers that share context and receive same events
    but has independent internal states
    """

class Transport(object):
    """TODO: different transports: sock, pipes, subprocess, etc."""
    def __init__(self, url):
        self.url = url

    def write(self, data, **info):
        """Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it
        to be sent out asynchronously.
        """
        raise NotImplementedError

    def writelines(self, list_of_data):
        """Write a list (or any iterable) of data bytes to the transport.

        The default implementation concatenates the arguments and
        calls write() on the result.
        """
        data = b''.join(list_of_data)
        self.write(data)

    def write_eof(self):
        """Close the write end after flushing buffered data.

        (This is like typing ^D into a UNIX program reading from stdin.)

        Data may still be received.
        """
        raise NotImplementedError

    def can_write_eof(self):
        """Return True if this transport supports write_eof(), False if not."""
        raise NotImplementedError

    def abort(self):
        """Close the transport immediately.

        Buffered data will be lost.  No more data will be received.
        The protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}: {self.url}"

    def __repr__(self):
        return str(self)

class SockTransport(Transport):
    def __init__(self, url, sock):
        super().__init__(url)
        self.sock = sock

    def write(self, data, **info):
        # TODO: timeit: convert only when is not byte or always
        self.sock.send(data)



class Protocol(object):
    """
    Ref: https://docs.python.org/3/library/asyncio-protocol.html#asyncio-protocol
    """
    def __init__(self, reactor, layer):
        self.transport = None
        self.reactor = reactor
        self.layer = layer

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        """Called when the connection is lost or closed.

        The argument is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """
        self.transport = None

    def data_received(self, data):
        """Called when a data is received from transport"""

    def eof_received(self):
        """Called when a send or receive operation raises an OSError."""

class EchoProtocol(Protocol):
    """A simple ECHO demo protocol"""

    def data_received(self, data):
        self.transport.write(data)

class TestBrowserProtcol(Protocol):
    def connection_made(self, transport):
        super().connection_made(transport)
        request = """GET / HTTP/1.1
Accept-Encoding: identity
Host: www.debian.org
User-Agent: Python-urllib/3.7
Connection: close

"""
        request = request.replace('\n', '\r\n')
        request = bytes(request, 'utf-8')
        self.transport.write(request)

    def data_received(self, data):
        """Called when a data is received from transport"""
        assert b'The document has moved' in data
        for line in str(data, 'utf-8').splitlines():
            print(line)

        # import urllib.request
        # import urllib.parse

        # url = 'http://www.debian.org'
        # f = urllib.request.urlopen(url)
        # print(f.read().decode('utf-8'))

    def eof_received(self):
        self.reactor.stop()


class Reactor(object):
    """Holds several STM and provide a mechanism for STM to
    receive and submit events:

    - use pub/sub paradigm.
    - use asycio paradigm.
    - need asycio events channels.
    - runs()

    Is focused on speed:
    - Layers define events using regexp.
    - Reactor use a cache of (event, state) updated in runtime.
    """

    def __init__(self):
        self.layers = WeakKeyDictionary()
        self.events = dict()
        self._queue = list()
        self._timers = list()
        self._transports = dict()
        self._protocols = dict()
        self._layer_transports = dict()

        self.running = False

    def attach(self, layer):
        """Attach a Layer to infrastructure:
        - evaluate all (event, state) pairs that the layer can process
        - add to reactor infrastructure
        """
        layer._compile()
        # prepare event placeholders
        for state, event, trx in layer._trx_iterator():
            self.events.setdefault(event, dict())
            if isinstance(event, str):
                # prepare timers as well
                timer = event.split('each:')
                timer = timer[1:]
                if timer:
                    timer = timer[0].split(',')
                    timer.append(0)
                    timer = [int(x) for x in timer[:2]]
                    timer.reverse()
                    timer.append(event)
                    self._timers.append(timer)
                    self._timers.sort()
                    foo = 1

        # set the initial state for the layer
        new_state = layer.state = STATE_INIT
        for ev, trx in layer.transitions[new_state].items():
            self.events[ev][layer] = trx

        # asure thet the context contains all public layer elements
        # so is not dependant on superclasses __init__() order
        context = dict([(k, getattr(layer, k)) for k in [k for k in dir(layer) if k[0] != '_']])
        layer.context.update(context)

        layer.reactor, self.layers[layer] = self, layer

    def detach(self, layer):
        """Detach a Layer from infrastructure:
        - evaluate all (event, state) pairs that the layer can process
        - remove from reactor infrastructure"""
        for source, event, transitions in layer._trx_iterator():
            info = self.events.get(event, {})
            info.pop(layer, None)

        # remove non persistent trsnsports created by layer
        for transport in self._layer_transports.pop(layer, []):
            self.close_channel(transport)

        # remove layer and check is reactor must be running
        self.layers.pop(layer)
        self.running = len(self.layers) > 0

    def publish(self, key, data=None):
        self._queue.append((key, data))

    def create_channel(self, protocol_factory, url,
                       sock=None, local_addr=None, layer=None,
                       **kw):
        """Create a transport connection linked with protocol instance from
        protocol factory.

        - layer != None : transport is removed when layers detach
        - layer = None  : transport is kept alive until reactor ends
        """
        if sock is None:
            for family, type_, proto, raddr, laddr in self._analyze_url(url):
                sock = socket.socket(family=family, type=type_, proto=proto)
                # sock.setblocking(False)
                ok = True
                for addr in laddr:
                    try:
                        sock.bind(addr)
                        break
                    except OSError as why:
                        ok = False
                if not ok:
                    continue
                for addr in raddr:
                    try:
                        sock.connect(addr)
                        break
                    except OSError as why:
                        ok = False
                if ok:
                    break
            else:
                raise RuntimeError(f"Unable to create a sock for {url}")

        protocol = protocol_factory(reactor=self, layer=layer)
        # TODO: different transport types based on url
        transport = SockTransport(url, sock)

        self._transports[sock] = transport
        self._protocols[sock] = protocol
        protocol.connection_made(transport)

        # store transport by layer. None means is persistent
        self._layer_transports.setdefault(layer, list()).append(transport)

        return transport, protocol

    def close_channel(self, transport=None, protocol=None):
        transport = transport or protocol.transport
        sock = transport.sock
        self._transports.pop(sock)
        self._protocols.pop(sock)
        sock.close()

    def run(self):
        # print("> Starting Reactor loop")

        self.t0 = time()
        self.running = True

        while self.running:
            # try to evolute layers that do not require any events (None)
            events = self.events.get(None)
            if events:
                key = data = None
            else:
                # or wait for an external event
                key, data = self.next_event()  # blocking
                events = self.events.get(key)
                if not events:
                    continue

            # process all available transitions
            for layer, transitions in chain(list(events.items())):
                # check if a transition can be trigered
                ctx = layer.context
                ctx['key'] = key

                # pass data into context
                # 1st in a isolated manner
                ctx['data'] = data

                # 2nd directly, to allow callbacks receive the params directly
                # this may override some context variable
                # TODO: update the other way arround, but is slower
                isinstance(data, dict) and ctx.update(data)

                for (new_state, preconds, funcs, comp_preconds) in transitions:
                    try:
                        # DO NOT check preconditions, it's makes slower
                        for pre in comp_preconds:
                            if not eval(pre, ctx):
                                break
                        else:
                            if new_state != layer.state:  # fast self-transitions
                                # remove current state events
                                for ev in layer.transitions[layer.state]:
                                    self.events[ev].pop(layer)  # must exists!!
                                # add new state events
                                for ev, trx in layer.transitions[new_state].items():
                                    self.events[ev][layer] = trx

                            # execute EXIT state functions (old state)
                            for func in layer.states[layer.state][GROUP_EXIT]:
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            # execute transition functions
                            for func in funcs:
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            layer.state = new_state

                            # execute ENTRY state functions (new state)
                            for func in layer.states[new_state][GROUP_ENTRY]:
                                # asyncio.iscoroutine(func)
                                # func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            # execute DO state functions (new state)
                            for func in layer.states[new_state][GROUP_DO]:
                                # asyncio.iscoroutine(func)
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            break  # assume there's only 1 transition possible each time
                    except Exception as why:
                        print()
                        print(f"- Reactor {'-'*70}")
                        print(f"*** ERROR: {why} ***")
                        traceback.print_exc()
                        print("-" * 80)
                        foo = 1

        # close all remaining transports
        for transport in list(self._transports.values()):
            print(f" - closing: {transport}")
            self.close_channel(transport)

        # print("< Exiting Reactor loop")
        foo = 1

    def stop(self):
        self.publish(EVENT_TERM)
        self.running = False

    @property
    def time(self):
        return time() - self.t0

    def next_event(self):
        """Blocks waiting for an I/O event or timer.
        Try to compensate delays by substracting time.time() and sub operations."""
        def close_sock(fd):
            self._protocols[fd].eof_received()
            self.close_channel(self._transports[fd])

        while True:
            if self._queue:
                return self._queue.pop(0)

            # there is not events to process. look for timers and I/O
            if self._timers:
                when, restart, key = timer = self._timers[0]
                seconds = when - self.time
                if seconds > 0:
                    rx, _, ex = select(self._transports, [], self._transports, seconds)
                    for fd in rx:
                        try:
                            raw = fd.recv(0xFFFF)
                            if raw:
                                self._protocols[fd].data_received(raw)
                            else:
                                close_sock(fd)
                        except Exception as why:
                            close_sock(fd)
                            pass

                    for fd in ex: # TODO: remove if never is invoked
                        close_sock(fd)
                        foo = 1
                else:
                    self.publish(key, None)
                    # --------------------------
                    # rearm timer
                    self._timers.pop(0)
                    if restart <= 0:
                        continue  # is a timeout timer, don't restart it
                    when += restart
                    timer[0] = when
                    #  insert in right position
                    i = 0
                    while i < len(self._timers):
                        if self._timers[i][0] > when:
                            self._timers.insert(i, timer)
                            break
                        i += 1
                    else:
                        self._timers.append(timer)
            else:
                # duplicate code for faster execution
                rx, _, _ = select(self._transports, [], [], 1)
                for fd in rx:
                    try:
                        raw = fd.recv(0xFFFF)
                        if raw:
                            self._protocols[fd].data_received(raw)
                        else:
                            close_sock(fd)
                    except Exception as why:
                        close_sock(fd)
                        pass
            foo = 1
        foo = 1

    def graph(self, dg=None, graph_cfg=None, styles=None, view=True, format='svg'):
        if graph_cfg is None:
            graph_cfg = dict(
                graph_attr=dict(
                    # splines="line",
                    # splnes="compound",
                    # model="subset",
                    # model="circuit",
                    ranksep="1",
                    model="10",
                    mode="KK",  # gradient descend
                    mindist="2.5",
                ),
                edge_attr=dict(
                    len="5",
                    ranksep="3",
                ),
                # engine='sfdp',
                # engine='neato',
                # engine='dot',
                # engine='twopi',
                # engine='circo',
                engine='dot',
            )

        # Styles
        if styles is None:
            styles = dict()

        for name, st in DEFAULT_STYLES.items():
            styles.setdefault(name, st)

        # Create a new DG or use the expernal one
        if dg is None:
            dg = graphviz.Digraph(**graph_cfg)

        for layer in self.layers:
            graph = layer.graph(graph_cfg, styles, format=format)
            name = layer.__class__.__name__
            graph.body.append(f'\tlabel="Layer: {name}"\n')
            dg.subgraph(graph)

        # dg._engine = 'neato'
        dg.render('reactor.dot', format='svg', view=view)
        foo = 1


    def _analyze_url(self, url):
        url_ = parse_uri(url)
        # family, type_, proto, raddr, laddr
        family, type_, proto, port = {
            'tcp': (socket.AF_INET, socket.SOCK_STREAM, -1, None),
            'http': (socket.AF_INET, socket.SOCK_STREAM, -1, 80),
            'udp': (socket.AF_INET, socket.SOCK_DGRAM, -1, None),
        }.get(url_['fscheme'])

        raddr = [(url_['host'], url_['port'] or port)]
        laddr = []

        yield family, type_, proto, raddr, laddr






class DebugReactor(Reactor):
    """Reactor with debugging and Statisctical information"""
    def __init__(self):
        super().__init__()
        self.__stats = dict()
        for k in ('cycles', 'publish', 'max_queue', 'max_channels', ):
            self.__stats[k] = 0

    def publish(self, key, data=None):
        Reactor.publish(self, key, data)
        self.__stats['publish'] += 1
        self.__stats['max_queue'] = max([len(self._queue), \
                                         self.__stats['max_queue']])

    def create_channel(self, url, **kw):
        Reactor.publish(self, url=url, **kw)

        s = self.__stats.setdefault('create_channel', dict())
        s[url] = s.get(url, 0) + 1

        self.__stats['max_channels'] = max([len(self._transports), \
                                            self.__stats['max_channels']])

    def run(self):
        # print("> Starting Reactor loop")
        s = self.__stats

        # events received
        evs = s['events'] = dict()
        for ev in self.events:
            evs[ev] = 0
        evs[None] = 0

        # states
        sts = s['states'] = dict()
        trx = s['transitions'] = dict()
        trx_f = s['transitions_failed'] = dict()
        for layer in self.layers:
            sts_ = sts[layer] = dict()
            trx_ = trx[layer] = dict()
            for logic, states, transitions, _ in layer._get_layer_setups():
                for state_ in states:
                    sts_[state] = 0
                for tx in transitions:
                    trx_[tx[0]] = 0
                    trx_f[tx[0]] = 0

        # the same code as Reactor.run() but updating stats
        # NOTE: we need to update the code manually if base class changes

        self.t0 = time()
        self.running = True

        while self.running:
            # try to evolute layers that do not require any events (None)
            events = self.events.get(None)
            if events:
                key = data = None
            else:
                # or wait for an external event
                key, data = self.next_event()  # blocking
                events = self.events.get(key)
                if not events:
                    continue

            s['cycles'] += 1  # <<
            evs[key] += 1  # <<

            # process all available transitions
            for layer, transitions in chain(list(events.items())):
                # check if a transition can be trigered
                ctx = layer.context
                ctx['key'] = key

                # pass data into context
                # 1st in a isolated manner
                ctx['data'] = data

                # 2nd directly, to allow callbacks receive the params directly
                # this may override some context variable
                # TODO: update the other way arround, but is slower
                isinstance(data, dict) and ctx.update(data)

                for (new_state, preconds, funcs, comp_preconds) in transitions:
                    try:
                        # DO NOT check preconditions, it's makes slower
                        for pre in comp_preconds:
                            if not eval(pre, ctx):
                                trx_f[new_state] += 1
                                break
                        else:
                            trx_[new_state] += 1
                            if new_state != layer.state:  # fast self-transitions
                                # remove current state events
                                for ev in layer.transitions[layer.state]:
                                    self.events[ev].pop(layer)  # must exists!!
                                # add new state events
                                for ev, trx in layer.transitions[new_state].items():
                                    self.events[ev][layer] = trx

                            # execute EXIT state functions (old state)
                            for func in layer.states[layer.state][GROUP_EXIT]:
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            # execute transition functions
                            for func in funcs:
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            layer.state = new_state

                            sts[layer][new_state] += 1  # <<

                            # execute ENTRY state functions (new state)
                            for func in layer.states[new_state][GROUP_ENTRY]:
                                # asyncio.iscoroutine(func)
                                # func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            # execute DO state functions (new state)
                            for func in layer.states[new_state][GROUP_DO]:
                                # asyncio.iscoroutine(func)
                                # await func(**ctx) if func.__code__.co_flags & CO_COROUTINE else func(**ctx)
                                func(**ctx)

                            break  # assume there's only 1 transition possible each time
                    except Exception as why:
                        print()
                        print(f"- Reactor {'-'*70}")
                        print(f"*** ERROR: {why} ***")
                        traceback.print_exc()
                        print("-" * 80)
                        foo = 1

        # close all remaining transports
        for transport in list(self._transports.values()):
            print(f" - closing: {transport}")
            self.close_channel(transport)

        # print("< Exiting Reactor loop")
        foo = 1

class DocRender(object):
    def __init__(self, reactor):
        self.reactor = reactor
        self.env = Environment(
            loader=PackageLoader(self.__module__, 'jinja2'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, root, include=None, skip=['term']):
        """Render the documentation in Markdown formar ready to be used
        by Hugo static html generator.

        - main file is 'stm.md'
        - graphs are created in SVG format under stm/xxx.svg directory (hugo compatible)

        """
        include = include or []
        skip = skip or []

        ctx = dict(format='svg', path=os.path.join(root, 'stm'), skip=skip)

        # render main Markdown file
        template = self.env.get_template('layer.md')
        ctx['layers'] = self.reactor.layers
        with open(os.path.join(root, 'stm.md'), 'w') as f:
            out = template.render(**ctx)
            f.write(out)

        # render each layer logic in a single diagram
        for layer in self.reactor.layers:
            ctx['layer'] = layer
            ctx['layer_name'] = layer.__class__.__name__
            ctx['include'] = []
            ctx['name'] = f"{ctx['layer_name']}"
            ctx['graph'] = graph = _call(layer.graph, **ctx)

            for logic, states, transitions, doc in layer._get_layer_setups(include, skip):
                ctx['include'] = [logic]
                ctx['name'] = f"{ctx['layer_name']}_{logic}"
                ctx['graph'] = graph = _call(layer.graph, **ctx)





        for logic, states, transitions in self._get_layer_setups():
            if logic in skip:
                continue

            if isolated:
                prefix = f"{self.__class__.__name__}_{logic}"
                dg = graphviz.Digraph(name=f"cluster_{logic}", **graph_cfg)

            render_logics()
            if isolated:
                dg.body.append(f'\tlabel="Logic: {logic}"')
                graph.subgraph(dg)


