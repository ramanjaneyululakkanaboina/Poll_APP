from django.core.management.base import BaseCommand
import csv
import os
from django.conf import settings
from poll.models import Survey, Choice


class Command(BaseCommand):
    help = "Export each survey along with its questions and choices to separate CSV files."

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            type=str,
            default='survey_exports',
            help='Output folder name (default: survey_exports inside commands/files)'
        )

    def handle(self, *args, **options):
        folder_name = options['folder']

        # Default base folder inside commands directory
        base_folder = os.path.join(settings.BASE_DIR, "poll", "management", "commands", "files", folder_name)
        os.makedirs(base_folder, exist_ok=True)

        self.stdout.write(self.style.WARNING("Exporting all surveys to individual CSV files..."))

        surveys = Survey.objects.prefetch_related("questions__choice_set", "questions__category").all()
        if not surveys.exists():
            self.stdout.write(self.style.ERROR("No surveys found to export."))
            return

        for survey in surveys:
            # 🔹 Create a safe file name (avoid spaces/special chars)
            safe_name = survey.name.replace(" ", "_").replace("/", "_")
            output_file = os.path.join(base_folder, f"{safe_name}_survey.csv")

            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = [
                    "survey_id",
                    "survey_name",
                    "description",
                    "start_time",
                    "end_time",
                    "question_id",
                    "question_text",
                    "category",
                    "choice_text",
                    "votes",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for question in survey.questions.all():
                    choices = question.choice_set.all()
                    if choices.exists():
                        for choice in choices:
                            writer.writerow({
                                "survey_id": survey.id,
                                "survey_name": survey.name,
                                "description": survey.description,
                                "start_time": survey.start_time,
                                "end_time": survey.end_time,
                                "question_id": question.id,
                                "question_text": question.question_text,
                                "category": question.category.name if question.category else "",
                                "choice_text": choice.choice_text,
                                "votes": choice.votes,
                            })
                    else:
                        writer.writerow({
                            "survey_id": survey.id,
                            "survey_name": survey.name,
                            "description": survey.description,
                            "start_time": survey.start_time,
                            "end_time": survey.end_time,
                            "question_id": question.id,
                            "question_text": question.question_text,
                            "category": question.category.name if question.category else "",
                            "choice_text": "",
                            "votes": 0,
                        })

            self.stdout.write(self.style.SUCCESS(f"✅ Exported: {output_file}"))

        self.stdout.write(self.style.SUCCESS(f"\nAll surveys exported successfully to folder: {base_folder}"))
