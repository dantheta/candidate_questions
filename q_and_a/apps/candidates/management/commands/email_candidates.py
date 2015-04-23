from django.core.management.base import BaseCommand
from candidates.models import Candidate
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

def make_email(candidate):
    subject = u'Questions for ' + candidate.constituency_name + u' candidates'
    email_from = u'questions@campaignreply.org'
    to = candidate.contact_address

    text_content = render_to_string('candidates/email.txt', {'candidate': candidate})
    html_content = render_to_string('candidates/email.html', {'candidate': candidate})
    msg = EmailMultiAlternatives(subject, text_content, email_from, [to])
    msg.attach_alternative(html_content, 'text/html')
    return msg

class Command(BaseCommand):
    def handle(self, *args, **options):
        candidates_with_email = [candidate for candidate in Candidate.objects.all()
                                 if candidate.contact_address and not candidate.invited]
        if not candidates_with_email:
            print 'no e-mails waiting to be sent'
            return
        reply = raw_input(u'this will e-mail {} candidates, are you sure? [y/n] '.format(len(candidates_with_email)))
        if not reply or reply[0].lower() != u'y':
            return
        print 'sending e-mails'
        conn = get_connection()
        for candidate in candidates_with_email:
            print 'emailing', candidate
            msg = make_email(candidate)
            conn.send_messages([msg])
            candidate.invited = timezone.now()
            candidate.save()
        conn.close()
