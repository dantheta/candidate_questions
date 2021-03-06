from selenium import webdriver
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

        
if __name__ == '__main__':
    unittest.main()
