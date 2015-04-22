from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.contrib.auth.models import User

from candidates.models import Candidate
from voters.models import Constituency
from questions.models import Question, Answer
from organisations.models import Organisation

from voters.views import HomePageView

class HomePageTest(TestCase):

    def test_uses_homepage_template(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePageView)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = HomePageView(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class LookUpConstituencyTest(TestCase):

    def test_homepage_can_save_a_POST_request(self):
        response = self.client.post(
            '/',
            data={'postcode': 'bn1 1ee'}
        )

        self.assertEqual(Constituency.objects.count(), 1)
        new_wmc = Constituency.objects.first()
        self.assertEqual(new_wmc.name, 'Brighton, Pavilion')

    def test_homepage_redirects_to_constituency_view(self):
        response = self.client.post(
            '/',
            data={'postcode': 'bn1 1ee'}
        )

        new_wmc = Constituency.objects.first()
        self.assertRedirects(response, '/constituencies/%d/' % (new_wmc.constituency_id,))

    def test_homepage_only_saves_constituency_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Constituency.objects.count(), 0)

    def test_homepage_only_saves_new_constituencies(self):
        response = self.client.post(
            '/',
            data={'postcode': 'bn1 1ee'}
        )
        response2 = self.client.post(
            '/',
            data={'postcode': 'bn1 1ee'}
        )

        self.assertEqual(Constituency.objects.count(), 1)

    def test_homepage_handles_invalid_input(self):
        response = self.client.post(
            '/',
            data={'postcode': 'not a postcode'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class ConstituencyModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        # TODO: constituency_id (pk) not specified yet this test still passes?!
        first_wmc = Constituency()
        first_wmc.name = 'My Constituency'
        first_wmc.save()

        second_wmc = Constituency()
        second_wmc.name = 'Your Constituency'
        second_wmc.save()

        saved_wmcs = Constituency.objects.all()
        self.assertEqual(saved_wmcs.count(), 2)

        first_saved_wmc = saved_wmcs[0]
        second_saved_wmc = saved_wmcs[1]
        self.assertEqual(first_saved_wmc.name, 'My Constituency')
        self.assertEqual(second_saved_wmc.name, 'Your Constituency')


class ConstituencyViewTest(TestCase):

    def create_candidate(self, popit_id, name, constituency_id, participating=True):
        user = User.objects.create(username="candidate-" + str(popit_id))
        candidate = Candidate.objects.create(
            popit_id = popit_id,
            name = name,
            user = user,
            constituency_id = constituency_id,
            participating = participating,
        )
        return(candidate)

    def create_organisation(self, username, name):
        user = User.objects.create(username=username)
        org = Organisation.objects.create(name=name, user=user)
        return(org)

    def create_question(self, question, org):
        q = Question.objects.create(question=question, organisation=org)
        return(q)

    def create_answer(self, question, candidate, answer):
        ans = Answer.objects.create(question=question, candidate=candidate, answer = answer)
        return(ans)

    def setUp(self):
        self.wmc = Constituency.objects.create(constituency_id=1, name='Dunny-on-the-Wold')
        org_1 = self.create_organisation('test_org_1', 'An Organisation')
        org_2 = self.create_organisation('test_org_2', 'Another Organisation')
        candidate_1 = self.create_candidate(1, 'Baldrick', self.wmc.constituency_id)
        candidate_2 = self.create_candidate(2, 'Pitt the Even Younger', self.wmc.constituency_id)
        q1 = self.create_question('Question 1', org_1)
        q2 = self.create_question('Question 2', org_1)
        q3 = self.create_question('Question A', org_2)
        a1 = self.create_answer(q1, candidate_1, 'Answer 1')
        a2 = self.create_answer(q2, candidate_1, 'Answer 2')
        a3 = self.create_answer(q3, candidate_1, 'Answer 3')
        a4 = self.create_answer(q1, candidate_2, 'Answer A')
        a5 = self.create_answer(q2, candidate_2, 'Answer B')

    def test_uses_constituency_template(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))
        self.assertTemplateUsed(response, 'constituency.html')

    def test_displays_correct_constituency_name(self):
        correct_wmc = Constituency.objects.create(constituency_id=2, name='Correct Constituency')
        other_wmc = Constituency.objects.create(constituency_id=3, name='Other Constituency')

        response = self.client.get('/constituencies/%d/' % (correct_wmc.constituency_id,))

        self.assertContains(response, 'Correct Constituency')
        self.assertNotContains(response,'Other Constituency')

    def test_displays_candidates_for_constituency(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))

        self.assertContains(response, 'Baldrick')
        self.assertContains(response, 'Pitt the Even Younger')

    def test_displays_answers_for_constituency(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))

        self.assertContains(response, 'Answer 1')
        self.assertContains(response, 'Answer 2')
        self.assertContains(response, 'Answer 3')
        self.assertContains(response, 'Answer A')
        self.assertContains(response, 'Answer B')
