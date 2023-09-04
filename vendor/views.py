from django.shortcuts import get_object_or_404, redirect, render

from menu.forms import CategoryForm, ProductItemForm
from .forms import VendorForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, ProductItem
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')  
            return redirect('vprofile')   
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        #loads existing content in database so you know what to update. 
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile, 
        'vendor': vendor,
    }
    return render (request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor). order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    productitems = ProductItem.objects.filter(vendor=vendor, category=category)
    context = {
        'productitems': productitems,
        'category': category,
    }
    return render(request, 'vendor/items_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)

def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_ProductItem(request):
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            ProductItem = form.save(commit=False)
            ProductItem.vendor = get_vendor(request)
            ProductItem.slug = slugify(item_title)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('items_by_category', ProductItem.category.id)
        else:
            print(form.errors)
    else:
        form = ProductItemForm()
        # modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
            'form':form,
        }
    return render(request, 'vendor/add_productItem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
    product = get_object_or_404(ProductItem, pk=pk)
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(item_title)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('items_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductItemForm(instance=product)
        # modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form':form,
        'product': product,
    }
    return render(request, 'vendor/edit_product.html', context)

def delete_product(request, pk=None):
    product = get_object_or_404(ProductItem, pk=pk)
    product.delete()
    messages.success(request, 'Product has been deleted successfully!')
    return redirect('items_by_category', product.category.id)

