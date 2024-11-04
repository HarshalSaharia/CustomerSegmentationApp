from django.urls import path
from .views import upload_data, segment_customers  # Import your views

urlpatterns = [
    path('upload/', upload_data, name='upload'),  # URL for uploading data
    path('segment/', segment_customers, name='segment'),  # URL for customer segmentation
]
