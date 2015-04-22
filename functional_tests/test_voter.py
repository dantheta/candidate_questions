from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class VoterTest(FunctionalTest):

    fixtures = ['ft-data.json']

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

        # I type in my postcode
        inputbox.send_keys('SW1A 0AA')

        # When I hit enter, I am taken to a new URL, and now the page 
        # shows the constituency for my postcode
        inputbox.send_keys(Keys.ENTER)
        voter1_wmc_url = self.browser.current_url
        self.assertRegexpMatches(voter1_wmc_url, '/constituencies/.+')
        self.check_for_strings_in_page_element('h1', 'Cities of London and Westminster')

        # A second user now visits the site

        ## New browser session to make sure that no information
        ## from the first user is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # The second user visits the home page. There is no sign of 
        # my constituency information.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Cties of London and Westminster', page_text)

        # They type in their postcode and press enter
        inputbox = self.browser.find_element_by_id('id_postcode')
        inputbox.send_keys('bn1 1ee')
        inputbox.send_keys(Keys.ENTER)
        
        # They are taken to a new URL, and now the page shows the
        # constituency for their postcode
        voter2_wmc_url = self.browser.current_url
        self.assertRegexpMatches(voter2_wmc_url, '/constituencies/.+')
        self.check_for_strings_in_page_element('h1', 'Brighton, Pavilion')

        # Their URL is different to the URL to which I was taken
        self.assertNotEqual(voter1_wmc_url, voter2_wmc_url)

        # Again, there is no trace of my constituency on their page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Cties of London and Westminster', page_text)
        
        # They can see which candidates are standing in their constituency
        self.check_for_strings_in_page_element('body', {
            'Chris Bowers',
            'Nigel Carter',
            'Caroline Lucas',
            'Clarence Mitchell',
            'Howard Pilott',
            'Purna Sen',
            'Nick Yeomans',
        })

        # They can see the questions asked of each candidate
        self.check_for_strings_in_page_element('body', {
            'What is the meaning of life?',
            'How many grains of sand are there under the sea?',
            'What is your name?',
            'What is your quest?',
        })

        # They can see each candidate's answers to each question
        self.check_for_strings_in_page_element('body', {
            '42',
            'I don\'t know.',
            'To find the Holy Grail',
            'Too many',
        })

        # They can see which organisation asked each question
        self.check_for_strings_in_page_element('body', {
            'The Very Organisation',
            'The Quite Organisation',
        })

        # Satisfied, they and I go back to sleep
