"""Testing function."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
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
