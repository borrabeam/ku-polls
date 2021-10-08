"""Manage models question and choice."""
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Class for setting question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField("ending date")

    def __str__(self):
        """Return a string representation of question."""
        return self.question_text

    def was_published_recently(self):
        """Check is the polls was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check the question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check if the poll can vote or not."""
        now = timezone.now()
        return now <= self.end_date and self.is_published()

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Class for setting choice."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return a string representation of choice."""
        return self.choice_text
