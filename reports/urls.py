from django.urls import path
from . import views

urlpatterns = [
    path('all_reports/', views.all_reports, name='all reports'),
    path('submit_report', views.submit_report, name='submit_report'),
    path('submit_review/<int:id>/', views.submit_review, name='submit_review'),
    path('download_report/<int:id>/', views.download_report, name='download_report'),
]
