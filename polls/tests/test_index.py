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

class QuestionIndexViewTests(TestCase):
    """Index view questions test."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past\
            are displayed on the index page."""
        create_question(question_text="Past question.", days=-30, end_date=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future\
            aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30, end_date=40)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist,\
            only past questions are displayed."""
        create_question(question_text="Past question.", days=-30, end_date=-10)
        create_question(question_text="Future question.", days=30, end_date=40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30, end_date=-10)
        create_question(question_text="Past question 2.", days=-5, end_date=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
