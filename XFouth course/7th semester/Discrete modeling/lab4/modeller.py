__author__ = 'monomah'


import numpy.random as nr


class UniformGenerator:
    def __init__(self, a, b):
        if not 0 <= a <= b:
            raise ValueError('Параметры должны удовлетворять условию 0 <= a <= b')
        self._a = a
        self._b = b

    def next(self):
        return nr.uniform(self._a, self._b)


class ExponentialGenerator:
    def __init__(self, lmbd):
        self._lambda = 1 / lmbd

    def next(self):
        return nr.exponential(self._lambda)


class RequestGenerator:
    def __init__(self, generator):
        self._generator = generator
        self._receivers = set()

    def add_receiver(self, receiver):
        self._receivers.add(receiver)

    def remove_receiver(self, receiver):
        try:
            self._receivers.remove(receiver)
        except KeyError:
            pass

    def next_time_period(self):
        return self._generator.next()

    def emit_request(self):
        for receiver in self._receivers:
            receiver.receive_request()


class RequestProcessor(RequestGenerator):
    def __init__(self, generator, reenter_probability=0):
        super().__init__(generator)
        self._generator = generator
        self._current_queue_size = 0
        self._max_queue_size = 0
        self._processed_requests = 0
        self._reenter_probability = reenter_probability
        self._reentered_requests = 0

    @property
    def processed_requests(self):
        return self._processed_requests

    @property
    def max_queue_size(self):
        return self._max_queue_size

    @property
    def current_queue_size(self):
        return self._current_queue_size

    @property
    def reentered_requests(self):
        return self._reentered_requests

    def process(self):
        if self._current_queue_size > 0:
            self._processed_requests += 1
            self._current_queue_size -= 1
            self.emit_request()
            if nr.random_sample() < self._reenter_probability:
                self._reentered_requests += 1
                self.receive_request()

    def receive_request(self):
        self._current_queue_size += 1
        if self._current_queue_size > self._max_queue_size:
            self._max_queue_size += 1

    def next_time_period(self):
        return self._generator.next()


class Modeller:
    def __init__(self, uniform_a, uniform_b, expo_lambda, reenter_prop):
        self._generator = RequestGenerator(UniformGenerator(uniform_a, uniform_b))
        self._processor = RequestProcessor(ExponentialGenerator(expo_lambda), reenter_prop)
        self._generator.add_receiver(self._processor)

    def event_based_modelling(self, request_count):
        generator = self._generator
        processor = self._processor

        gen_period = generator.next_time_period()
        proc_period = gen_period + processor.next_time_period()
        while processor.processed_requests < request_count:
            if gen_period <= proc_period:
                generator.emit_request()
                gen_period += generator.next_time_period()
            if gen_period >= proc_period:
                processor.process()
                if processor.current_queue_size > 0:
                    proc_period += processor.next_time_period()
                else:
                    proc_period = gen_period + processor.next_time_period()

        return (processor.processed_requests, processor.reentered_requests,
                processor.max_queue_size, proc_period)

    def time_based_modelling(self, request_count, dt):
        generator = self._generator
        processor = self._processor

        gen_period = generator.next_time_period()
        proc_period = gen_period + processor.next_time_period()
        current_time = 0
        while processor.processed_requests < request_count:
            if gen_period <= current_time:
                generator.emit_request()
                gen_period += generator.next_time_period()
            if current_time >= proc_period:
                processor.process()
                if processor.current_queue_size > 0:
                    proc_period += processor.next_time_period()
                else:
                    proc_period = gen_period + processor.next_time_period()
            current_time += dt

        return (processor.processed_requests, processor.reentered_requests,
                processor.max_queue_size, current_time)
