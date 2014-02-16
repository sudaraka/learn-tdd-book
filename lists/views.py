""" list view controller. """

from django.shortcuts import render, redirect

from .models import Item


def home_page(request):
    """ Render home page HTML. """

    if 'POST' == request.method:
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    return render(request, 'home.html')


def view_list(request):
    """ Render list view page HTML """

    return render(request, 'list.html', {'items': Item.objects.all()})
