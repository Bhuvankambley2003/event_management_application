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
    path('attendees/remove/<int:attendee_id>/', views.remove_attendee, name='remove_attendee'),
    path('tasks/', views.task_list, name='task_list'),
    path('remove_task/<int:task_id>/', views.remove_task, name='remove_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('events/remove/<int:event_id>/', views.remove_event, name='remove_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    
    # Progress Tracker URL
    path('progress_tracker/', views.progress_tracker, name='progress_tracker'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]