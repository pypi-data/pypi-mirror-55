import sys

sys.path.append("/Users/wuzi/PycharmProjects/distributed_schedule")

from distributed_schedule.tasks import Task, register_task
from distributed_schedule.client import main

import time


class Test2Task(Task):

    def execute(self, *args, **kwargs):
        print("Test2Task task {0}  {1}".format(args, kwargs))
        time.sleep(1)
        print("Test2Task over ")


class TestD2Task(Task):

    def execute(self, *args, **kwargs):
        print("TestD2Task task {0}  {1}".format(args, kwargs))
        time.sleep(1)
        print("TestD2Task over ")


register_task(Test2Task("test2_task"))
register_task(TestD2Task("test2d_task"))

main()