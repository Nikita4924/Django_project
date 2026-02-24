from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task, Profile


# ---------------- TASKS ----------------
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']


# ---------------- AUTH ----------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


# ---------------- PROFILE ----------------
class ProfileForm(forms.ModelForm):
    # Добавляем email прямо в форму профиля
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "rank",
            "bio",
            "neon_color",
            "github",
            "telegram",
            "qr_code",
            "structure_rating",
            "content_rating",
            "style_rating",
            "interactivity_rating",
            "navigation_rating",
            "functionality_rating",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Если передали пользователя — заполняем email
        if user:
            self.fields["email"].initial = user.email

        # Красивые виджеты для Matrix Criteria
        rating_choices = [(i, str(i)) for i in range(1, 6)]
        for field in [
            "structure_rating",
            "content_rating",
            "style_rating",
            "interactivity_rating",
            "navigation_rating",
            "functionality_rating",
        ]:
            self.fields[field] = forms.ChoiceField(
                choices=rating_choices,
                widget=forms.Select(attrs={"class": "form-control"}),
                initial=5
            )

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Сохраняем email в связанном User
        email = self.cleaned_data.get("email")
        if email and profile.user:
            profile.user.email = email
            if commit:
                profile.user.save()

        if commit:
            profile.save()
        return profile