""" list view controller. """

from django.shortcuts import render


def home_page(request):
    """ Render home page HTML. """

    return render(request, 'home.html')
