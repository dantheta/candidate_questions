from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_strings_in_page_element(self, element, string_list):
        element_text = self.browser.find_element_by_tag_name(element).text
        self.assertTrue(
            all(strings in element_text for strings in string_list),
            '<%s> element did not contain one or more of the following strings: %s' % (element, string_list)
        )

    def check_link_appears_on_page(self, href):
        links = self.browser.find_elements_by_tag_name('a')
        self.assertTrue(
            any(link.get_attribute('href') == href for link in links)
        )

    def test_about_information(self):
        # So that I can learn more about this website
        # As a voter
        # I want to read a page of explanatory information

        # I can see the page title and header mention asking questions of candidates
        self.browser.get('http://localhost:8000')
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

    def test_view_answers(self):
        # So that I can decide for whom to vote
        # As a voter
        # I want to read the answers given by candidates in my constituency

        # I visit the homepage and am invited to enter my postcode
        self.browser.get('http://localhost:8000')
        inputbox = self.browser.find_element_by_id('id_postcode')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your postcode'
        )

        # I type in my friend's postcode to see how the system works
        inputbox.send_keys('SW1A 0AA')

        # When I hit enter, the page updates, and it now shows the constituency for my postcode
        inputbox.send_keys(Keys.ENTER)
        self.check_for_strings_in_page_element('h2', 'Cities of London and Westminster')

        # There is still a text box inviting me to enter another postcode
        # I type in my postcode
        inputbox.send_keys('bn1 1ee')

        # When I hit enter, the page updates, and it now shows the constituency for my postcode
        inputbox.send_keys(Keys.ENTER)
        self.check_for_strings_in_page_element('h2', 'Brighton Pavilion')

        # I can see which candidates are standing in my constituency
        self.check_for_strings_in_page_element('body', {
            'Chris Bowers',
            'Nigel Carter',
            'Caroline Lucas',
            'Clarence Mitchell',
            'Howard Pilott',
            'Purna Sen',
            'Nick Yeomans',
        })

        # I can see the questions asked of each candidate
        # I can see each candidate's answers to each question
        # I can see which organisation asked each question
        self.assertFail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
