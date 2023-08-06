##############################################################################
#
# Copyright (c) 2019 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Helpers to run benchmarks concurrently.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import threading

from pyperf import perf_counter

from zope.interface import implementer

from .interfaces import IDBBenchmark
from .interfaces import IDBBenchmarkCollectionWrapper

from .speedtest import SpeedTestWorker
from .speedtest import ForkedSpeedTestWorker
from ._dbsupport import SharedDBFunction
from ._wrapper import AbstractWrapper
from ._wrapper import AbstractBenchmarkFunctionWrapper
from .fork import distribute

logger = __import__('logging').getLogger(__name__)

def avg(times):
    return sum(times) / len(times)

@implementer(IDBBenchmark)
class AbstractConcurrentFunction(AbstractWrapper):
    """
    Run a benchmark function concurrently across a set of workers and
    return the results.
    """

    mp_strategy = None
    collector_strategies = {
        'max': max,
        'sum': sum,
        'min': min,
        'avg': avg,
    }
    collector_strategy = max

    def __init__(self, workers, func_name):
        assert func_name
        self.func_name = func_name
        self.workers = workers
        if os.environ.get('ZS_COLLECTOR_FUNC') in self.collector_strategies:
            # Instead of using the max recorded time,
            # you may want to use the sum of all the times. This helps
            # account for decreased performance as concurrency increases
            # due to systemic effects. i.e., the database may slow down
            # just slightly; that may effect the max time only a little bit
            # but the overall runtime quite a lot.
            # The min time is similar to the max, but better at ignoring
            # outliers.
            self.collector_strategy = self.collector_strategies[os.environ['ZS_COLLECTOR_FUNC']]

    @property
    def __wrapped__(self):
        return getattr(self.workers[0], self.func_name)

    def __getattr__(self, name):
        # We're a function-like object, delegate to the function
        # on the first worker (which should be identical to everything
        # else).
        # In Python 3.8, multiprocessing using the 'spawn' worker by default
        # on more platforms where previously it used 'fork'. The spawn worker
        # makes a *copy* of the object to run by pickling. Unpickling tries to look up
        # "__getstate__' and '__setstate' on this object (not the type, for some reason)
        # so we can be called in an incomplete state. Catch that and turn missing
        # attributes into AttributeError instead of RecursionError or KeyError.
        try:
            worker = self.__dict__['workers'][0]
            func_name = self.__dict__['func_name']
        except KeyError:
            raise AttributeError(name)
        wrapped = getattr(worker, func_name)
        return getattr(wrapped, name)

    def _distribute(self, func, arg_iter):
        return distribute(func, arg_iter, self.mp_strategy)

    def __call__(self, loops, db_factory):
        begin = perf_counter()
        times = self._distribute(self.worker,
                                 ((w, loops, db_factory) for w in self.workers))
        end = perf_counter()
        return self._result_collector(times, end - begin, db_factory)

    def _result_collector(self, times, total_duration, db_factory):
        raise NotImplementedError

    def worker(self, worker_loops_db_factory, sync):
        # This is the function that's called in the worker, either
        # in a different thread, or in a different process.
        worker, loops, db_factory = worker_loops_db_factory
        assert worker is not None
        assert loops is not None
        assert callable(db_factory)
        assert callable(sync)
        worker.sync = sync
        return self.run_worker_function(worker, self.func_name, loops, db_factory)

    @staticmethod
    def run_worker_function(worker, func_name, loops, db_factory):
        thread = threading.current_thread()
        thread.name = "%s-%s-%s" % (func_name, db_factory.name, worker.worker_number)
        f = getattr(worker, func_name)
        begin = perf_counter()
        time = f(loops, db_factory)
        end = perf_counter()
        logger.debug("Worker %s ran for %s",
                     func_name, end - begin)
        return time


class ForkedConcurrentFunction(AbstractConcurrentFunction):
    mp_strategy = 'mp'

    def _result_collector(self, times, total_duration, db_factory): # pylint:disable=unused-argument
        assert self.mp_strategy == 'mp'
        # We used forking, there was no contention we need to account for.
        # But we do return, not an average, but the *max* time. This
        # lets pyperf do the averaging and smoothing for us and makes it
        # more useful at finding outliers.
        return self.collector_strategy(times)


