from queue import Queue

import logging


logger = logging.getLogger(__name__)


queue = Queue()


class Task(object):

    def __init__(self, task_name):
        self.task_name = task_name

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class Tasks(list):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Tasks, cls).__new__(cls, *args, **kw)
        return cls._instance


def register_task(task):
    global tasks
    tasks.append(task)
    return tasks


tasks = Tasks()


# class TaskOne(Task):
#
#     def execute(self, *args, **kwargs):
#         print("task execute  {0}".format(self.task_name))
#         print("task one  {0}  {1} ".format(args, kwargs))
#
# for i in [TaskOne("task_1"), TaskOne("task_2"), TaskOne("task_3")]:
#     register_task(i)


def worker_threads(worker_nums=5):
    def worker():
        while True:
            try:
                task_msg = queue.get()
            except Exception as e:
                logger.exception("error :  {0}".format(e))
                return
            task_id = task_msg.pop("task_id")
            client = task_msg.pop("client")
            for task in tasks:
                if task.task_name == task_id:
                    res = {"task_id": task_id, "client_id": client.client_name}
                    res.update(task_msg)
                    try:
                        task.execute(**task_msg)
                    except Exception as e:
                        logger.exception(e)
                        res["status"] = "fail"
                    else:
                        res["status"] = "suc"
                    from distributed_schedule.handlers import NotifyTaskStatue
                    data = NotifyTaskStatue().deserialize(data=res)
                    client.write_result(data)

    from threading import Thread
    for i in range(worker_nums):
        t = Thread(target=worker)
        t.setDaemon(False)
        t.start()


worker_threads()

