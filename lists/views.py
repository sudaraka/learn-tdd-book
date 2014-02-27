""" list view controller. """

from django.shortcuts import render, redirect

from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request):
    """ Render home page HTML. """

    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """ Render list view page HTML """

    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if 'POST' == request.method:
        form = ExistingListItemForm(for_list=list_, data=request.POST)

        if form.is_valid():
            form.save()

            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    """ Handle new list creation via HTTP POST """

    form = ItemForm(data=request.POST)

    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)

        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
