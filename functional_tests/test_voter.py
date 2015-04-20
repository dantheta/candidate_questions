from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class VoterTest(FunctionalTest):

    def test_view_answers(self):
        # So that I can decide for whom to vote
        # As a voter
        # I want to read the answers given by candidates in my constituency

        # I visit the homepage and am invited to enter my postcode
        self.browser.get(self.live_server_url)
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
