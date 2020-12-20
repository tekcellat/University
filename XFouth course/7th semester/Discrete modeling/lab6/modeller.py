from collections import deque
from generator import ExponentialGenerator


class QueueSystemError(Exception):
    pass


class AllReceiversBusyError(QueueSystemError):
    pass


class Request(object):
    fmt = '{:.2f}'

    def __init__(self, creation_time):
        self._creation_time = creation_time
        self._processing_start = self._processing_end = 0
        self._dropped = False

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def processing_start(self):
        return self._processing_start

    @processing_start.setter
    def processing_start(self, value):
        self._processing_start = value

    @property
    def processing_end(self):
        return self._processing_end

    @processing_end.setter
    def processing_end(self, value):
        self._processing_end = value

    def __str__(self):
        return self.fmt.format(self._creation_time)

    def __repr__(self):
        return self.fmt.format(self._creation_time)


class Device(object):
    def __init__(self, generator, name):
        self._generator = generator
        self._name = name
        self._receivers = []
        self._next_event_time = 0
        self._requests = 0
        self._dropped_requests = 0
        self._idle = False

    @property
    def name(self):
        return self._name

    def __str__(self):
        return '{} - {:.2f}'.format(self._name, self._next_event_time)

    def __repr__(self):
        return '{} - {:.2f}'.format(self._name, self._next_event_time)

    @property
    def next_event_time(self):
        return self._next_event_time

    @property
    def requests(self):
        return self._requests

    @property
    def dropped_requests(self):
        return self._dropped_requests

    @property
    def idle(self):
        return self._idle

    def add_receiver(self, receiver):
        if receiver not in self._receivers:
            self._receivers.append(receiver)

    def add_receivers(self, receivers):
        for receiver in receivers:
            self.add_receiver(receiver)

    def generate_time(self):
        return self._generator.next()

    def emit_request(self, request):
        potential_receivers = [receiver for receiver in self._receivers if
                               receiver.can_receive_request()]
        if not potential_receivers or request._dropped:
            self._dropped_requests += 1
            return None
        potential_receiver = min(potential_receivers, key=lambda rcvr: rcvr.occupation)
        potential_receiver.receive_request(request)
        return potential_receiver

    def action(self):
        raise NotImplementedError


class RequestGenerator(Device):
    def __init__(self, generator, name, *, request_count=float('inf')):
        super().__init__(generator, name)
        self._count = request_count

    @property
    def generated_requests(self):
        return self._requests

    def __generate_request(self):
        self.emit_request(Request(self._next_event_time))
        self._next_event_time += self.generate_time()
        self._requests += 1

    def action(self):
        if not self._receivers:
            raise RuntimeError('No receivers bound to {}'.format(self._name))
        self.__generate_request()
        if self._requests >= self._count:
            self._idle = True


class RequestProcessor(Device):
    """
    Request processor

    Notes about implementation:
    1)  Request processing is always performed over a request in queue at index 0 (zero). Therefore,
        real queued request count is _queued_requests - 1.
    """
    def __init__(self, generator, name, *, max_queue_size=float('inf'), 
                is_exit=False, can_drop=False):
        super().__init__(generator, name)
        self._queue = deque()
        self._max_queue_size = max_queue_size
        self._current_queue_size = 0
        self._queued_requests = 0
        self._max_waiting_time = 0
        self._idle_time = self._active_time = 0
        self._idle = True
        self._is_exit = is_exit
        self._can_drop = can_drop
        if can_drop:
            self.drop_prob_gen = ExponentialGenerator()
        else:
            self.drop_prob_gen = None
        

    @property
    def processed_requests(self):
        return self._requests

    @property
    def max_waiting_time(self):
        return self._max_waiting_time

    @property
    def queue_size(self):
        return self._current_queue_size

    @property
    def queued_requests(self):
        # See Note 1 in class docstring
        return self._queued_requests - 1

    @property
    def idle_time(self):
        return self._idle_time

    @property
    def active_time(self):
        return self._active_time

    @property
    def utilization(self):
        try:
            util = self._active_time / (self._active_time + self.idle_time)
        except ZeroDivisionError:
            util = 0.0
        return util

    def can_receive_request(self):
        # See Note 1 in class docstring
        if self._queued_requests - 1 < self._max_queue_size:
            return True
        return False

    @property
    def occupation(self):
        return self._queued_requests

    def receive_request(self, request):
        
        self._queue.append(request)
        self._queued_requests += 1
        if self._idle:
            self.__process_request()
        # See Note 1 in class docstring
        elif self._current_queue_size < self._queued_requests - 1 <= self._max_queue_size:
            self._current_queue_size += 1
        elif self._queued_requests - 1 <= self._max_queue_size:
            pass
        else:
            self._queue.pop()
            self._queued_requests -= 1
            self._dropped_requests += 1
            raise QueueSystemError('Receiver is busy. Emitter should check availability with '
                                   'can_receive_request()')

    def __process_request(self):
        if self._idle:
            request = self._queue[0]
            self._idle_time += request.creation_time - self._next_event_time
            request.processing_start = request.creation_time
            self._next_event_time = request.creation_time + self.generate_time()
            self._idle = False
        else:
            request = self._queue.popleft()
            self._queued_requests -= 1
            current_time = self._next_event_time
            request.processing_end = current_time
            self._max_waiting_time = max(request.processing_start - request.creation_time,
                                         self._max_waiting_time)
            self._requests += 1
            self._active_time += request.processing_end - request.processing_start

            if self._queued_requests == 0:
                self._idle = True
            else:
                self._queue[0].processing_start = current_time
                self._next_event_time += self.generate_time()

            new_request = Request(current_time)
            if self._can_drop:
                prob = self.drop_prob_gen.next()
                if prob < 0.9:
                    new_request._dropped = True

            if not self._is_exit:
                self.emit_request(new_request)

    def action(self):
        if not self._receivers and not self._is_exit:
            raise RuntimeError('No receivers bound to {}'.format(self._name))
        self.__process_request()


def event_based_modelling(devices, condition):
    try:
        while not condition():
            device = min(filter(lambda x: not x.idle, devices), key=lambda x: x.next_event_time)
            device.action()
    except ValueError:
        print('Condition cannot be achieved with given model.')


if __name__ == '__main__':
    pass