from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Event, Attendee, Task
from .serializers import EventSerializer, AttendeeSerializer, TaskSerializer


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

@login_required
def event_list(request):
    return render(request, 'dashboard/event_list.html')

@login_required
def attendee_list(request):
    return render(request, 'dashboard/attendee_list.html')

@login_required
def task_list(request):
    return render(request, 'dashboard/task_list.html')

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


@login_required
def attendee_list(request):
    return render(request, 'dashboard/attendee_list.html')

@login_required
def task_list(request):
    return render(request, 'dashboard/task_list.html')



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
            return Response({'status': 'task status updated'})
        return Response({'error': 'Invalid status'}, 
                      status=status.HTTP_400_BAD_REQUEST)