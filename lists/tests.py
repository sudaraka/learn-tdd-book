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


class ListViewTest(TestCase):
    """ List view UI (url, view, template) test """

    def test_used_list_template(self):
        """ Test if list is rendered using correct template list.html """

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        """
        Make sure the list table on home page display all the items

        """

        check_items = ['Item 1', 'Item 2', 'Another item']

        for item in check_items:
            Item.objects.create(text=item)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        for item in check_items:
            self.assertContains(response, item)


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

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
