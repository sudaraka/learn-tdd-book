""" lists app unit test. """

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from .views import home_page
from .models import Item


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

    def test_home_page_can_save_a_POST_request(self):
        """
        Check if home page can handle the submitted data via HTTP POST.

        """

        item_text = 'A new list item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text

        home_page(request)

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_home_page_redirects_after_POST(self):
        """
        Check if home page redirect after handling the HTTP POST request

        """

        item_text = 'A new list item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        """
        Make sure a normal visit to the home page doesn't create a new item.

        """

        request = HttpRequest()
        home_page(request)

        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        """
        Make sure the list table on home page display all the items

        """

        check_items = ['Item 1', 'Item 2', 'Another item']

        for item in check_items:
            Item.objects.create(text=item)

        request = HttpRequest()
        response = home_page(request)

        for item in check_items:
            self.assertIn(item, response.content.decode())


class ItemModelTest(TestCase):
    """ Test Item model related operations """

    def test_saving_and_retrieving_items(self):
        """ Test saving and retrieving items """

        first_item = Item()
        first_item.text = 'First (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[1].text, second_item.text)
