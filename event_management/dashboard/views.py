from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event, Attendee, Task
from .serializers import EventSerializer, AttendeeSerializer, TaskSerializer
from .forms import EventForm, AttendeeForm, TaskForm

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def event_list(request):
    events = Event.objects.all()  # Fetch all events
    if request.method == 'POST' and (request.user.is_staff or request.user.is_superuser):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'dashboard/event_list.html', {'events': events, 'form': form})

@user_passes_test(is_admin)
@login_required
def remove_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('event_list')

@login_required
def attendee_list(request):
    attendees = Attendee.objects.all()
    if request.method == 'POST' and (request.user.is_staff or request.user.is_superuser):
        form = AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendee_list')
    else:
        form = AttendeeForm()
    return render(request, 'dashboard/attendee_list.html', {'attendees': attendees, 'form': form})

@user_passes_test(is_admin)
@login_required
def remove_attendee(request, attendee_id):
    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee.delete()
    return redirect('attendee_list')

@login_required
def task_list(request):
    events = Event.objects.all()
    tasks = Task.objects.all()
    if request.method == 'POST' and (request.user.is_staff or request.user.is_superuser):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'dashboard/task_list.html', {'events': events, 'tasks': tasks, 'form': form})

from django.http import JsonResponse
from django.http import JsonResponse

@login_required
def progress_tracker(request):
    events = Event.objects.all()
    event_progress = []

    for event in events:
        tasks = Task.objects.filter(event=event)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='completed').count()
        progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        event_progress.append({
            'event': event.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percentage': progress_percentage
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'event_progress': event_progress})

    return render(request, 'dashboard/progress_tracker.html', {
        'event_progress': event_progress
    })

@user_passes_test(is_admin)
@login_required
def remove_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

@user_passes_test(is_admin)
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/edit_event.html', {'form': form, 'event': event})

@user_passes_test(is_admin)
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/edit_task.html', {'form': form, 'task': task})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('event_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('event_list')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    
    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_attendee(self, request, pk=None):
        event = self.get_object()
        attendee_id = request.data.get('attendee_id')
        attendee = get_object_or_404(Attendee, id=attendee_id)
        event.attendees.add(attendee)
        return Response({'status': 'attendee added'})

    @action(detail=True, methods=['post'])
    def remove_attendee(self, request, pk=None):
        event = self.get_object()
        attendee_id = request.data.get('attendee_id')
        attendee = get_object_or_404(Attendee, id=attendee_id)
        event.attendees.remove(attendee)
        return Response({'status': 'attendee removed'})

class AttendeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer

# class TaskViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TaskSerializer

#     def get_queryset(self):
#         return Task.objects.filter(event__created_by=self.request.user)

#     @action(detail=True, methods=['patch'])
#     def update_status(self, request, pk=None):
#         task = self.get_object()
#         status = request.data.get('status')
#         if status in dict(Task.STATUS_CHOICES):
#             task.status = status
#             task.save()
#             return Response({'status': 'task status updated'})
#         return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(event__created_by=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        status = request.data.get('status')
        if status in dict(Task.STATUS_CHOICES):
            task.status = status
            task.save()

            # Fetch updated progress data
            events = Event.objects.all()
            event_progress = []
            for event in events:
                tasks = Task.objects.filter(event=event)
                total_tasks = tasks.count()
                completed_tasks = tasks.filter(status='completed').count()
                progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
                event_progress.append({
                    'event': event.name,
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'progress_percentage': progress_percentage
                })

            return Response({'status': 'task status updated', 'event_progress': event_progress})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)