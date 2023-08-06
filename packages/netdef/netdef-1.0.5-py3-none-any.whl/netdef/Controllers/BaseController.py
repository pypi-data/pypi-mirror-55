import queue
import logging
import time
from ..Sources.BaseSource import StatusCode
from ..Shared.Internal import Statistics

class BaseController():
    """
    Abstract class for controllers.

    :param str name: Name to be used in logfiles
    :param shared: a reference to the shared object

    """
    def __init__(self, name, shared):
        self.name = name
        self.shared = shared
        self.add_logger(name)
        self.init_queue()
        self.init_sources(None)
        self.init_parsers(None)
        self.add_interrupt(None)
        self._statistics_counters = {
            "last_minute": 0,
            "last_minute_time": ((time.time() // 60) * 60),
        }

    def _statistics_update_last_minute(self, increment):
        "Write internal statistics to the Statistics singleton if activated"
        if Statistics.on:
            Statistics.set(self.name + ".incoming.queue.size", self.incoming.qsize())

            counters = self._statistics_counters
            if not counters["last_minute_time"] == ((time.time() // 60) * 60):
                Statistics.set(self.name + ".incoming.last_minute.count", counters["last_minute"])
                Statistics.set(
                    self.name + ".incoming.last_minute.time",
                    time.strftime("%y.%m.%d %H:%M", time.localtime(counters["last_minute_time"]))
                )
                counters["last_minute_time"] = ((time.time() // 60) * 60)
                counters["last_minute"] = 1 if increment else 0
            elif increment:
                counters["last_minute"] += 1

    def add_logger(self, name):
        "Setup logging module"
        self.logger = logging.getLogger(name)

    def init_queue(self):
        "Setup the message queue and timeout"
        self.incoming = self.shared.queues.get_messages_to_controller(self.name)
        self.messagetypes = self.shared.queues.MessageType
        self.appstatetypes = self.shared.queues.AppStateType
        self.queue_timeout = 0.1

    def add_interrupt(self, interrupt):
        "Setup the interrupt signal"
        self._interrupt = interrupt

    def has_interrupt(self):
        "Returns True if the interrupt signal is received"
        return self._interrupt.is_set()
    
    def sleep(self, seconds):
        """"
        Sleep by waiting for the interrupt.
        Should be used instead of time.sleep.
        Override if sleep should be interrupted by even more signals
        """
        self._interrupt.wait(seconds)

    def init_sources(self, sources):
        """
        Setup the source storage as a dict.
        Override if something else is needed.
        """
        if sources:
            self._sources = sources
        else:
            self._sources = {}

    def init_parsers(self, parsers):
        """
        Setup the parser storage as a list.
        Override if something else is needed.
        """
        if parsers:
            self._parsers = parsers
        else:
            self._parsers = []

    def has_source(self, name):
        """
        Return True if source name is found
        """
        return (name in self._sources)

    def add_source(self, name, init_value):
        """
        Add a source to the storage dict.
        Override if something else is needed.
        """
        if not self.has_source(name):
            self._sources[name] = init_value

        if Statistics.on:
            Statistics.set(self.name + ".sources.count", len(self._sources))

    def get_sources(self):
        "Return source storage"
        return self._sources

    def get_source(self, name):
        "Return named source"
        return self._sources[name]

    def get_parsers(self):
        "Return parser storage"
        return self._parsers
    
    def add_parser(self, parser):
        "Add parser if not already exists"
        if not parser in self._parsers:
            self._parsers.append(parser)

    def run(self):
        """
        Override this function in controller. Example:

        .. code-block:: python

            def run(self):
                self.logger.info("Running")

                while not self.has_interrupt():
                    self.loop_incoming() # dispatch handle_* functions
                    self.loop_outgoing() # dispatch poll_* functions

                self.logger.info("Stopped")

        """
        raise NotImplementedError

    def fetch_one_incoming(self):
        """
        Returns one message from the queue.

        :returns: tuple of (messagetype, incoming)
        :rtype: tuple(netdef.Shared.SharedQueues.MessageType, netdef.Sources.BaseSource.BaseSource)
        """
        try:
            if not self.has_interrupt():
                messagetype, incoming = self.incoming.get(block=True, timeout=self.queue_timeout)
                self._statistics_update_last_minute(1)
                return messagetype, incoming

        except queue.Empty:
            self._statistics_update_last_minute(0)
            return None, None

    def loop_incoming(self):
        """
        Get every message from the queue and dispatch the associated handler function
        """
        try:
            while not self.has_interrupt():
                messagetype, incoming = self.incoming.get(block=True, timeout=self.queue_timeout)

                self._statistics_update_last_minute(1)

                if messagetype == self.messagetypes.READ_ALL:
                    self.handle_readall(incoming)
                elif messagetype == self.messagetypes.ADD_SOURCE:
                    self.handle_add_source(incoming)
                elif messagetype == self.messagetypes.READ_SOURCE:
                    self.handle_read_source(incoming)
                elif messagetype == self.messagetypes.WRITE_SOURCE:
                    self.handle_write_source(incoming[0], incoming[1], incoming[2])
                elif messagetype == self.messagetypes.ADD_PARSER:
                    self.handle_add_parser(incoming)
                elif messagetype == self.messagetypes.TICK:
                    self.handle_tick(incoming)
                elif messagetype == self.messagetypes.APP_STATE:
                    self.handle_app_state(incoming)
                else:
                    raise NotImplementedError
                self.incoming.task_done()

        except queue.Empty:
            self._statistics_update_last_minute(0)

    def handle_tick(self, incoming):
        """
        Answer the tick message
        """
        incoming.tick()

    def handle_app_state(self, app_state):
        """
        Override if controller need to react to application states
        """
        if app_state == self.appstatetypes.RUNNING:
            self.handle_app_state_running()
        elif app_state == self.appstatetypes.SETUP:
            self.handle_app_state_setup()

    def handle_app_state_running(self):
        """
        Override if controller need to react to running state
        """
        self.logger.debug("Entering running state")

    def handle_app_state_setup(self):
        """
        Override if controller need to react to setup state
        """
        self.logger.debug("Entering setup state")

    def handle_add_parser(self, incoming):
        "Add parser to controller if not already exists"
        self.add_parser(incoming)

    def handle_readall(self, incoming):
        raise NotImplementedError

    def handle_add_source(self, incoming):
        raise NotImplementedError

    def handle_read_source(self, incoming):
        raise NotImplementedError

    def handle_write_source(self, incoming, value, source_time):
        raise NotImplementedError

    def loop_outgoing(self):
        """
        Check every source and call the poll_outgoing_item function
        """
        for item in self.get_sources().values():
            self.poll_outgoing_item(item)

    def poll_outgoing_item(self, item):
        raise NotImplementedError

    def send_outgoing(self, outgoing):
        "Send RUN_EXPRESSION message on valuechange"
        self.shared.queues.send_message_to_rule(
            self.shared.queues.MessageType.RUN_EXPRESSION,
            outgoing.rule,
            outgoing
        )

    def statistics_update(self):
        self._statistics_update_last_minute(0)

    @staticmethod
    def update_source_instance_value(source_instance, value, stime, status_ok, oldnew_check):
        """ Updates value, timestamp and state on given source_instance
            Returns True if source_instance have triggered a value change
        """

        prev_val = source_instance.get
        prev_st = source_instance.status_code

        if status_ok:
            if oldnew_check:
                if prev_val == value and prev_st in (StatusCode.GOOD, StatusCode.INITIAL):
                    return False
            source_instance.get = value
            source_instance.source_time = stime
            if prev_st == StatusCode.NONE:
                source_instance.status_code = StatusCode.INITIAL
            else:
                source_instance.status_code = StatusCode.GOOD

            # event til uttrykk sendes bare på gode verdier.
            return True

        else:
            if oldnew_check:
                if prev_val == value and prev_st == StatusCode.INVALID:
                    return False
            source_instance.get = value
            source_instance.source_time = stime
            if prev_st != StatusCode.NONE:
                source_instance.status_code = StatusCode.INVALID
        
            return False
