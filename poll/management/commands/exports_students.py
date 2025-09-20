from django.core.management.base import BaseCommand
import csv
from poll.models import CustomUser

class Command(BaseCommand):
    help = "Exporting students data into csv file"
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, default='student_csv.csv', help='output csv file name(default:student_csv file)')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'w', newline='', encoding='utf-8') as student_file:
            stdunt_dat = csv.writer(student_file)
            stdunt_dat.writerow(["username","role"])

            for s in CustomUser.objects.all():
                stdunt_dat.writerow([s.username, s.role ] )
        self.stdout.write(self.style.SUCCESS(f'Data Exported to {filename}'))