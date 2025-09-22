import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from poll.models import Question, Choice


class Command(BaseCommand):
    help = "Export questions and choices into a single CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default=os.path.join(settings.BASE_DIR, "exports_question_choices_data.csv"),
            help="Path to export CSV file",
        )

    def handle(self, *args, **options):
        output_file = options["output"]

        self.stdout.write(self.style.WARNING("Exporting Questions and Choices..."))

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["question_id", "question_text", "pub_date", "is_active", "choice_text", "votes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for question in Question.objects.all():
                choices = Choice.objects.filter(question=question)
                if choices.exists():
                    for choice in choices:
                        writer.writerow({
                            "question_id": question.id,
                            "question_text": question.question_text,
                            "pub_date": question.pub_date,
                            "is_active": question.is_active,
                            "choice_text": choice.choice_text,
                            "votes": choice.votes,
                        })
                else:
                   
                    writer.writerow({
                        "question_id": question.id,
                        "question_text": question.question_text,
                        "pub_date": question.pub_date,
                        "is_active": question.is_active,
                        "choice_text": "",
                        "votes": 0,
                    })

        self.stdout.write(self.style.SUCCESS(f"Data exported successfully to {output_file}"))
