from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FunctionalTest(LiveServerTestCase):

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
