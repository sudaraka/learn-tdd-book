""" list view controller. """

from django.shortcuts import render, redirect

from .models import Item


def home_page(request):
    """ Render home page HTML. """

    if 'POST' == request.method:
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'home.html', {'items': Item.objects.all()})
