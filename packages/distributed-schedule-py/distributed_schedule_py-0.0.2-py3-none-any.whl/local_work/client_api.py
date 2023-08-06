import sys

from distributed_schedule.client import TaskClient, Client
from distributed_schedule.config import set_logging_level

sys.path.append("/Users/wuzi/PycharmProjects/distributed_schedule")

set_logging_level(20)


c = Client("client")
c.start()

tclient = TaskClient(c)


print("start")
res = tclient.submit("test_task", shard=5)
#
print(res)

res = tclient.submit("test_task", mode="all")
print(res)


res = tclient.submit("test2d_task", mode="once")
print(res)

