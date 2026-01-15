"""
URL configuration for time_estimator app
"""

from django.urls import path
from .views import ProcessTimeStudyAPIView, UploadPageView

app_name = 'time_estimator'

urlpatterns = [
    path('api/process-time-study/', ProcessTimeStudyAPIView.as_view(), name='process-time-study-api'),
    path('', UploadPageView.as_view(), name='upload-page'),
]
