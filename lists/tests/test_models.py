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

    def test_duplicate_items_are_invalid(self):
        """
        adding duplicate items to the list must be prevented at model level

        """

        list_ = List.objects.create()
        Item.objects.create(text='SAME', list=list_)

        with self.assertRaises(ValidationError):
            item = Item(text='SAME', list=list_)
            item.full_clean()

    def test_can_save_same_item_in_different_lists(self):
        """ test as the name suggests """

        list_1 = List.objects.create()
        Item.objects.create(text='SAME', list=list_1)
        list_2 = List.objects.create()
        item = Item.objects.create(text='SAME', list=list_2)
        item.full_clean()

    def test_list_ordering(self):
        """ test as name suggest """

        list_ = List.objects.create()
        i1 = Item.objects.create(list=list_, text='i1')
        i2 = Item.objects.create(list=list_, text='item 2')
        i3 = Item.objects.create(list=list_, text='3')

        self.assertEqual(list(Item.objects.all()), [i1, i2, i3])

    def test_string_representation(self):
        """ test as name suggest """

        item = Item(text='Some Text')
        self.assertEqual(str(item), 'Some Text')
