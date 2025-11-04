from django.core.management.base import BaseCommand
from poll.models import Category

class Command(BaseCommand):
    help = "Create default question categories"

    DEFAULT_CATEGORIES = [
        "Technology",
        "Education",
        "Politics",
        "Sports"
    ]

    def handle(self, *args, **kwargs):
        created_count = 0

        for name in self.DEFAULT_CATEGORIES:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                created_count += 1

        if created_count:
            self.stdout.write(self.style.SUCCESS(f"{created_count} categories created successfully!"))
        else:
            self.stdout.write(self.style.WARNING("All default categories already exist."))
