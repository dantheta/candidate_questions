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
        inputbox = self.browser.find_element_by_id('id_postcode')
        inputbox.send_keys('bn1 1ee')

        # When I hit enter, I am taken to a new URL, and now the page
        # shows the constituency for my postcode
        inputbox.send_keys(Keys.ENTER)
        wmc_1_url = self.browser.current_url
        self.assertRegexpMatches(wmc_1_url, '/constituencies/.+')
        self.check_for_strings_in_page_element('h1',
            'Brighton, Pavilion'
        )

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

        # There is still a postcode field on the page so I can look up 
        # another constituency. I type in the postcode of my office.
        inputbox = self.browser.find_element_by_id('id_postcode')
        inputbox.send_keys('SW1A 0AA')
        inputbox.send_keys(Keys.ENTER)

        # I am taken to a new URL, and now the page shows the
        # constituency for my office's postcode
        wmc_2_url = self.browser.current_url
        self.assertRegexpMatches(wmc_2_url, '/constituencies/.+')
        self.check_for_strings_in_page_element('h1',
            'Cities of London and Westminster'
        )

        # The URL is different to the URL for my constituency
        self.assertNotEqual(wmc_1_url, wmc_2_url)

        # There is no trace of my constituency information on the page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Brighton, Pavilion', page_text)
        self.assertNotIn('Caroline Lucas', page_text)

        # Satisfied, I go back to sleep.
