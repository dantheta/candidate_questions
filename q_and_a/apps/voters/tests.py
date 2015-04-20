from mock import patch

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

    @patch('voters.views.ynmp_get_constituency_from_postcode')
    def test_homepage_can_look_up_constituency_from_postcode(
            self, mock_ynmp_get_constituency_from_postcode
        ):
        mock_ynmp_get_constituency_from_postcode.return_value = None
        request = HttpRequest()
        request.method = 'POST'
        request.POST['postcode'] = 'SW1A 1AA'

        response = HomePageView(request)

        mock_ynmp_get_constituency_from_postcode.assert_called_once_with('SW1A 1AA')

        # TODO: Retrieve static file, JSON parsing, find correct elements
