from django.views.generic.edit import FormView
from forms import QuestionForm
from .models import Question
from django.http import HttpResponse
import json

class AddQuestion(FormView):
    form_class = QuestionForm

    def get_form_kwargs(self):
        kwargs = super(AddQuestion, self).get_form_kwargs()
        kwargs.update({'instance': Question(organisation_id=self.kwargs['org'])})
        return kwargs

    def get_success_url(self):
        return self.object.organisation.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(AddQuestion, self).form_valid(form)

def api(request, question_id):
    question = Question.objects.get(id=question_id)
    org = question.organisation
    data = json.dumps({
        'id': question.id,
        'organisation': {'name': org.name, 'id': org.id},
        'question': question.question,
        'answers': {int(a.candidate.popit_id): a.answer for a in question.answer_set.all() if a.answer},
    }, indent=2)
    return HttpResponse(data, content_type='application/json')

