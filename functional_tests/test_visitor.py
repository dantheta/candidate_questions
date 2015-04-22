from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_about_information(self):
        # So that I can learn more about this website
        # As a voter
        # I want to read a page of explanatory information

        # I can see the page title and header mention asking questions of candidates
        self.browser.get(self.live_server_url)
        self.assertIn('Ask your candidate', self.browser.title)
        self.check_for_strings_in_page_element('h1', 'Candidate Q&As')

        # I can see that the site is specific to the UK general election 2015
        # I can see that the site is a prototype
        self.check_for_strings_in_page_element('body', {
            'UK general election 2015',
            'prototype',
        })

        # I can see who made the site
        self.check_link_appears_on_page('http://89up.org/')
        self.check_link_appears_on_page('https://www.openrightsgroup.org/')
        self.check_link_appears_on_page('https://democracyclub.org.uk/')

        # I can find the source code for the site
        self.check_link_appears_on_page('https://github.com/DemocracyClub/candidate_questions/')

        # I can see an email address to write to with quesitons or comments
        self.check_link_appears_on_page('mailto:questions@campaignreply.org')
