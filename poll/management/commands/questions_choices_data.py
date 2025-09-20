import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from poll.models import Question, Choice


class Command(BaseCommand):
    help = "Import questions and choices from CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--questions",
            type=str,
            default=os.path.join(settings.BASE_DIR, "questions.csv"),
            help="Path to questions CSV file",
        )
        parser.add_argument(
            "--choices",
            type=str,
            default=os.path.join(settings.BASE_DIR, "choices.csv"),
            help="Path to choices CSV file",
        )

    def handle(self, *args, **options):
        questions_file = options["questions"]
        choices_file = options["choices"]

        self.stdout.write(self.style.WARNING("Importing Questions..."))
        question_map = {}  

        with open(questions_file, newline="", encoding="utf-8") as qfile:
            reader = csv.DictReader(qfile)
            for row in reader:
                question = Question.objects.create(
                    question_text=row["question_text"],
                    pub_date=row["pub_date"],
                    is_active=row.get("is_active", "True").lower() in ["true", "1"],
                )
                question_map[row["id"]] = question
        self.stdout.write(self.style.SUCCESS(f"Imported {len(question_map)} questions."))

        
        self.stdout.write(self.style.WARNING("Importing Choices..."))
        choice_count = 0
        with open(choices_file, newline="", encoding="utf-8") as cfile:
            reader = csv.DictReader(cfile)
            for row in reader:
                q_id = row["question_id"]
                if q_id in question_map:
                    Choice.objects.create(
                        question=question_map[q_id],
                        choice_text=row["choice_text"],
                        votes=int(row.get("votes", 0)),
                    )
                    choice_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {choice_count} choices."))
