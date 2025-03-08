from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import JobSerializer, JobCreateSerializer
from rest_framework.filters import SearchFilter
from rest_framework import status, generics
from .scheduler import schedule_jobs, group_schedule_job
from config.celery import app
from django.db.models import F, ExpressionWrapper, fields, Sum, Count
from django.utils import timezone
from rest_framework.views import APIView

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def logout_confirm_view(request):
    return render(request, 'accounts/logout.html')

def logout_view(request):
    logout(request)
    return redirect(f'/accounts/login/?next=/')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(form.is_valid())
            return redirect('/')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


class CustomPagination(PageNumberPagination):
    permission_classes = [IsAuthenticated]
    page_size_query_param = 'per_page'
    max_page_size = 100

class JobList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.all()
    pagination_class = CustomPagination
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        status_filter = self.request.query_params.get('status', 'all')
        
        if status_filter != 'all':
            queryset = queryset.filter(status=status_filter)

        queryset = queryset.order_by('-created_datetime')
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        jobs_query_set = Job.objects.filter(user=self.request.user)
        job_status = {
            'all': jobs_query_set.count(),
            'completed': jobs_query_set.filter(status="Completed").count(),
            'running': jobs_query_set.filter(status="Running").count(),
            'pending': jobs_query_set.filter(status="Pending").count(),
            'failed': jobs_query_set.filter(status="Failed").count(),

        }
        jobs_query_set = jobs_query_set.filter(start_time__isnull=False, end_time__isnull=False, status="Completed")
        duration_expression = ExpressionWrapper(F('end_time') - F('start_time'), output_field=fields.DurationField())
        jobs_with_duration = jobs_query_set.annotate(duration=duration_expression)
        total_duration = jobs_with_duration.aggregate(total_duration=Sum('duration'))['total_duration']
        job_count = jobs_with_duration.count()
        if job_count > 0 and total_duration:
            average_duration = total_duration.total_seconds() / job_count
        else:
            average_duration = timezone.timedelta(0).total_seconds()
        job_analytics = {
            'avg_wait_time': round(average_duration,2),
            'high': jobs_query_set.filter(priority=1).count(),
            'medium': jobs_query_set.filter(priority=2).count(),
            'low': jobs_query_set.filter(priority=3).count(),

        }
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request })
            response_data = {
            'job_status': job_status,
            'job_analytics': job_analytics,
            'results': serializer.data
            }
            return self.get_paginated_response(response_data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request })
        response_data = {
            'job_status': job_status,
            'job_analytics': job_analytics,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Create the job and save it
        Job.objects.all().update(execution_order=0)
        serializer.save(user=self.request.user,execution_order=1)
        app.control.purge()
        schedule_jobs()

class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            job = Job.objects.get(id=id)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Add authentication if needed
def start_schedule_jobs_view(request):
    """
    POST request to start the job scheduler.
    """
    try:
        # Call the start_schedule_jobs function
        group_schedule_job()

        # Return a success response
        return Response(
            {"status": "Scheduler started successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        # Return an error response if something goes wrong
        return Response(
            {"status": "Failed to start scheduler.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
