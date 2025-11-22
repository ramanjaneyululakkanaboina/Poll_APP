import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from poll.models import CustomUser

class Command(BaseCommand):
    help = "Import students from a CSV file into CustomUser model"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file with student data')

    def handle(self, *args, **options):
        csv_file = Path(options['csv_file'])
        if not csv_file.is_absolute():
            csv_file = Path(settings.BASE_DIR) / "poll" / "management" / "commands" / "files" / csv_file
        
        if not csv_file.exists():
            self.stdout.write(self.style.ERROR(f"❌ File not found: {csv_file}"))
            return

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0            

            for row in reader:
                username = row['username']
                password1 = row['password1']
                password2 = row['password2']
                role = row.get('role', 'student')

                
                if password1 != password2:
                    self.stdout.write(self.style.WARNING(f"⚠ Password mismatch for {username}, skipped."))
                    continue

                
                if CustomUser.objects.filter(username=username).exists():
                    self.stdout.write(self.style.WARNING(f"⚠ User {username} already exists, skipped."))
                    continue

                
                user = CustomUser(username=username, role=role)
                user.set_password(password1) 
                user.save()

                count += 1
                self.stdout.write(self.style.SUCCESS(f" Created user {username}"))

        self.stdout.write(self.style.SUCCESS(f" Successfully imported {count} users"))
