import threading
from utils.redis_utils import RedisQueue
from core.processor import Processor
from config import THREAD_NUM


class MessageThreadPool(object):
    def __init__(self, thread_num):
        self.threads = []
        self.task_queue = RedisQueue("task")
        self.running = 0
        self.thread_num = thread_num
        self._init_pool()

    def _init_pool(self):
        for _ in range(self.thread_num):
            self.threads.append(MessageWorker(self))

    def start_task(self):
        for item in self.threads:
            item.start()

    def increase_running(self):
        self.running += 1

    def decrease_running(self):
        self.running -= 1

    def add_task(self, content):
        self.task_queue.put(content)

    def get_task(self):
        content = self.task_queue.get()
        return content


class MessageWorker(threading.Thread):
    def __init__(self, thread_pool):
        super(MessageWorker, self).__init__()
        self.thread_pool = thread_pool

    def run(self):
        print(threading.current_thread().getName())
        while True:
            try:
                content = self.thread_pool.get_task()
                self.thread_pool.increase_running()
                print("get task {}".format(content))
                Processor.distribute(content['topic'], content['payload'])
            except (Exception,) as e:
                print(e)
            finally:
                self.thread_pool.decrease_running()


message_thread_pool = MessageThreadPool(THREAD_NUM)
