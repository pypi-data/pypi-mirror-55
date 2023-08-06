from queue import Queue
import time
from cpythreads.threadrunner import ThreadRunner, ThreadRunnable


class ThreadsPoolManager:

    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.task_queue = Queue()
        self.threads_pool = []

    def kill_threads_on_finish(self, *args, **kwargs):
        """
            Wait until all the task in the queue are finished
            then exit the threads and wait to finish the process
        """
        while not self.task_queue.empty():
            time.sleep(1)

        self.safe_kill_threads()

    def safe_kill_threads(self):
        for thread in self.threads_pool:
            thread.kill()
            thread.join()

    def add_thread_to_pool(self):
        thread = ThreadRunner(self.task_queue)
        thread.setDaemon(True)
        thread.start()
        self.threads_pool.append(thread)

    def add_thread_if_needed(self):
        if self.max_threads > len(self.threads_pool):
            for th_runner in self.threads_pool:
                if th_runner.is_idle():
                    return
            self.add_thread_to_pool()

    def add_task(self, task: ThreadRunnable):
        self.task_queue.put(task)
        self.add_thread_if_needed()
