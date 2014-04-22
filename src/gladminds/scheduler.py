#!/usr/bin/python
import sys
import json
import time
from boto.sqs.connection import SQSConnection

class TaskQueue:
    def add(self, task_name, task_params=None, **kwargs):
        pass

class SqsTaskQueue(TaskQueue):
    def __init__(self, sqs_name):
        self._conn = SQSConnection()
        self._q = self._conn.get_queue(sqs_name)

    def add(self, task_name, task_params=None, **kwargs):
        task_params = task_params or {}
        payload = {
                "task_name": task_name,
                "params" : task_params
            }
        payload_as_str = json.dumps(payload)
        self._conn.send_message(self._q,payload_as_str)


QUEUE_NAME = "lithium-dashboard-dev-worker"
taskqueue = SqsTaskQueue(QUEUE_NAME)

if __name__ == '__main__':
    task_name = sys.argv[1]
    #task_params = sys.argv[2]
    task_params = {"trigger_time":int(time.time())}
    taskqueue.add(task_name,task_params)

