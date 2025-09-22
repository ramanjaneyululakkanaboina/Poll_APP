import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from poll.models import Question, Choice


class Command(BaseCommand):
    help = "Import questions and choices from a single CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=os.path.join(settings.BASE_DIR, "question_choices.csv"),
            help="Path to CSV file containing questions and choices",
        )

    def handle(self, *args, **options):
        csv_file = options["file"]

        self.stdout.write(self.style.WARNING("Importing Questions and Choices..."))

        question_map = {}  
        choice_count = 0
        question_count = 0

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_text = row["question_text"].strip()
                pub_date = row["pub_date"]
                is_active = row.get("is_active", "True").lower() in ["true", "1"]

                
                if q_text not in question_map:
                    question = Question.objects.create(
                        question_text=q_text,
                        pub_date=pub_date,
                        is_active=is_active,
                    )
                    question_map[q_text] = question
                    question_count += 1

               
                Choice.objects.create(
                    question=question_map[q_text],
                    choice_text=row["choice_text"].strip(),
                    votes=int(row.get("votes", 0)),
                )
                choice_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {question_count} questions."))
        self.stdout.write(self.style.SUCCESS(f"Imported {choice_count} choices."))
