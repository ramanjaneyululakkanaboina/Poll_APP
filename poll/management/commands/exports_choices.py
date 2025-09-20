from django.core.management.base import BaseCommand
import csv
from poll.models import Choice, Question

class Command(BaseCommand):
    help = 'Exporting choices data into csv file'

    def add_arguments(self, parser):
        parser.add_argument( '--filename', type=str, default='choices_csv.csv', help='output file name(default : choices_csv.csv file)')
    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'w', newline='', encoding='utf-8') as choices_file:
            writer = csv.writer(choices_file)
            writer.writerow(['Question', 'Choices', 'Votes'])

            for c in Choice.objects.all():
                writer.writerow([c.question, c.choice_text, c.votes])

            # for q in Question.objects.all():
            #     choice_text = [c.choice_text for c in q.choice_set.all()]
            #     votes = [v.votes for v in q.choice_set.all()]
            #     writer.writerow([q.question_text, choice_text, votes])

        self.stdout.write(self.style.SUCCESS(f'Data Exported to {filename}'))