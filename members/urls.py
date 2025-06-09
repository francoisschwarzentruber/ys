from django.urls import path
from . import views

urlpatterns = [
    path('submissions/', views.submissions, name='submissions'),
    path('download_submission/<int:id>/', views.download_submission, name='download_submission'),
]
