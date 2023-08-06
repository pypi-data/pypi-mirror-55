import threading
from queue import Queue
import logging
from time import sleep
from abc import ABC, abstractmethod


class TaskRunnable(ABC):
    @abstractmethod
    def run(self):
        ...


class TaskThreadRunner(threading.Thread):
    TOTAL_THREADS = 0

    def __init__(self, queue: Queue, group=None, target=None, name=None):
        super(TaskThreadRunner, self).__init__(
            group=group,
            target=target,
            name=name
        )
        self.queue = queue
        self.killed = False
        self._is_busy = False
        TaskThreadRunner.TOTAL_THREADS += 1

    def kill(self):
        self.killed = True

    def is_busy(self):
        return self._is_busy

    def is_idle(self):
        return not self._is_busy

    def run(self):
        logging.debug("Starting thread: %s" % self.name)
        while True:
            if self.killed:
                logging.debug("Stopping thread: %s" % self.name)
                break
            if not self.queue.empty():
                self._is_busy = True
                class_runnable: TaskRunnable = self.queue.get()
                class_runnable.run()
                self._is_busy = False
            else:
                sleep(1)

    def __del__(self):
        TaskThreadRunner.TOTAL_THREADS -= 1