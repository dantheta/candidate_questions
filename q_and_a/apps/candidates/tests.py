from django.db import IntegrityError
from django.test import TestCase

from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from questions.models import Question,Answer
from organisations.models import Organisation
from candidates.models import Candidate

# Create your tests here.

class TestQuestionAssignment(TestCase):
    def setUp(self):
        # create an organisation
        user = User(username='test_org_user')
        user.save()
        org = Organisation(name='test_org')
        org.user = user
        org.save()

        # create three questions
        self.q1 = Question(question='What is your name?', organisation=org)
        self.q1.save()

        # create a candidate
        self.candidate = Candidate(name='Terry', status=Candidate.PARTICIPATING, popit_id=1234)
        self.candidate.save()
        # post-save hook on candidate will automatically assign q1

        q2 = Question(question='What is your quest?', organisation=org)
        q2.save()
        q3 = Question(question='What is your favourite colour?',organisation=org)
        q3.save()


        # assign 1 question to the candidate
        self.answer = Answer.objects.get(question=self.q1, candidate=self.candidate)

    def test_auto_assign(self):
        """Auto-assign from post-save hook has succeeded"""
        self.assertEquals(self.answer.question, self.q1)

    def test_question_assignment_count(self):
        """Open question count increases when a new question is assigned"""
        self.assertEquals(self.candidate.get_open_question_count(), 1)
        existing = Answer.objects.filter(candidate=self.candidate)
        self.candidate.assign_questions(1)
        self.assertEquals(self.candidate.get_open_question_count(), 2)
        pass

    def test_question_assignment_count_close(self):
        """Open question count decreases when a question is completed"""
        self.assertEquals(self.candidate.get_open_question_count(), 1)
        self.answer.completed=True
        self.answer.save()
        self.assertEquals(self.candidate.get_open_question_count(), 0)
        pass

    def test_question_assignment(self):
        """Questions are assigned in age order"""
        # complete the existing assignment
        self.answer.completed=True
        self.answer.save()
        # assign a new one
        count = self.candidate.assign_questions(1)
        self.assertEquals(count,1)
        newanswer = Answer.objects.filter(candidate=self.candidate,completed=False)[0]
        self.assertEquals(newanswer.question.question, "What is your quest?")

    def test_no_more_questions(self):
        """No more questions are available"""
        self.candidate.assign_questions(2)
        count = self.candidate.assign_questions(1)
        self.assertEquals(count,0)


    def test_unique(self):
        """Question/Answer combinations must be unique"""
        answer = Answer(candidate=self.candidate, question=self.q1)
        self.assertRaises(IntegrityError,answer.save)


class ReminderTestCase(TestCase):
    def setUp(self):
        user = User(username='test_org1_user')
        user.save()
        o1 = Organisation(name='Organisation 1')
        o1.user = user
        o1.save()

        user = User(username='test_org2_user')
        user.save()
        o2 = Organisation(name='Organisation 2')
        o2.user = user
        o2.save()

        c1 = Candidate(popit_id=1235,
            name='Bob',
            contact_address='bob@example.com',
            status=Candidate.PARTICIPATING
            )
        c1.save()
        self.candidate = c1

        q1 = Question(organisation=o1,
            question='What is your name?',
            type='text',
            )
        q1.save()
        q2 = Question(organisation=o2,
            question='What is your quest?',
            type='text',
            )
        q2.save()

        a1 = Answer(candidate=c1,
            question=q1,
            completed=True,
            completed_timestamp=datetime.datetime(2015,1,1,
                tzinfo=timezone.get_current_timezone())
            )
        a1.save()
        self.a1 = a1

        a2 = Answer(candidate=c1,
            question=q2,
            completed=False
            )
        a2.save()
        self.a2 = a2

    def testReminder(self):
        """Reminder should be sent when last answer >n days ago, 
        last reminder is null or >n days ago and there are open questions"""
        self.assertEquals(self.candidate.should_send_reminder(), True)

    def testLast7DaysAnswer(self):
        """Reminder should not be sent when last answer is <n days ago"""
        self.a1.completed_timestamp = timezone.now()
        self.a1.save()
        self.assertEquals(self.candidate.should_send_reminder(), False)

    def testLast7DaysReminder(self):
        """Reminder should not be sent when last reminder is <n days ago"""
        self.candidate.last_reminder_sent = timezone.now()
        self.assertEquals(self.candidate.should_send_reminder(), False)

    def testNoOpenQuestions(self):
        """Reminder should not be send if there are no open questions"""
        self.a2.delete()
        self.assertEquals(self.candidate.should_send_reminder(), False)
        
    def testNeverAnswered(self):
        """Reminder should not be sent if the candidate has never answered"""
        self.a1.delete()
        self.a2.delete()
        self.assertEquals(self.candidate.should_send_reminder(), False)

