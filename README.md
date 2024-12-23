# Event Management Application

## Overview
This project is a Django-based event management system that provides the following features:
- Event creation and management.
- Attendee registration and management.
- Task assignment and tracking for events.
- RESTful API endpoints for integration.
- Responsive and dynamic UI templates.

---

## Models

### 1. Attendee Model
- Stores attendee details like:
  - Name
  - Email (unique to avoid duplication)
  - Phone number

### 2. Event Model
- Contains fields for:
  - Name
  - Description
  - Location
  - Date
- Includes:
  - Many-to-Many relationship with the `Attendee` model.
  - `ForeignKey` to the `User` model for event creator tracking.
  - Timestamps for creation and updates.

### 3. Task Model
- Includes fields for:
  - Name
  - Deadline
  - Status (choices: "Pending" or "Completed")
- Links to:
  - `Event` model (via `ForeignKey`)
  - `Attendee` model (via `ForeignKey`)
- Tracks creation and update timestamps.

### Implementation
1. Add `'dashboard'` to `INSTALLED_APPS` in `settings.py`.
2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## API Features

### Serializers
1. **AttendeeSerializer**: Handles serialization for attendee data.
2. **TaskSerializer**: Includes the assigned attendee's name.
3. **EventSerializer**: Serializes tasks and attendees with nested structures.

### ViewSets
1. **EventViewSet**:
   - CRUD operations for events.
   - Custom actions to add/remove attendees.
   - Filters events by the logged-in user.

2. **AttendeeViewSet**:
   - CRUD operations for attendees.

3. **TaskViewSet**:
   - CRUD operations for tasks.
   - Custom action to update task statuses.
   - Filters tasks based on the event creator.

### Setup Instructions
1. Install Django REST framework:
   ```bash
   pip install djangorestframework
   ```
2. Add `'rest_framework'` to `INSTALLED_APPS` in `settings.py`.

---

## URL Configuration

### API Endpoints
1. **Event API**:
   - List all events: `GET /api/events/`
   - Create an event: `POST /api/events/`
   - Retrieve event: `GET /api/events/{id}/`
   - Update event: `PUT /api/events/{id}/`
   - Delete event: `DELETE /api/events/{id}/`
   - Add attendee: `POST /api/events/{id}/add_attendee/`
   - Remove attendee: `POST /api/events/{id}/remove_attendee/`

2. **Attendee API**:
   - List all attendees: `GET /api/attendees/`
   - Create attendee: `POST /api/attendees/`
   - Retrieve attendee: `GET /api/attendees/{id}/`
   - Update attendee: `PUT /api/attendees/{id}/`
   - Delete attendee: `DELETE /api/attendees/{id}/`

3. **Task API**:
   - List all tasks: `GET /api/tasks/`
   - Create task: `POST /api/tasks/`
   - Retrieve task: `GET /api/tasks/{id}/`
   - Update task: `PUT /api/tasks/{id}/`
   - Delete task: `DELETE /api/tasks/{id}/`
   - Update status: `PATCH /api/tasks/{id}/update_status/`

### Testing Endpoints
You can test the endpoints using:
- Django's browsable API interface.
- Postman.
- curl commands, e.g.:
   ```bash
   # List all events
   curl -H "Authorization: Bearer your_token" http://localhost:8000/api/events/

   # Create a new event
   curl -X POST \
     -H "Authorization: Bearer your_token" \
     -H "Content-Type: application/json" \
     -d '{"name":"Team Meeting","description":"Monthly team meeting","location":"Conference Room","date":"2024-12-25T10:00:00Z"}' \
     http://localhost:8000/api/events/
   ```

---

## Templates

### 1. Base Template (`base.html`)
- Features:
  - Responsive navigation bar with authentication indicators.
  - Styling using Tailwind CSS.
  - Dynamic AJAX requests using Axios.

### 2. Event List Template (`event_list.html`)
- Features:
  - Displays a list of all events.
  - Add, edit, and delete functionality.
  - Modal form for creating/editing events.
  - Dynamic rendering with JavaScript.

### 3. Attendee Template (`attendee_list.html`)
- Features:
  - List all attendees.
  - Add, edit, and delete attendees.
  - Modal form for attendee management.

### 4. Task Template (`task_list.html`)
- Features:
  - List all tasks.
  - Add, update status, and delete tasks.
  - Modal form for task creation with event and attendee selection.
  - Status toggle functionality.

### Implementation Steps
1. Create a `templates` directory within the `dashboard` app:
   ```bash
   mkdir -p dashboard/templates/dashboard
   ```
2. Place templates in their respective locations:
   - `base.html` → `templates/base.html`
   - `event_list.html` → `templates/dashboard/event_list.html`
   - `attendee_list.html` → `templates/dashboard/attendee_list.html`
   - `task_list.html` → `templates/dashboard/task_list.html`

3. Update `settings.py` to configure the template directory:
   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / 'templates'],
           'APP_DIRS': True,
           ...
       },
   ]
   ```

4. Add views in `views.py`:
   ```python
   from django.shortcuts import render
   from django.contrib.auth.decorators import login_required

   @login_required
   def attendee_list(request):
       return render(request, 'dashboard/attendee_list.html')

   @login_required
   def task_list(request):
       return render(request, 'dashboard/task_list.html')
   ```

---

## Authentication & User Management

### Authentication Views
- Includes login and logout functionality.

### Configuration
1. Update `settings.py`:
   ```python
   LOGIN_URL = 'login'
   LOGIN_REDIRECT_URL = 'event_list'
   LOGOUT_REDIRECT_URL = 'login'
   ```

2. Create a superuser for testing:
   ```bash
   python manage.py createsuperuser
   ```

3. Apply migrations and start the server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

---

## Summary
This event management application provides:
- Comprehensive user authentication and authorization.
- Full-featured management of events, attendees, and tasks.
- A RESTful API for external integration.
- A responsive, dynamic UI for easy navigation and interaction.

Feel free to reach out for additional support or to suggest improvements!
