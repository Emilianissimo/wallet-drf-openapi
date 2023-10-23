from django.urls import path, include

urlpatterns = [
    path('v1/', include('application.v1.urls')),    
]
