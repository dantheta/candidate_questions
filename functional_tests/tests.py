from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_about_information(self):
        # So that I can learn more about this website
        # As a voter
        # I want to read a page of explanatory information

        # I can see the page title and header mention asking questions of candidates
        self.browser.get('http://localhost:8000')
        self.assertIn('Ask your candidate', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Candidate Q&As', header_text)

        # I can see that the site is specific to the UK general election 2015
        self.assertIn('UK general election 2015', self.browser.find_element_by_tag_name('body').text)

        # I can see that the site is a prototype
        self.assertIn('prototype', self.browser.find_element_by_tag_name('body').text)

        # I can see who made the site
        links = self.browser.find_elements_by_tag_name('a')
        self.assertTrue(
            any(link.get_attribute('href') == 'http://89up.org/' for link in links) and
            any(link.get_attribute('href') == 'https://www.openrightsgroup.org/' for link in links) and
            any(link.get_attribute('href') == 'https://democracyclub.org.uk/' for link in links)
        )

        # I can find the source code for the site
        self.assertTrue(
            any(link.get_attribute('href') == 'https://github.com/DemocracyClub/candidate_questions/' for link in links)
        )

        # I can see an email address to write to with quesitons or comments
        self.assertTrue(
            any(link.get_attribute('href') == 'mailto:questions@campaignreply.org' for link in links)
        )

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
        self.assertIn('Cities of London and Westminster', self.browser.find_element_by_tag_name('h2').text)

        # There is still a text box inviting me to enter another postcode
        # I type in my postcode
        inputbox.send_keys('bn1 1ee')

        # When I hit enter, the page updates, and it now shows the constituency for my postcode
        inputbox.send_keys(Keys.ENTER)
        self.assertIn('Brighton Pavilion', self.browser.find_element_by_tag_name('h2').text)

        # I can see which candidates are standing in my constituency
        body_text = self.browser.find_elements_by_tag_name('body').text
        self.assertIn('Chris Bowers', body_text)
        self.assertIn('Nigel Carter', body_text)
        self.assertIn('Caroline Lucas', body_text)
        self.assertIn('Clarence Mitchell', body_text)
        self.assertIn('Howard Pilott', body_text)
        self.assertIn('Purna Sen', body_text)
        self.assertIn('Nick Yeomans', body_text)

        # I can see the questions asked of each candidate
        # I can see each candidate's answers to each question
        # I can see which organisation asked each question
        self.assertFail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