class ThreadedConcurrentFunction(AbstractConcurrentFunction):
    mp_strategy = 'threads'
    uses_gevent = False
    smooth = not os.environ.get('ZS_NO_SMOOTH')

    def _result_collector(self, times, total_duration, db_factory):
        # We used in-process concurrency. There may be contention to
        # account for.

        # If we use our own wall clock time (*total_duration*), we include all the
        # overhead of distributing the tasks and whatever internal
        # time they didn't want included. OTOH, if we just return the
        # sum (or average) of the individual concurrent runs, some
        # things might get charged more than once (especially with
        # gevent: one can start a timer, switch away to another for an
        # unbounded amount of time while still accumulating clock
        # time, while not even running; this can also happen in
        # threads if the driver releases the GIL frequently. Suppose
        # you have 10 tasks, each of which does 10 things, and each
        # thing takes 1ms, but releases the GIL; the first task runs
        # for 1ms then releases the GIL, the second does the same, and
        # so on. If scheduling is fair or FIFO, by the time the first
        # task runs again, 10ms will already have elapsed; by the time
        # it finishes, 100ms will have elapsed).

        # TODO: Would it make sense to keep these numbers and find
        # some way to add them to the pyperf Run that winds up being
        # computed from this?

        concurrency = len(times)
        actual_duration = total_duration
        recorded_duration = sum(times)
        actual_average = actual_duration / concurrency
        recorded_average = recorded_duration / concurrency
        if recorded_duration > actual_duration and not self.smooth:
            # We think we took longer than we actually did. This means
            # that there was a high level of actual concurrent operations
            # going on, a lot of GIL switching, or gevent switching. That's a good thing!
            # it means you have a cooperative database driver.
            #
            # In that case, we want to treat the concurrency as essentially an extra
            # 'inner_loop' for the benchmark. To do this, we find the biggest one
            # (usually the first to start?) and divide by the concurrency.

            # This "normalization" helps when comparing different
            # types of concurrency. If you're only going to be working
            # with one type of database (fully cooperative, fully
            # non-cooperative), you may not want to do this normalization.
            if self.uses_gevent:
                logger.debug('(gevent-cooperative driver %s)', db_factory.name)
            result = max(times) / concurrency
        else:
            if self.uses_gevent:
                logger.debug('(gevent NON-cooperative driver %s)', db_factory.name)
            result = self.collector_strategy(times)
        logger.debug(
            "Actual duration of %s is %s. Recorded duration is %s. "
            "Actual average is %s. Recorded average is %s. "
            "Result: %s. Times: %s",
            self.func_name, actual_duration, recorded_duration,
            actual_average, recorded_average,
            result, times
        )

        return result

class GeventConcurrentFunction(ThreadedConcurrentFunction):
    uses_gevent = True


@implementer(IDBBenchmarkCollectionWrapper)
class AbstractConcurrentBenchmarkCollection(AbstractBenchmarkFunctionWrapper):
    """
    Creates a speed test worker to match the concurrency level.

    Subclasses need to provide the ``make_function_wrapper`` that
    does the distribution, usually using `ConcurrentFunction`.
    """
    # pylint:disable=abstract-method
    WorkerClass = SpeedTestWorker

    def __init__(self, data, options):
        self.options = options
        self.concurrency = options.concurrency
        self.workers = [self.WorkerClass(i, data) for i in range(self.concurrency)]

    @property
    def delegate(self):
        return self.workers[0]

    @property
    def inner_loops(self):
        return self.workers[0].inner_loops

    @inner_loops.setter
    def inner_loops(self, nv):
        for w in self.workers:
            w.inner_loops = nv


class ThreadedConcurrentBenchmarkCollection(AbstractConcurrentBenchmarkCollection):
    """
    Uses in-process concurrency.
    """
    mp_strategy = 'threads'
    ConcurrentFunction = ThreadedConcurrentFunction


    def __init__(self, data, options):
        super(ThreadedConcurrentBenchmarkCollection, self).__init__(data, options)
        if options.gevent:
            self.ConcurrentFunction = GeventConcurrentFunction

    def make_function_wrapper(self, func_name):
        wrapper = self.ConcurrentFunction(self.workers, func_name)
        assert wrapper.mp_strategy == self.mp_strategy
        return wrapper


class SharedConcurrentBenchmarkCollection(ThreadedConcurrentBenchmarkCollection):
    """
    Uses a shared database for all threads.
    """

    def make_function_wrapper(self, func_name):
        concurrent = super(SharedConcurrentBenchmarkCollection, self).make_function_wrapper(func_name)
        return SharedDBFunction(concurrent)

class _NonConcurrentFunction(AbstractConcurrentFunction):

    def _distribute(self, func, arg_iter):
        import gc
        args = list(arg_iter)
        assert len(args) == 1
        # Do account for GC as part of the single-threaded function.
        # This shows up better on profiling.
        c = gc.collect
        gc.collect = lambda *args: []
        try:
            return func(args[0], lambda msg: None)
        finally:
            gc.collect = c

    def _result_collector(self, times, total_duration, db_factory):
        return times

class NonConcurrentBenchmarkCollection(AbstractConcurrentBenchmarkCollection):
    """
    Doesn't actually use any concurrency.

    This exists to provide a uniform interface for things like
    profiling.
    """

    def __init__(self, data, options):
        super(NonConcurrentBenchmarkCollection, self).__init__(data, options)
        assert len(self.workers) == 1

    def make_function_wrapper(self, func_name):
        # pylint:disable=no-value-for-parameter
        # Some storages are very expensive to open, and some benchmarks
        # open and close storages (when they really should probably be explicitly
        # clearing caches)...that makes interpreting profiles hard. So
        # only open them once.

        return SharedDBFunction(_NonConcurrentFunction(self.workers, func_name))


class ForkedConcurrentBenchmarkCollection(ThreadedConcurrentBenchmarkCollection):
    mp_strategy = 'mp'
    WorkerClass = ForkedSpeedTestWorker
    ConcurrentFunction = ForkedConcurrentFunction

    def __init__(self, data, options):
        super(ForkedConcurrentBenchmarkCollection, self).__init__(data, options)
        assert not options.threads
        assert not options.gevent
