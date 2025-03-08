from rest_framework import serializers
from .models import Job
from datetime import datetime,timezone, timedelta

class JobSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    created_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    deadline = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    user = serializers.CharField(source='user.username', read_only=True)
    priority = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'name', 'estimated_duration', 'priority', 'deadline', 'status', 'user','start_time', 'end_time', 'created_datetime']

    def get_priority(self, obj):
        priority_map = {1: 'High', 2: 'Medium', 3: 'Low'}
        return priority_map.get(obj.priority, 'Unknown')
    
class JobCreateSerializer(serializers.ModelSerializer):

    # Custom validation for the 'name' field
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Job name is required.")
        return value

    # Custom validation for the 'estimated_duration' field
    def validate_estimated_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Estimated duration must be a positive number.")
        return value
    
    # Custom validation for the 'priority' field
    def validate_priority(self, value):
        if not any(value == item[0] for item in Job.PRIORITY_CHOICES):
            raise serializers.ValidationError("Invalid priority value. Choose from Low, Medium, High.")
        return value
    
    # Custom validation for the 'deadline' field
    def validate_deadline(self, value):
        value = value.replace(tzinfo=timezone.utc)

        # Check if deadline is in the future
        if value <= datetime.now(timezone.utc):
            raise serializers.ValidationError("Deadline must be in the future.")
        return value
    class Meta:
        model = Job
        fields = ['name', 'estimated_duration', 'priority', 'deadline']