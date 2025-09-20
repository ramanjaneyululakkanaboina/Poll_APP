from django.test import TestCase
from django.utils import timezone
from .models import Question
import  datetime
class QuestionmodelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        feature_question = Question(pub_date = time)
        self.assertIs(feature_question.pub_date <= timezone.now(), False)       