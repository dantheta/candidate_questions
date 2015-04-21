from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from voters.views import HomePageView
from voters.models import Constituency

class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePageView)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = HomePageView(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_homepage_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['postcode'] = 'bn1 1ee'

        response = HomePageView(request)

        self.assertEqual(Constituency.objects.count(), 1)
        new_wmc = Constituency.objects.first()
        self.assertEqual(new_wmc.name, 'Brighton, Pavilion')

    def test_homepage_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['postcode'] = 'bn1 1ee'

        response = HomePageView(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_homepage_only_saves_constituency_when_necessary(self):
        request = HttpRequest()
        HomePageView(request)
        self.assertEqual(Constituency.objects.count(), 0)

    def test_homepage_only_saves_new_constituencies(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['postcode'] = 'bn1 1ee'

        response = HomePageView(request)
        response2 = HomePageView(request)

        self.assertEqual(Constituency.objects.count(), 1)

    def test_homepage_handles_invalid_input(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['postcode'] = 'not a postcode'

        response = HomePageView(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


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
