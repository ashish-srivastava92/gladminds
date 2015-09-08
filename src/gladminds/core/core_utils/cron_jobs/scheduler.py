#!/usr/bin/python
import sys
import json
from boto.sqs.connection import SQSConnection
ACCESS_KEY = 'AKIAIL7IDCSTNCG2R6JA'
SECRET_KEY = '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'


class TaskQueue:

    def add(self, task_name, task_params=None, **kwargs):
        pass


task_info = {
    "expire_service_coupon": {
        "time_taken": 0
    },
    "export_coupon_redeem_to_sap": {
        "time_taken": 0
    },
    "export_customer_reg_to_sap": {
        "time_taken": 0
    },
    "send_report_mail_for_feed": {
        "day_duration": 1
    },
    "send_reminder": {
        "reminder_day": 7
    },
    "import_data": {
        "time_taken": 0
    },
    "send_schedule_reminder": {
        "time_taken": 0
    },
    "delete_unused_otp": {
    },
    "send_reminders_for_servicedesk": {
        "time_taken": 0
    }
}


class SqsTaskQueue(TaskQueue):

    def __init__(self, sqs_name, brand):
        self._conn = SQSConnection(ACCESS_KEY, SECRET_KEY)
        self._q = self._conn.get_queue(sqs_name)
        self.brand = brand

    def add(self, task_name, brand, task_params=None, **kwargs):
        task_params = task_info.get(task_name, {"time_taken": 0})
        task_params.update({"brand": self.brand})
        payload = {
            "task_name": task_name,
            "params": task_params
        }
        payload_as_str = json.dumps(payload)
        self._conn.send_message(self._q, payload_as_str)


# QUEUE_NAME = sys.argv[2]
# taskqueue = SqsTaskQueue(QUEUE_NAME)
# 
# if __name__ == '__main__':
#     task_name = sys.argv[1]
#     # task_params = {"time": sys.argv[1]}
#     # task_params = {"trigger_time":int(time.time())}
#     taskqueue.add(task_name)