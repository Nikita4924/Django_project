from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, CustomUserCreationForm, ProfileForm
from .models import Task

# ---------------- TASKS ----------------

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'edit': True})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def task_toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def toggle_task_status(request):
    return redirect('task_list')

# ---------------- AUTH & PROFILE ----------------

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('task_list')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'tasks/registration/register.html', {
        'form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    profile = request.user.profile
    criteria = [
        ("STRUCTURE", profile.structure_rating),
        ("CONTENT", profile.content_rating),
        ("STYLE", profile.style_rating),
        ("INTERACTIVITY", profile.interactivity_rating),
        ("NAVIGATION", profile.navigation_rating),
        ("FUNCTIONALITY", profile.functionality_rating),
    ]
    mode = request.GET.get("mode", "radial")  # stars / bars / radial
    return render(request, "tasks/profile.html", {
        "profile": profile,
        "criteria": criteria,
        "mode": mode
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'tasks/profile_edit.html', {'form': form})