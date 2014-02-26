""" list app form test """

from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR


class ItemFormTest(TestCase):
    """ Test item form """

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """ test as name suggests """

        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """ test as name suggest """

        form = ItemForm({'data': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])
