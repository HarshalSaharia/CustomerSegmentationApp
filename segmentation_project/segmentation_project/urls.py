"""
URL configuration for segmentation_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from customer_segmentation.views import upload_data, segment_customers  # Import your views directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_data, name='upload'),  # Directly reference the view
    path('segment/', segment_customers, name='segment'),  # Directly reference the view
    path('', RedirectView.as_view(url='upload/', permanent=False)),  # Redirect root to upload
]


