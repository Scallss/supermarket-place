import datetime
import json
from django.shortcuts import render, redirect 
from .models import Product
from main.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_main(request):

    context = {
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

@csrf_exempt
def add_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Pastikan semua field disertakan
            new_product = Product.objects.create(
                user=request.user,  # Ambil user dari request yang sudah login
                name=data["name"],
                price=int(data["price"]),
                description=data["description"],
                stock=int(data["stock"]),
                image=data['image'],
                category=data["category"],  # Default category ke string kosong jika tidak ada
            )

            new_product.save()
            return JsonResponse({"status": "success"}, status=200)

        except KeyError as e:
            # Tangani error jika ada field yang hilang
            return JsonResponse({"status": "error", "message": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            # Tangani error lain
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):

    user = request.user
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    stock = request.POST.get("stock")
    image = request.FILES.get("image")
    category = strip_tags(request.POST.get("category"))

    new_product = Product(
        name=name, price=price,
        description=description, stock=stock,
        image=image, category=category, user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def edit_product(request, id):
    product = Product.objects.get(pk = id)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = Product.objects.get(pk = id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.user.is_authenticated:
        # Redirect authenticated users to the homepage or other page
        return redirect('main:show_main')

   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")