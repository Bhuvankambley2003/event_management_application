from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import EventViewSet, AttendeeViewSet, TaskViewSet

# DRF router
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'attendees', AttendeeViewSet, basename='attendee')
router.register(r'tasks', TaskViewSet, basename='task')

# URL patterns
urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
   # Template URLs
    path('', views.event_list, name='event_list'),
    path('attendees/', views.attendee_list, name='attendee_list'),
    path('tasks/', views.task_list, name='task_list'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]