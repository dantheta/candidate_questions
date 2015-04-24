import datetime

from django.core.management.base import BaseCommand
from candidates.models import Candidate
from questions.models import Answer
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

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
                                 if candidate.contact_address and 
                                    candidate.status = candidate.PARTICIPATING]


        print 'sending e-mails'
        conn = get_connection()
        for c in candidates_with_email:
            if c.should_send_reminder():

                print 'emailing', c
                # store timestamp for reminder email so that they don't get another one for <REMINDER_TIME_PERIOD> days
                c.last_reminder_sent = timezone.now()
                c.save()
                msg = make_email(c)
                conn.send_messages([msg])
        conn.close()
