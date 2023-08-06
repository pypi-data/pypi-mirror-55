"""
 test file
"""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.


def create_question(question_text, days):
    """
    create a question with a given `question_text` and days
    which is when the question should be published
    where days can be either negative or positive
    negative for questions published in the past
    positive for questions yet to be published
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """
    all tests for Question model
    """

    context_object_name = 'latest_question_list'

    def test_no_questions(self):
        """
        show a message if no questions exists
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context[self.context_object_name], [])

    def test_past_question(self):
        """
        questions in the past are displayed on the index page
        """
        create_question('past question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context[self.context_object_name],
            ['<Question: past question>']
        )

    def test_future_question(self):
        """
        questions in the future should not be displayed
        """
        create_question('future question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context[self.context_object_name],
            []
        )

    def test_future_and_past_questions(self):
        """
        questions only in the past are displayed even if
        there are questions in the future
        """
        create_question('future question', 30)
        create_question('past question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context[self.context_object_name],
            ['<Question: past question>']
        )

    def test_two_past_questions(self):
        """
        multiple questions can be also shown in the past
        """
        create_question('past question 1', -30)
        create_question('past question 2', -1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context[self.context_object_name],
            ['<Question: past question 2>',
             '<Question: past question 1>']
        )

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
        was_published_recently() returns False for
        questions whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(
            days=1,
            seconds=1
        )
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for
        questions whose pub_date is less than 1 day
        """
        time = timezone.now() - datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59
        )
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionDetailTests(TestCase):
    """
    all tests for detail view
    """

    def test_not_found_question(self):
        """
        404 is shown when trying to open detail for question
        that doesn't exists
        """
        response = self.client.get(reverse('polls:detail', args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        """
        404 is shown when trying to open detail for question
        that is not yet published
        """
        question = create_question('future question', 30)
        response = self.client.get(
            reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the question text is displayed when trying to open detail for question
        that has been published in the past
        """
        question = create_question('past question', -1)
        response = self.client.get(
            reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, question.question_text)
