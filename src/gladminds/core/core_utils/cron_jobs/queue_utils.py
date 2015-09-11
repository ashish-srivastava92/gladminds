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


def queue_job(task, task_params, queue_name, delay_seconds=None, brand=None):
    '''
    queues jobs
    :param task:
    :type task:
    :param task_params:
    :type task_params:
    :param queue_name:
    :type queue_name:
    :param delay_seconds:
    :type delay_seconds:
    :param brand:
    :type brand:
    '''
    if not hasattr(task, '__call__'):
        raise ParamToBeFunctionException
    if brand is None:
        brand = settings.BRAND
    task_params.update({'brand': brand})

    if settings.ENABLE_AMAZON_SQS:
        task_name = task.__name__
        SqsTaskQueue(queue_name, brand).add(task_name, task_params,
                                            delay_seconds=delay_seconds)
    else:
        if check_celery_running():
            if delay_seconds is None:
                task.delay(**task_params)
            else:
                task.apply_async(kwargs=task_params, countdown=delay_seconds)
        else:
            task(**task_params)


def send_job_to_sms_queue(task, task_params, delay_seconds=None, brand=None):
    queue_name = getattr(settings, 'SQS_QUEUE_NAME_SMS', None)
    queue_job(task, task_params, queue_name, delay_seconds=delay_seconds,
              brand=brand)


def send_job_to_queue(task, task_params, delay_seconds=None, brand=None):
    queue_name = getattr(settings, 'SQS_QUEUE_NAME', None)
    if 'phone_number' in task_params.keys():
        queue_name = getattr(settings, 'SQS_QUEUE_NAME_SMS', queue_name)
    queue_job(task, task_params, queue_name, delay_seconds=delay_seconds,
              brand=brand)
