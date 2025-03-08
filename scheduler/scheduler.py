from celery import shared_task
from datetime import datetime
import time
from heapq import heappop, heappush
from .models import Job
from django.db.models import Q
from celery.result import AsyncResult
from config.celery import app


# Priority Queue class to manage jobs by priority and deadline
class JobScheduler:
    def __init__(self):
        self.job_queue = []  # The main queue of jobs to be scheduled
        self.pending_running_job_queue = []

    def add_job(self, job):
        """Add a job to the queue based on priority and deadline."""
        # Push jobs into the priority queue with negative priority for max-heap behavior
        heappush(self.job_queue, (job.deadline, -job.priority, job.estimated_duration, job))
    
    def add_pending_running_job(self, job):
        """Add a job to the queue based on priority and deadline."""
        # Push jobs into the priority queue with negative priority for max-heap behavior
        heappush(self.pending_running_job_queue, (job.deadline, -job.priority, job.estimated_duration, job))

    def get_next_job(self):
        """Pop the job with the highest priority and earliest deadline."""
        if self.job_queue:
            return heappop(self.job_queue)[3]  # Return the job object
        return None
    

    def check_task_priority(self, job):
        if job.status == "Pending":
            if Job.objects.filter(status="Running").count() == 3:
                position  = 0
                for index, job_tuple in enumerate(reversed(self.pending_running_job_queue)):
                    job_fetch = job_tuple[-1]
                    if job_fetch.name == job.name:
                        position = index
                    if job_fetch.status == "Running":
                        if index > position:
                            job_fetch.status = "Pending"
                            job_fetch.start_time = None
                            job_fetch.save()
                            app.control.purge()
                            app.control.revoke(job_fetch.taskid, terminate=True)
                            self.add_job(job_fetch)
                            print(f"Task {job_fetch.taskid} terminated.")


# Global job scheduler instance
scheduler = JobScheduler()

@shared_task(bind=True)
def execute_job(self, job_id):
    try:
        """Celery task to execute a job."""
        job = Job.objects.get(id=job_id)

        # Set job status to running
        job.start_time = datetime.now()
        job.taskid = self.request.id
        job.status = 'Running'

        job.save()

        # Simulate job execution (sleep for the execution time)
        
        time.sleep(job.estimated_duration)
        if Job.objects.get(id=job_id).status == "Running":
            job.status = 'Completed'
            job.end_time = datetime.now()
            job.save()
        # After the current job is completed, check if there is a pending job
            print(f"Job {job.name} Completed")
    except Exception as e:
        job.status = 'Failed'
        job.save()
        print(f"Job {job.name} Failed")
        return False

def schedule_jobs():
    """Schedule jobs based on priority and deadlines."""
    # Fetch all jobs that are pending
    pending_jobs = Job.objects.filter(Q(status='Pending'))
    running_pending_job = Job.objects.filter(Q(status='Pending') | Q(status='Running')).order_by('status')
    # Add jobs to the scheduler based on priority and deadline
    for job in pending_jobs:
        scheduler.add_job(job)
    
    for run in running_pending_job:
        scheduler.add_pending_running_job(run)

    # Process the jobs in the order of priority and deadline
    print(pending_jobs,"PENDING")
    print(running_pending_job,"PENDING RUNNING")
    while scheduler.job_queue:
        next_job = scheduler.get_next_job()
        
        if next_job:
            # Execute the next job in the scheduler
            scheduler.check_task_priority(next_job)
            execute_job.apply_async((next_job.id,))
    



