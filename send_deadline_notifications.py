from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from tasks.models import Task

class Command(BaseCommand):
    help = "Send email notifications for tasks with upcoming deadlines"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        upcoming = Task.objects.filter(
            due_date__lte=now + timezone.timedelta(hours=24),
            completed=False
        )
        for task in upcoming:
            if task.user.email:
                send_mail(
                    subject=f"[Arasaka] Deadline approaching: {task.title}",
                    message=f"Task '{task.title}' is due on {task.due_date}.",
                    from_email=None,
                    recipient_list=[task.user.email],
                )