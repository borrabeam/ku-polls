"""Testing function."""
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    """Model question test."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions\
            whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions\
            whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions\
            whose pub_date is within the last day."""
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_question(self):
        """is_published() return False for questions whose\
            pub_date is older than 7 days."""
        time = timezone.now() - datetime.timedelta(days=7)
        end_time = time
        past_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_recent_question(self):
        """is_published() return True for question\
             whose pub_date is not within 2 hours."""
        time = timezone.now() - \
            datetime.timedelta(hours=2)
        end_time = time + datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False for questions\
            whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_past_question(self):
        """can_vote() return False for question\
            pub_date is older than end_date."""
        time = timezone.now() - \
            datetime.timedelta(days=7)
        end_time = time
        past_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(past_question.can_vote(), False)

    def test_can_vote_with_recent_question(self):
        """can_vote() return True for question\
            pub_date is in time for vote."""
        time = timezone.now() - datetime.timedelta(hours=2)
        end_time = time + datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_with_future_question(self):
        """can_vote() return False for whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        end_time = time - datetime.timedelta(days=1)
        future_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(future_question.can_vote(), False)


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
