'''
Created on 21-Jan-2014

@author: sripathikrishnan
'''


#_task_map = { "task_name":task_handler}
# task_queue = SqsTaskQueue(queue_name)
# or 
# task_queue = MutlProcessQueue(_task_map)
# If SQS Queue, also define the following in urls.py
# url(r'^tasks/', SqsHandler.as_view(task_map=_tasks_map)),
# Finally, you execute a task like this -
# task_queue.add("send_fresher_email_registration", fresher)
#Note: ACCESS KEY and SECRET KEY need to set in enviornment variable

import json
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseServerError,\
    HttpResponseBadRequest
from boto.sqs.connection import SQSConnection

class TaskQueue:
    def add(self, task_name, task_params=None, **kwargs):
        pass

class SqsHandler(View):
    task_map = None
    def __init__(self, **kwargs):
        super(SqsHandler, self).__init__(**kwargs)
        task_map = {} if not 'task_map' in kwargs else kwargs['task_map']
        if not isinstance(task_map, dict):
            raise Exception("task_map must be a dictionary mapping task names to a callable/function that will perform the task")
        self._validate_task_map(task_map)
        self.task_map = task_map
    
    def _validate_task_map(self, task_map):
        #Validate the task_map, fail fast if it isn't valid
        for task_name, task_handler in task_map.items():
            if not task_name:
                raise Exception("")
            if not callable(task_handler):
                raise Exception("task_handler for task %s is not a callable. Expected a callable, found %s instead" 
                                % (task_name, type(task_handler)))
    
    def post(self, request):
        if request.META["CONTENT_TYPE"] == 'application/json':
            try:
                self._handler_tasks(request.body)        
                return HttpResponse(content="Task Completed")
            except Exception as e:
                return HttpResponseServerError(content=e)
        else:
            return HttpResponseBadRequest(content="Needed Content-Type in application/json")
    
    def _handler_tasks(self,payload_as_str):
        payload = json.loads(payload_as_str)
        task_name = payload["task_name"]
        params = payload["params"]
        handler = self.task_map[str(task_name)]
        handler(**params)
    
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

class MultiProcessQueue(TaskQueue):
    """ A simple implementation of a background jobs, FOR DEVELOPMENT USE ONLY
    
    This implementation launches a background process to execute the task. If the foreground process terminats, background jobs are not executed.
    This isn't fit for use in a production environment. Use SqsQueue instead.
    
    """
    def __init__(self, task_map):
        from multiprocessing import Pool
        self._worker_pool = Pool(2)
        self._task_map = task_map
    
    def add(self, task_name, task_params=None, **kwargs):
        task_params = task_params or {}
        if not task_name in self._task_map:
            raise Exception("Task %s not definied in task_map. No task definition found, cannot proceed" % task_name)

        task_handler = self._task_map[task_name]
        if not callable(task_handler):
            raise Exception("""Task %s does not define a method or class that can be called.
                 Must be a callable, instead found %s""" % (task_name, type(task_handler)))
        
        self._worker_pool.apply_async(task_handler, [task_params])
