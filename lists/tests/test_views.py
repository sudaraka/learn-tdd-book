""" lists app unit test. """

from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR


class HomePageTest(TestCase):
    """ Test home page functions and UI. """

    def test_home_page_renders_home_template(self):
        """ test as name suggests """

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        """ test as name suggests """

        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    """ List view UI (url, view, template) test """

    def test_display_item_form(self):
        """ Test if item form is bing used """

        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % list_.id)

        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

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

    def test_can_save_a_POST_reqest_to_an_existing_list(self):
        """ add and item to existing list """

        text = 'A new item for an existing list'

        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post('/lists/%d/' % correct_list.id,
                         data={'text': text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, correct_list)
        self.assertNotEqual(new_item.list, other_list)

    def test_POST_redirects_to_list_view(self):
        """ add and item to existing list """

        text = 'A new item for an existing list'

        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post('/lists/%d/' % correct_list.id,
                                    data={'text': text})

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def post_invalid_input(self):
        """ test as the name suggest """

        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % list_.id, data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        """ test as the name suggest """

        self.post_invalid_input()

        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """ test as the name suggest """

        response = self.post_invalid_input()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_shows_error_on_page(self):
        """ test as the name suggest """

        response = self.post_invalid_input()

        self.assertContains(response, escape(EMPTY_LIST_ERROR))


class NewListTest(TestCase):
    """ Test functionality of creating a new list """

    def test_saving_a_POST_request(self):
        """
        Check if we can handle the submitted data via HTTP POST.

        """

        text = 'A new list item'

        self.client.post('/lists/new', data={'text': text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_redirects_after_POST(self):
        """
        Check if it redirect after handling the HTTP POST request

        """

        text = 'A new list item'

        response = self.client.post('/lists/new',
                                    data={'text': text})

        new_list = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_for_invalid_input_renders_home_template(self):
        """ test as the name suggest """

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """ test as the name suggest """

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_invalid_input_passes_form_to_template(self):
        """ test as the name suggest """

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arnt_saved(self):
        """ test as the name suggest """

        self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
