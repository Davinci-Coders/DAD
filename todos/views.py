# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from todos.forms import TodoItemForm
from todos.models import Item


@login_required
def todos(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        # TODO: check that Item is owned by User
        # TODO: handle a case of a user passing a bad `id`
        #       - hint: Item.DoesNotExist
        obj = Item.objects.get(id=item_id)
        obj.completed = True
        obj.save()
    context = {
        'all_of_them': Item.objects.filter(user=request.user)
    }
    return render(request, 'todos.html', context)


@login_required
def new_todo(request):
    form = TodoItemForm()
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            # form.save()
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

    context = {
        'form': form,
    }
    return render(request, 'new_todo.html', context)
