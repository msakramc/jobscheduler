from celery import shared_task
import time
from datetime import datetime
from .models import Job

# @shared_task(bind=True)
# def execute_job(self,job_id):
#     """
#     This is the Celery task to execute a job asynchronously.
#     """
#     job = Job.objects.get(id=job_id)
#     print(f"Executing Job: Priority={job.priority}, Deadline={job.deadline}, Job={job}")

#     job.start_time = datetime.now()
#     job.status = 'Running'
#     job.taskid = self.request.id
#     job.save()

#     # Simulate job execution
#     time.sleep(job.estimated_duration)  # assuming estimated_duration is in seconds

#     # After job completion, update job status
#     job.status = 'Completed'
#     job.end_time = datetime.now()
#     job.save()

@shared_task
def my_task():
    # Task logic here
    return "Task completed"