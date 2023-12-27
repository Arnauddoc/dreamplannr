from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("home", views.index, name="home"),
    path("privacy", views.privacy, name="privacy"),
    path("terms", views.terms, name="terms"),
    path("", views.index, name="home"),
    path("agenda", views.agenda, name="agenda"),
    path("todos", views.todos, name="todos"),
    path("login/", views.register_and_login, name="login"),
    path("userLogin", views.userLogin, name="userLogin"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("userRegister", views.userRegister, name="userRegister"),
    path("toDo", views.toDo, name="toDo"),
    path("task", views.get_task, name="task"),
    path("edit_task/<int:task_id>", views.edit_task, name="edit_task"),
    path("delete_task/<int:task_id>", views.delete_task, name="delete_task"),
    path('get_events/', views.get_events, name='get_events'),
    path('todo/delete/<int:todo_id>', views.delete_todo, name='delete_todo'),
    path('todo/edit/<int:todo_id>', views.edit_todo, name='edit_todo')
]

