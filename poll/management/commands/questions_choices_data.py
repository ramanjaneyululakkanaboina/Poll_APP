import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from poll.models import Question, Choice,Category


class Command(BaseCommand):
    help = "Import questions and choices from a single CSV file (skips duplicates)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=os.path.join(settings.BASE_DIR, "question_choices.csv"),
            help="Path to CSV file containing questions and choices",
        )

    def handle(self, *args, **options):
        file_arg = options["file"]

        # If only filename given (no folder), place in default import folder
        if not os.path.isabs(file_arg) and not os.path.dirname(file_arg):
            csv_file = os.path.join(settings.BASE_DIR, "poll", "management", "commands", "files", file_arg)
        else:
            csv_file = file_arg

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {csv_file}"))
            return

        self.stdout.write(self.style.WARNING("📥 Importing Questions and Choices (skipping duplicates)..."))

        question_count = 0
        choice_count = 0
        skipped_questions = 0
        skipped_choices = 0

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_text = row["question_text"].strip()
                pub_date = row["pub_date"]
                is_active = row.get("is_active", "True").lower() in ["true", "1"]
                category_name = row.get("category", "").strip()

                category = None
                if category_name:
                    category, _ = Category.objects.get_or_create(name=category_name)

                # ✅ Check if question already exists
                existing_q = Question.objects.filter(question_text=q_text).first()
                if existing_q:
                     question = existing_q
                     skipped_questions += 1
                else:
                     question = Question.objects.create(
                          question_text=q_text,
                          pub_date=pub_date,
                          is_active=is_active,
                          category=category

                                  )
                     question_count += 1


                # ✅ Check if this choice already exists for that question
                choice_text = row["choice_text"].strip()
                if choice_text:  # ignore blank choices
                    choice, c_created = Choice.objects.get_or_create(
                        question=question,
                        choice_text=choice_text,
                        defaults={"votes": int(row.get("votes", 0))},
                    )

                    if c_created:
                        choice_count += 1
                    else:
                        skipped_choices += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {question_count} new questions, {choice_count} new choices."))
        self.stdout.write(self.style.WARNING(f"⏩ Skipped {skipped_questions} existing questions, {skipped_choices} duplicate choices."))
        self.stdout.write(self.style.SUCCESS(f"📂 Import completed from {csv_file}"))
