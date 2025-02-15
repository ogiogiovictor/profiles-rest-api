from django.urls import path
from profiles_api import views

urlpatterns = [
    path('index/', views.HelloAPIView.as_view()),
]
