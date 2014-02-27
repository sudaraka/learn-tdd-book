""" list app form test """

from django.test import TestCase

from lists.forms import (ExistingListItemForm, ItemForm,
                         EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR)
from lists.models import Item, List


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

    def test_form_handles_saving_to_a_list(self):
        """ test as name suggest """

        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
    """ Test existing list item form """

    def test_form_renders_item_text_input(self):
        """ test as name suggests """

        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)

        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """ test as name suggest """

        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_validation_for_duplicate_items(self):
        """ test as name suggest """

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='SAME')
        form = ExistingListItemForm(for_list=list_, data={'text': 'SAME'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
