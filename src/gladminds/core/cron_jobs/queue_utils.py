from django.conf import settings
from gladminds.core.exceptions import ParamToBeFunctionException
from gladminds.core.cron_jobs.taskqueue import SqsTaskQueue


def get_task_queue(brand=None):
    if brand is None:
        brand = settings.BRAND
    queue_name = settings.SQS_QUEUE_NAME
    return SqsTaskQueue(queue_name, brand)


def check_celery_running():
    '''
    Check whether celery is running or not
    '''
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if d:
            return True
    except:
        pass
    return False


def send_job_to_queue(task, task_params, brand=None):
    '''
    Sends a job to queue
    :param task_name:
    :type string:
    :param task_params:
    :type dict:
    :param brand:
    :type string:
    '''
    if not hasattr(task, '__call__'):
        raise ParamToBeFunctionException
    if brand is None:
        brand = settings.BRAND
    task_params.update({'brand': brand})

    if settings.ENABLE_AMAZON_SQS:
        queue_name = settings.SQS_QUEUE_NAME
        task_name = task.__name__
        SqsTaskQueue(queue_name, brand).add(task_name, task_params)
    else:
        if check_celery_running():
            task.delay(**task_params)
        else:
            task(**task_params)
