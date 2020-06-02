import os

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ItemForm
from .models import Item


# Create your views here.

def get_to_do_list(request):
    items = Item.objects.all()
    development = os.environ.get('DEVELOPMENT', False)
    db = os.environ.get('DATABASE_URL')
    context = {
        "items": items,
        "development":development,
        "db":db
    }

    return render(request, 'to_do/to_do_list.html', context)


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_to_do_list')

    form = ItemForm()
    context = {
        'form': form
    }
    return render(request, 'to_do/add_item.html', context)


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('get_to_do_list')
    form = ItemForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'to_do/edit_item.html', context)


def toggle_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.done = not item.done
    item.save()
    return redirect('get_to_do_list')

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('get_to_do_list')
