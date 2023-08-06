"""
 main views file
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    """/polls/"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions
        without those set to be published in the future"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """/polls/<question_id>/"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        exclude questions in the future
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    """/polls/<question_id>/results"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """/polls/<question_id>/vote"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
