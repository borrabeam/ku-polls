"""View for set and manage page."""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    """For setting index view page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """For setting detail view page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """For setting results view page."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """For choice the polls."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        vote = get_vote_for_user(question, user)
        if not vote:
            vote = Vote.objects.create(choice=selected_choice, voter=user)
        else:
            vote.choice = selected_choice
        vote.save()
        logger.info(f"{user} voted in {question}.")

        return HttpResponseRedirect(reverse('polls:results',
                                        args=(question.id,)))


def vote_poll(request, question_id):
    """Vote for the polls."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "You are not allowed to vote this poll")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})


def get_queryset(self):
    """
    Return the last five published questions.

    (not including those set to be published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
