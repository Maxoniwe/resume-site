from django.urls import path

from .views import download_resume_pdf, home

app_name = 'resume'

urlpatterns = [
    path('', home, name='home'),
    path('download/', download_resume_pdf, name='download_pdf'),
]
