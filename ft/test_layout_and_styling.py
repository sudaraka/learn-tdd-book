""" Functional test for TDD Book. """

from .base import BaseFunctionalTest


class LayoutAndStyleTest(BaseFunctionalTest):
    """ Test UI layout. """

    def test_layout_and_style(self):
        """ Test to ensure we have the basic layout and style """

        # Edith goes to the home page
        self.browser.get(self.server_url)
        #self.browser.set_window_size(1024, 768)
        viewport = self.browser.get_window_size()

        # She notice the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            viewport['width'] / 2, delta=5)

        # She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            viewport['width'] / 2, delta=5)
