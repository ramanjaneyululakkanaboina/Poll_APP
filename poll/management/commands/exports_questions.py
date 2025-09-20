from django.core.management.base import BaseCommand
import csv
from poll.models import Question

class Command(BaseCommand):
    help = 'exports questions data into csv'
    
    def add_arguments(self, parser):
        parser.add_argument( '--filename', type=str, default='questions_csv.csv', help=' output csv file name for question')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'w', newline='', encoding='utf-8') as question_file:
            writer = csv.writer(question_file)
            writer.writerow(['Question', 'published Date', 'is_active'])

            for q in Question.objects.all():
                writer.writerow([q.question_text, q.pub_date, q.is_active])
        self.stdout.write(self.style.SUCCESS(f'Data exported to {filename}'))