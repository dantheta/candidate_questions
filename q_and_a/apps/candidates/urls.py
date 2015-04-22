from django.conf.urls import patterns, url
from django.views.decorators.http import require_POST

from views import CandidateQuestionsView, CandidateAnswer, CandidateAuthenticateView, CandidateAnswerList, CandidateAnswerDetail

urlpatterns = patterns('',
    url(r'^/authenticate/(?P<token>.*)/',
        CandidateAuthenticateView.as_view(),
        name='candidate_authenticate'),
    url(r'^/(?P<pk>\d+)/questions',
        CandidateQuestionsView.as_view(), name='candidate_questions'),
    url(r'^/answer/(?P<pk>\d+)',
        require_POST(CandidateAnswer.as_view()), name='candidate_answer'),
    url(r'^/view_answers/?$',
        CandidateAnswerList.as_view(), name='candidate_answer_list'),
    url(r'^/view_answer/(?P<pk>\d+)',
        CandidateAnswerDetail.as_view(), name='candidate_answer_detail')
)

