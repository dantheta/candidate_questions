from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ConstituencyTest(FunctionalTest):

    fixtures = ['ft-data.json']

    def test_view_constituency(self):
        # So that I can discover answers from relevant candidates
        # As a voter
        # I want to see which candidates in my costituency have answered
        # questions.

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
        self.assertNotIn('Cities of London and Westminster', page_text)

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
        self.assertNotIn('Cities of London and Westminster', page_text)

        # They can see:
        #   which candidates are standing in their constituency, and;
        #   to which party each belongs; and
        #   either the number of questions each has answered, or;
        #   that the candidate has chosen not to participate.
        self.check_for_strings_in_page_element('body', {
            'Chris Bowers (Liberal Democrats / 2 questions answered)',
            'Nigel Carter (UK Independence Party (UKIP) / 2 questions answered)',
            'Caroline Lucas (Green Party / 2 questions answered)',
            'Clarence Mitchell (Conservative Party / Not participating)',
            'Howard Pilott (The Socialist Party of Great Britain / 2 questions answered)',
            'Purna Sen (Labour Party / 2 questions answered)',
            'Nick Yeomans (Independent / 1 questions answered)',
        })

        # Satisfied, I go back to sleep
