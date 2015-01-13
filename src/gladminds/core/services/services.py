from gladminds.core.model_fetcher import models
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue

class Services():
    def __init__(self):
        self.models= models
        self.queue_service = send_job_to_queue
