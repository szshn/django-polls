from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return (
            Question.objects
            .filter(pub_date__lte=timezone.now(), choice__isnull=False)
            .order_by("-pub_date")
            .distinct()[:5]
        )

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return (
            Question.objects
            .filter(pub_date__lte=timezone.now(), choice__isnull=False)
            .distinct()
        )

    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return (
            Question.objects
            .filter(pub_date__lte=timezone.now(), choice__isnull=False)
            .distinct()
        )
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice."
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()    
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))