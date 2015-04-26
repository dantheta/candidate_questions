from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.contrib.auth.models import User

from candidates.models import Candidate
from constituencies.models import Constituency
from questions.models import Question, Answer
from organisations.models import Organisation

from constituencies.views import HomePageView

class HomePageTest(TestCase):

    def test_uses_homepage_template(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePageView)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = HomePageView(request)
        expected_html = render_to_string('home.html', {
            'candidates_involved': 0,
            'questions_answered': 0,
        })
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

    def create_candidate(self, popit_id, name, constituency_id, party, participating=True):
        user = User.objects.create(username="candidate-" + str(popit_id))
        candidate = Candidate.objects.create(
            popit_id = popit_id,
            name = name,
            user = user,
            constituency_id = constituency_id,
            party = party,
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

    def create_answer(self, question, candidate, answer, completed=True):
        ans = Answer.objects.create(
            question=question,
            candidate=candidate,
            answer = answer,
            completed = completed
        )
        return(ans)

    def setUp(self):
        self.wmc = Constituency.objects.create(constituency_id=1, name='Dunny-on-the-Wold')
        org_1 = self.create_organisation('test_org_1', 'An Organisation')
        org_2 = self.create_organisation('test_org_2', 'Another Organisation')
        candidate_1 = self.create_candidate(
            popit_id = 1,
            name = 'Baldrick',
            constituency_id = self.wmc.constituency_id,
            party = 'Adder Party',
        )
        candidate_2 = self.create_candidate(
            popit_id = 2,
            name = 'Pitt the Even Younger',
            constituency_id = self.wmc.constituency_id,
            party = 'Whig',
        )
        candidate_3 = self.create_candidate(
            popit_id = 3,
            name = 'Brigadier General Horace Bolsom',
            constituency_id = self.wmc.constituency_id,
            party = 'Keep Royalty White, Rat Catching And Safe Sewage Residents Party',
            participating = False
        )
        q1 = self.create_question('Question 1', org_1)
        q2 = self.create_question('Question 2', org_1)
        q3 = self.create_question('Question A', org_2)
        a1 = self.create_answer(q1, candidate_1, 'Answer 1')
        a2 = self.create_answer(q2, candidate_1, 'Answer 2')
        a3 = self.create_answer(q3, candidate_1, 'Answer 3')
        a4 = self.create_answer(q1, candidate_2, 'Answer A')
        a5 = self.create_answer(q2, candidate_2, 'Answer B', False)

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

    def test_displays_parties_for_candidates(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))

        self.assertContains(response, 'Baldrick</a> (Adder Party')
        self.assertContains(response, 'Pitt the Even Younger</a> (Whig')

    def test_displays_answer_count_for_candidates(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))
        self.assertContains(response,
            '<li><a href="/candidates/view_answer/1">' +
            'Baldrick</a> ' +
            '(Adder Party /' +
            ' 3 questions answered)</li>',
            html=True
        )
        self.assertContains(response,
            '<li><a href="/candidates/view_answer/2">' +
            'Pitt the Even Younger</a> ' +
            '(Whig /' +
            ' 1 questions answered)</li>',
            html=True
        )

    def test_displays_non_participating_candidates(self):
        response = self.client.get('/constituencies/%d/' % (self.wmc.constituency_id,))
        self.assertContains(response,
            '<li><a href="/candidates/view_answer/3">' +
            'Brigadier General Horace Bolsom</a> ' +
            '(Keep Royalty White, Rat Catching And Safe Sewage Residents Party / ' +
            'Not participating)</li>',
            html=True
        )
