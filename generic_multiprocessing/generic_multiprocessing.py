import multiprocessing
import subprocess
from abc import ABCMeta, abstractmethod


class TaskManager(object):
    __metaclass__ = ABCMeta

    def __init__(self, n_processes=None, *args, **kwargs):
        self._task_queue = multiprocessing.Queue()
        self._n_processes = multiprocessing.cpu_count()
        if n_processes is not None:
            self._n_processes = n_processes - 1
        self.args = args
        self.kwargs = kwargs

    def add_task(self, task):
        if isinstance(task, TaskBase):
            self._task_queue.put(task)

    def start(self):
        processes = list()
        for _ in range(self._n_processes):
            p = multiprocessing.Process(target=self._process_tasks)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    def _process_tasks(self):
        while not self._task_queue.empty():
            task = self._task_queue.get()
            task.start_task(self.args, self.kwargs)
        return True


class TaskBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_task(self, *args, **kwargs):
        pass