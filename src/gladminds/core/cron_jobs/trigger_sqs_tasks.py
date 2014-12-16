import sys
from scheduler import SqsTaskQueue
from gladminds.core.auth_helper import GmApps

QUEUE_NAME = sys.argv[2]
try:
    brand = sys.argv[3]
except:
    brand = GmApps.BAJAJ
taskqueue = SqsTaskQueue(QUEUE_NAME, brand)
task_name = sys.argv[1]
taskqueue.add(task_name, brand)

