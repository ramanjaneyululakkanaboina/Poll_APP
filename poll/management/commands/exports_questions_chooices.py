import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from poll.models import Question, Choice


class Command(BaseCommand):
    help = "Export questions and choices (with categories) into a single CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="exports_question_choices_data.csv",
            help="Filename or path for the export CSV file",
        )

    def handle(self, *args, **options):
        output_arg = options["output"]

        # Default folder where we store CSVs
        commands_folder = os.path.join(settings.BASE_DIR, "poll", "management", "commands","files")

        # If user gives only filename (no folder), save inside commands folder
        if not os.path.dirname(output_arg):
            output_file = os.path.join(commands_folder, output_arg)
        else:
            output_file = output_arg

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        self.stdout.write(self.style.WARNING(f"Exporting Questions & Choices to: {output_file}"))

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "question_id",
                "question_text",
                "category_name",
                "pub_date",
                "is_active",
                "choice_text",
                "votes",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for question in Question.objects.select_related("category").all():
                choices = Choice.objects.filter(question=question)
                category_name = question.category.name if question.category else "Uncategorized"

                if choices.exists():
                    for choice in choices:
                        writer.writerow({
                            "question_id": question.id,
                            "question_text": question.question_text,
                            "category_name": category_name,
                            "pub_date": question.pub_date,
                            "is_active": question.is_active,
                            "choice_text": choice.choice_text,
                            "votes": choice.votes,
                        })
                else:
                    writer.writerow({
                        "question_id": question.id,
                        "question_text": question.question_text,
                        "category_name": category_name,
                        "pub_date": question.pub_date,
                        "is_active": question.is_active,
                        "choice_text": "",
                        "votes": 0,
                    })

        self.stdout.write(self.style.SUCCESS(f"✅ Export complete: {output_file}"))
