from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from voters.views import HomePageView


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

        self.assertIn('Brighton Pavilion', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'constituency': 'Brighton Pavilion'}
        )
        self.assertEqual(response.content.decode(), expected_html)
