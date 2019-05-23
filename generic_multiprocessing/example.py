import random
from time import sleep
import multiprocessing
import subprocess
from generic_multiprocessing import TaskManager, TaskBase


class MyTask(TaskBase):

    def __init__(self, i):
        self.i = i

    def start_task(self, *locks):
        sleep(random.uniform(0, .2))
        print_lock = locks[0][0]
        cmd = ' '.join(['ls -l && echo', str(self.i)])
        out = subprocess.check_output(cmd, shell=True)
        with print_lock:
            print(out.decode('utf-8'))


def run():
    tm = TaskManager(None, multiprocessing.Lock())
    for _ in range(1000):
        tm.add_task(MyTask(_))
    tm.start()


if __name__ == '__main__':
    run()