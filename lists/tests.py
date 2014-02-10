from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from .views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolved_to_the_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_retuens_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
