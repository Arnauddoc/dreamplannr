from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm, ToDoItemForm, taskForm
from django.contrib.auth import login, authenticate
from .models import todo, task
from django.http import JsonResponse
import traceback
from datetime import timedelta

def agenda(request):
    if request.user.is_authenticated:
        all_events = task.objects.filter(user=request.user)
        return render(request, "customerInterface/agenda.html", {"form": taskForm(), "all_events": all_events})
    else:
        # Handle the case when the user is not authenticated
        return render(request, "customerInterface/agenda.html")

def get_events(request):
    try:
        events = task.objects.filter(user=request.user).values('title', 'start_date', 'end_date', 'start_time', 'end_time', 'repeat','id','description','all_day')
        list_events = []

        for event in events:
            event_id = event['id']

            repeat = event['repeat']

            if repeat == "daily":
                start_date = event['start_date']
                stop_date = event['end_date'] + timedelta(days=365)

                current_date = start_date
                while current_date < stop_date:
                    repeated_event = {
                        'description': event['description'],
                        'all_day': event['all_day'],
                        'id': event_id,
                        'title': event['title'],
                        'start_date': current_date,
                        'end_date': current_date,
                        'start_time': event['start_time'],
                        'end_time': event['end_time'],
                        'repeat': event['repeat']
                    }
                    list_events.append(repeated_event)
                    current_date += timedelta(days=1)

            elif repeat == "weekly":
                start_date = event['start_date']
                stop_date = event['end_date'] + timedelta(days=365)

                current_date = start_date
                while current_date < stop_date:
                    weekly_event = {
                        'description': event['description'],
                        'all_day': event['all_day'],
                        'id': event_id,
                        'title': event['title'],
                        'start_date': current_date,
                        'end_date': current_date,
                        'start_time': event['start_time'],
                        'end_time': event['end_time'],
                        'repeat': event['repeat']
                    }
                    list_events.append(weekly_event)
                    current_date += timedelta(weeks=1)

            else:
                # For non-repeating events, simply add the original event
                list_events.append(event)                

        return JsonResponse(list_events, safe=False)

    except Exception as e:
        traceback.print_exc()  # Print the exception details to the console
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def get_task(request):
    errors = ""
    if request.method == "POST":
        form = taskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data.get('description', None)
            if not description:
                form.cleaned_data['description'] = None
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            repeat = form.cleaned_data['repeat']

            all_day = form.cleaned_data.get('all_day',None)
            if all_day:
                start_time = None
                end_time = None
            else:
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
            
            new_task = task(user=request.user, title=title, description= description, start_date=start_date, 
                            end_date=end_date, repeat=repeat, all_day=all_day, start_time=start_time, end_time=end_time)
            new_task.save()

            return redirect('agenda')
        else:
            errors = True
    else:
        form = taskForm()

    all_events = task.objects.filter(user=request.user)
    return render(request, "customerInterface/agenda.html", {"form": form, "errors": errors,"all_events": all_events})

def edit_task(request, task_id):
    task_item = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = taskForm(request.POST, instance=task_item)
        if form.is_valid():
            form.save()
            return redirect('agenda')  # Redirect to the todo list page after editing
    else:
        form = ToDoItemForm(instance=task_item)
    all_events = task.objects.filter(user=request.user)
    return render(request, "customerInterface/agenda.html", {"form": taskForm(), "all_events": all_events})

def delete_task(request, task_id):
    task_item = get_object_or_404(task, pk=task_id, user=request.user)
    task_item.delete()
    all_events = task.objects.filter(user=request.user)
    return redirect('agenda')

def todos(request):
    if request.user.is_authenticated:
        todos = todo.objects.filter(user=request.user).order_by("end_date")
        return render(request, "customerInterface/todos.html", {"todo": todos, "form": ToDoItemForm()})
    else:
        # Handle the case when the user is not authenticated
        return render(request, "customerInterface/todos.html", {"todos": None})

def delete_todo(request, todo_id):
    todo_item = get_object_or_404(todo, pk=todo_id, user=request.user)
    todo_item.delete()
    todos = todo.objects.filter(user=request.user).order_by("end_date")
    return redirect('todos')

def edit_todo(request, todo_id):
    todo_item = get_object_or_404(todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        form = ToDoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            return redirect('todos')  # Redirect to the todo list page after editing
    else:
        form = ToDoItemForm(instance=todo_item)
    todos = todo.objects.filter(user=request.user).order_by("end_date")
    return redirect('todos')

def toDo(request):
    errors = ""
    todos = todo.objects.filter(user=request.user).order_by("end_date")
    if request.method == "POST":
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content', None)
            if not content:
                form.cleaned_data['content'] = None
            date = form.cleaned_data['end_date']

            new_todo = todo(user=request.user, title=title, content=content, end_date=date)
            new_todo.save()

            return redirect('todos')
        else:
            errors = True
    else:
        form = ToDoItemForm()
    return render(request, "customerInterface/todos.html",{"form": form, "error": errors, "todo": todos})
 
def register_and_login(request):
    return render(request, 'customerInterface/login.html', {'form1': LoginForm(), "form": RegisterForm()})

def userLogin(request):
    error = ""
    next = request.GET.get('next', '')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("home")
            else:
                error = 'Invalid username or password'
        else:
            error = 'Invalid form data'
    else:
        form = LoginForm()
    return render(request, 'customerInterface/login.html', {'form1': LoginForm(), "form": RegisterForm(),'error':error})

def userRegister(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home") 
        else:
            registration_errors = True
    else:
        form = RegisterForm()
    return render(request, "customerInterface/login.html",{"form1": LoginForm(), "form": form, "registration_errors": registration_errors})

def index(request):
    return render(request, "customerInterface/index.html")

def privacy(request):
    return render(request, "customerInterface/privacy.html")

def terms(request):
    return render(request, "customerInterface/terms.html")

def error_404_view(request, exception):
    return render(request, 'customerInterface/404.html')