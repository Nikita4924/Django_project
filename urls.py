from django.urls import path
from .views import (
    task_list,
    add_task,
    edit_task,
    delete_task,
    task_toggle_complete,
    toggle_task_status,
    register,
    profile,
    edit_profile,   # ← добавили сюда
)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('<int:task_id>/edit/', edit_task, name='task_edit'),
    path('<int:task_id>/delete/', delete_task, name='task_delete'),
    path('<int:task_id>/toggle/', task_toggle_complete, name='task_toggle'),
    path('toggle/', toggle_task_status, name='toggle_task_status'),

    # регистрация


    # профиль
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]