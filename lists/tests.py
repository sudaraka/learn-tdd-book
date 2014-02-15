""" lists app unit test. """

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from .views import home_page


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
        expected_html = render_to_string('home.html',
                                         {'new_item_text': item_text})

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(response.content.decode(), expected_html)
