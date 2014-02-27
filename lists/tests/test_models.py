""" lists app unit test. """

from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ItemModelTest(TestCase):
    """ Test Item model related operations """

    def test_default_text(self):
        """ Test item's default text value """

        item = Item()
        self.assertEqual(item.text, '')

    def test_saving_and_retrieving_items(self):
        """ Test saving and retrieving items """

        list_ = List.objects.create()

        item = Item()
        item.list = list_
        item.save()

        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """ test as the name suggest """

        list_ = List.objects.create()
        item = Item(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """
        adding duplicate items to the list must be prevented at model level

        """

        list_ = List.objects.create()
        Item.objects.create(text='SAME', list=list_)

        with self.assertRaises(ValidationError):
            item = Item(text='SAME', list=list_)
            item.full_clean()
            #item.save()

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


class ListModelTest(TestCase):
    """ Test Item model related operations """

    def test_get_absolute_url(self):
        """ test as the name suggest """

        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % list_.id)
