import sys
from gladminds.scheduler import SqsTaskQueue
QUEUE_NAME = sys.argv[2]
taskqueue = SqsTaskQueue(QUEUE_NAME)
        
if __name__ == '__main__':
    task_name = sys.argv[1]
    taskqueue.add(task_name)
