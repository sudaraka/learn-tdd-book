""" Functional test for TDD Book. """

import sys

from django.test import LiveServerTestCase

from selenium import webdriver


class BaseFunctionalTest(LiveServerTestCase):
    """ Shared subroutines for the FTs """

    @classmethod
    def setUpClass(cls):
        """ Initialize test/live servers """

        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]

                return

        LiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        """ Cleanup global test/live test environment """

        if cls.server_url == cls.live_server_url:
            LiveServerTestCase.tearDownClass()

    def setUp(self):
        """ Initialize environment for each test """

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        """ Cleanup environment of each test """

        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """ Check if given text exists in the listing table """

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        """ return the item input box on current page """

        return self.browser.find_element_by_id('id_text')
