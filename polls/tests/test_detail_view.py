"""Testing function."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse




def create_question(question_text, days, end_date):
    """Create a question with the given `question_text` and\
        published the given number of `days` offset to now\
        (negative for questions published in the past,\
        positive for questions that have yet to be published)."""
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = timezone.now() + datetime.timedelta(days=days, hours=5)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date = end_time)


class QuestionDetailViewTests(TestCase):
    """Detail view questions test."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future.

        Returns:
                a 404 not found.
        """
        future_question = \
            create_question(question_text='Future question.', days=5, end_date=7)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date\
            in the past displays the question's text."""
        past_question = \
            create_question(question_text='Past Question.', days=-5 ,end_date=-1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
