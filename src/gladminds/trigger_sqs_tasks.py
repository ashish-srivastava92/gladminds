import sys
from scheduler import SqsTaskQueue

QUEUE_NAME = sys.argv[2]
taskqueue = SqsTaskQueue(QUEUE_NAME)
task_name = sys.argv[1]
taskqueue.add(task_name)
