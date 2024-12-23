from django import forms
from .models import Event, Attendee, Task

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date']

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'email', 'phone']

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'event', 'assigned_to', 'deadline', 'status']