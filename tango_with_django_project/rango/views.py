from django.shortcuts import render, redirect
from django.http import HttpResponse
import tango_with_django_project.settings as settings
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.urls import reverse

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save()
            # Redirect to the add_page view with the slug of the newly created category.
            return redirect(reverse('rango:add_page', kwargs={'category_name_slug': new_category.slug}))
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return redirect(reverse('rango:show_category',
                            kwargs={'category_name_slug':
                                    category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def index(request):
    top_five_pages = Page.objects.order_by('-views')[:5]
    top_five_categories = Category.objects.order_by('-likes')[:5]
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['top_pages'] = top_five_pages
    context_dict['top_categories'] = top_five_categories
    
    return render(request, 'rango/index.html', context=context_dict)

def about(request) -> HttpResponse:
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!', 
        'boldmessage2': 'This tutorial has been put together by Aaron David',
    }
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/about.html', context=context_dict)