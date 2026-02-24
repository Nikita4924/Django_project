from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class Task(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('overdue', 'Overdue'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now() and not self.completed

    @property
    def is_urgent(self):
        return self.due_date and (self.due_date - timezone.now()).days <= 1 and not self.completed

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    neon_color = models.CharField(max_length=7, default="#ff0033")  # HEX цвет

    # Дополнительные поля для карточки
    github = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr/', blank=True, null=True)

    # Оценочные критерии (Matrix Criteria)
    structure_rating = models.IntegerField(default=5)
    content_rating = models.IntegerField(default=5)
    style_rating = models.IntegerField(default=5)
    interactivity_rating = models.IntegerField(default=5)
    navigation_rating = models.IntegerField(default=5)
    functionality_rating = models.IntegerField(default=5)

    def __str__(self):
        return self.user.username


# Сигналы для автоматического создания профиля
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()