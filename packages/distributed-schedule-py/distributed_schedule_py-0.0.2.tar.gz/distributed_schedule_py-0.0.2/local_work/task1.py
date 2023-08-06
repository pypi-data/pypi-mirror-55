import sys

sys.path.append("/Users/wuzi/PycharmProjects/distributed_schedule")

from distributed_schedule.tasks import Task, register_task
from distributed_schedule.client import main

import time


class TestTask(Task):

    def execute(self, *args, **kwargs):
        print("TestTask task {0}  {1}".format(args, kwargs))
        time.sleep(10)
        print("TestTask over ")


class TestDTask(Task):

    def execute(self, *args, **kwargs):
        print("TestDTask task {0}  {1}".format(args, kwargs))
        time.sleep(1)
        raise
        print("TestDTask over ")


register_task(TestTask("test_task"))
register_task(TestDTask("testd_task"))

main()