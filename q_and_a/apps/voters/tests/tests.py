from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from voters.models import Constituency
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

    def test_uses_constituency_template(self):
        wmc = Constituency.objects.create(constituency_id=1, name='My Constituency')
        response = self.client.get('/constituencies/%d/' % (wmc.constituency_id,))
        self.assertTemplateUsed(response, 'constituency.html')

    def test_displays_correct_constituency_name(self):
        correct_wmc = Constituency.objects.create(constituency_id=1, name='Correct Constituency')
        other_wmc = Constituency.objects.create(constituency_id=2, name='Other Constituency')

        response = self.client.get('/constituencies/%d/' % (correct_wmc.constituency_id,))

        self.assertContains(response, 'Correct Constituency')
        self.assertNotContains(response,'Other Constituency')

