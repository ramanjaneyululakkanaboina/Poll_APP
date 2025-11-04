# poll/management/commands/disable_expired_surveys.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from poll.models import Survey

class Command(BaseCommand):
    help = "Automatically disables expired surveys"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired = Survey.objects.filter(end_time__lt=now, is_active=True)
        count = expired.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(f"Disabled {count} expired surveys."))


