from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tasks import views as task_views
from django.contrib.auth import views as auth_views
from tasks.forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # стандартные auth пути

    # кастомный login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),

    # кастомная регистрация
    path('register/', task_views.register, name='register'),

    # кастомный logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# 🔧 Раздача медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)