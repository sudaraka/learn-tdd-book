""" lists app unit test. """

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    """ Test home page functions and UI. """

    def test_root_url_resolved_to_the_home_page_view(self):
        """ Uri / should be pointed to the home page. """

        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """ Check for home page content. """

        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode(), expected_html)


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


class ListViewTest(TestCase):
    """ List view UI (url, view, template) test """

    def test_used_list_template(self):
        """ Test if list is rendered using correct template list.html """

        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % list_.id)

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """
        Make sure the list table on home page display all the items

        """

        check_items = ['Item 1', 'Item 2', 'Another item']

        correct_list = List.objects.create()
        other_list = List.objects.create()

        for item in check_items:
            Item.objects.create(text=item, list=correct_list)
            Item.objects.create(text='Other %s' % item, list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        for item in check_items:
            self.assertContains(response, item)
            self.assertNotContains(response, 'Other %s' % item)

    def test_passes_correct_list_to_template(self):
        """ list view should get the current list object """

        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertEqual(response.context['list'], correct_list)
        self.assertNotEqual(response.context['list'], other_list)


class NewListTest(TestCase):
    """ Test functionality of creating a new list """

    def test_saving_a_POST_request(self):
        """
        Check if we can handle the submitted data via HTTP POST.

        """

        item_text = 'A new list item'

        self.client.post('/lists/new', data={'item_text': item_text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirects_after_POST(self):
        """
        Check if it redirect after handling the HTTP POST request

        """

        item_text = 'A new list item'

        response = self.client.post('/lists/new',
                                    data={'item_text': item_text})

        new_list = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/%d/' % new_list.id)


class NewItemTest(TestCase):
    """ Test adding new items to lists """

    def test_can_save_a_POST_reqest_to_an_existing_list(self):
        """ add and item to existing list """

        item_text = 'A new item for an existing list'

        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post('/lists/%d/new_item' % correct_list.id,
                         data={'item_text': item_text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)
        self.assertNotEqual(new_item.list, other_list)

    def test_redirects_to_list_view(self):
        """ add and item to existing list """

        item_text = 'A new item for an existing list'

        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post('/lists/%d/new_item' % correct_list.id,
                                    data={'item_text': item_text})

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)
