import datetime

from django.core.management.base import BaseCommand
from django.db.models import Max
from candidates.models import Candidate
from questions.models import Answer
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from django.conf import settings

def make_email(candidate):
    subject = u'New questions for ' + candidate.constituency_name + u' candidates'
    email_from = u'questions@campaignreply.org'
    to = candidate.contact_address

    text_content = render_to_string('candidates/reminder.txt', {'candidate': candidate})
    html_content = render_to_string('candidates/reminder.html', {'candidate': candidate})
    msg = EmailMultiAlternatives(subject, text_content, email_from, [to])
    msg.attach_alternative(html_content, 'text/html')
    return msg

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Send a reminder email to participating candidates who haven't answered a question
        in <n> days, but have more questions to answer"""

        candidates_with_email = [candidate for candidate in Candidate.objects.all()
                                 if candidate.contact_address and candidate.participating]

        reply = raw_input(u'this will e-mail up to {} candidates, are you sure? [y/n] '.format(len(candidates_with_email)))
        if not reply or reply[0].lower() != u'y':
            return

        #cutoff date is defined in settings
        reminder_date = datetime.date.today() - datetime.timedelta(settings.REMINDER_TIME_PERIOD)

        print 'sending e-mails'
        conn = get_connection()
        for c in candidates_with_email:
            # consider moving this check to a model method to allow testing

            last_answer = Answer.objects.filter(candidate=c,completed=True).aggregate(Max('completed_timestamp'))['completed_timestamp__max']
            open_questions = c.get_open_question_count()
            print "Candidate: ", c, "; Last answer: ", last_answer, "; Open questions: ", open_questions

            if last_answer is None: # don't send to people who haven't answered a question ever
                continue
            if last_answer <= reminder_date and open_questions > 0:

                print 'emailing', c
                msg = make_email(c)
                conn.send_messages([msg])
        conn.close()
