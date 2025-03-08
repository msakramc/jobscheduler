from django.urls import path
from scheduler import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('api/v1/getjobs/', views.JobList.as_view(), name='get_jobs'),
    path('api/v1/createjob/', views.JobCreateView.as_view(), name='create_job'),
    path('api/v1/runjob/', views.start_schedule_jobs_view, name='run_job'),

]
