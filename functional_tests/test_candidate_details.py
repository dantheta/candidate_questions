from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class CandidateDetailsTest(FunctionalTest):

    fixtures = ['ft-data.json']

    def test_answers_appear_on_candidate_details_page(self):

        # I visit the page for my constituency directly.
        constituency_url = (self.live_server_url + '/constituencies/65787/')
        self.browser.get(constituency_url)

        # I can see the name of my constituency.
        self.check_for_strings_in_page_element('h1', 'Brighton, Pavilion')

        # I am thinking of voting for Purna Sen so I click
        # on her name.
        candidate_1_link = self.browser.find_element_by_link_text('Purna Sen')
        candidate_1_link.click()

        # I am taken to a new URL
        self.assertEqual(self.browser.current_url,
            self.live_server_url + '/candidates/view_answer/4279'
        )

        # The newpage shows Purna's name, party and constituency.
        self.check_for_strings_in_page_element('body', {
            'Purna Sen',
            'Brighton, Pavilion',
            'Labour Party',
        })

        # I can see the questions asked of Purna.
        self.check_for_strings_in_page_element('body', {
            'What is the meaning of life?',
            'What is your quest?',
        })

        # I can see her answers to each question.
        self.check_for_strings_in_page_element('body', {
            'Lorem Ipsum is not simply random text.',
            'To find the Holy Grail',
        })

        # I can see which organisation asked each question.
        self.check_for_strings_in_page_element('body', {
            'The Very Organisation',
            'The Quite Organisation',
        })

        # No unanswered questions appear.
        self.fail('Finish the test!')

        # I decide to review the answers from another candidate
        # in my constituency so I click a link to return to the
        # constituency page

        # I click on Caroline Lucas's name. I am taken to a new URL.
        # I can see Carorline's details on the page.
        # I can see the questions asked of Caroline.
        # I can see her answers to each question.
        # I can see which organisation asked each question.
        # None of the details for Purna appear on the page.

        # Having made my decision, I go back to sleep.
