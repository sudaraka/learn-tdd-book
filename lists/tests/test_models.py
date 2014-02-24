""" lists app unit test. """

from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    """ Test Item model related operations """

    def test_saving_and_retrieving_items(self):
        """ Test saving and retrieving items """

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'First (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, second_item.text)
        self.assertEqual(saved_items[1].list, list_)

    def test_cannot_save_empty_list_items(self):
        """ test as the name suggest """

        list_ = List.objects.create()
        item = Item(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        """ test as the name suggest """

        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % list_.id)
