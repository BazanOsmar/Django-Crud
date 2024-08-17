from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import taskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#funcion que imprime "hello world" en la pagina
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == 'GET':
        return render(request, "singup.html",{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrando al usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Task')
            except:
                return render(request, 'singup.html',{
                    "form": UserCreationForm,
                    "Error": "User name already exist" 
                })
        else:
            return render(request, "singup.html",{
                "form": UserCreationForm,
                "Error": "Password do not match" 
            })
            
            
@login_required       
def task(request):
    tareas = Task.objects.filter(user = request.user, dateCompleted__isnull = True)
    return render(request, "task.html",{
        'tasks': tareas
    })


def signOut(request):
    logout(request)
    return redirect("Home")

def signIn(request):
    if request.method == 'GET':
        return render(request, 'Signin.html',{
            "form": AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'Signin.html',{
                "form": AuthenticationForm,
                "Error": "Algo hiciste mal"
            })
        else:
            login(request, user)
            return redirect("Task")
        
@login_required    
def createTask(request):
    if request.method == 'GET':
        return render(request, "create_task.html",{
            "Form": taskForm
        })
    else:
        form = taskForm(request.POST)
        newTask = form.save(commit=False)
        newTask.user = request.user
        newTask.save()
        redirect('Task')
        #newTask = form.save(commit=False)
        print(request.POST)
        return redirect("Task")

@login_required    
def taskDetail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = taskForm(instance=task)
        #task = Task.objects.get(pk=task_id) <- forma no adecuada de recuperar un objeto
        return render(request, "task_detail.html",{
            'task': task,
            'form': form
        })
    else:
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        form = taskForm(request.POST, instance=task)
        form.save()
        return redirect('Task')

@login_required    
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('Task')


@login_required    
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('Task')


@login_required    
def completedTasks(request):
    tareas = Task.objects.filter(user = request.user, dateCompleted__isnull = False).order_by('-dateCompleted')
    return render(request, "task.html",{
        'tasks': tareas
    })