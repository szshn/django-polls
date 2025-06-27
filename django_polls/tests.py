import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):        
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question_without_choices(question_text, days=0):
    """
    Create a question with the given `question_text` and publish the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_question_with_choices(question_text, days=0, choice_count=1):
    """
    Create a question with the given `question_text` with `choice_count`
    number of choices and publish the given number of `days` offset to now 
    (negative for questions published in the past, positive for questions 
    that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    for i in range(choice_count):
        question.choice_set.create(choice_text=f"Choice {i}")
    return question
    

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question_with_choices(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )
        
    def test_past_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question_with_choices(question_text="Past question.", days=-30)
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question_with_choices(question_text="Past question 1.", days=-30)
        question2 = create_question_with_choices(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1]
        )
    
    def test_no_choices_question(self):
        """
        Questions (published in the past) without choices aren't displayed
        on the index page.
        """
        create_question_without_choices(question_text="Question with no choices.")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

        
    def test_no_choices_question_and_one_choice_question(self):
        """
        Only the question with choice(s) are displayed on the index page.
        """
        question = create_question_with_choices(question_text="Question with no choices.")
        create_question_without_choices(question_text="Question with choices")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question_with_choices(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question_with_choices(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
    def test_no_choices_question(self):
        """
        The detail view of a question without any choices returns a
        404 not found.
        """
        no_choice_question = create_question_without_choices(question_text="Question with no choices.")
        url = reverse("polls:detail", args=(no_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question_with_choices(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question_with_choices(question_text="Past Question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    def test_no_choices_question(self):
        """
        The results view of a question without any choices returns a
        404 not found.
        """
        no_choice_question = create_question_without_choices(question_text="Question with no choices.")
        url = reverse("polls:results", args=(no_choice_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
# TODO: More tests
# Perhaps logged-in admin users should be allowed to see unpublished Question 
# entries, but not ordinary visitors. 
# https://docs.djangoproject.com/en/5.2/intro/tutorial05/#ideas-for-more-tests