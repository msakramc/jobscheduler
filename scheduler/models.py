from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    PENDING = 'Pending'
    RUNNING = 'Running'
    COMPLETED = 'Completed'
    FAILED = 'Failed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]
    
    name = models.CharField(max_length=255)
    estimated_duration = models.IntegerField()  # in seconds
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    taskid = models.CharField(max_length=250, null=True, blank=True)
    execution_order = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
