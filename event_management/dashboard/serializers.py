from rest_framework import serializers
from .models import Event, Attendee, Task

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email', 'phone', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'status', 
                 'event', 'assigned_to', 'assigned_to_name', 
                 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    attendees = AttendeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date', 
                 'attendees', 'tasks', 'created_by', 'created_at', 
                 'updated_at']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)