from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('testing', views.HelloViewSet, basename='testing')
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('index/', views.HelloAPIView.as_view()),
    
    path('login/', views.UserLoginAPIView.as_view()),
    path('register/', views.registration_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('getprofile/', views.UserProfileDetailView.as_view()),
    
    
    
    # Using Viewsets url instead.
    path('', include(router.urls))
]
