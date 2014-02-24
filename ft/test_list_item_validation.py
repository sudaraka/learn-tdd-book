""" Functional test for TDD Book. """

from .base import BaseFunctionalTest


class ItemValidationTest(BaseFunctionalTest):
    """ Test user inputs """

    def test_cannot_add_empty_list_items(self):
        """ Check if empty items are being added to the list """

        # Edith goes to the homepage and accidentally tries to submit and empty
        # list item. She hits Enter on the empty input box.

        # The homepage refreshes, and there is an error message saying that
        # list items cannot be blank.

        # She tries again with some text for the item, which now works.

        # Perversely, she not decides to submit a second blank list item

        # She receives a similar message on the list page.

        # And she can correct it by filling some text in

        self.fail('write me!')
