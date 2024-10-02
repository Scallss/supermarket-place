# Supermarket-Place
Place to fulfill your daily grocery needs!

Tautan untuk melihat website pada [link ini](http://pascal-hafidz-supermarketplace2.pbp.cs.ui.ac.id)

Loncat ke [Tugas 2](https://github.com/Scallss/supermarket-place#tugas-2)

Loncat ke [Tugas 3](https://github.com/Scallss/supermarket-place?tab=readme-ov-file#tugas-3)

Loncat ke [Tugas 4](https://github.com/Scallss/supermarket-place/tree/main#tugas-4) 

# Tugas 2
## Implementation Checklist 
Untuk mmebuat proyek Django baru bernama `supermarket-place` kita jalankan perintah berikut:

```
django-admin startproject supermarket-place .
```

Untuk membuat aplikasi bernama `main` yang mana kita akan menyimpan model kita yaitu Product, kita jalankan program berikut:
```
python manage.py startapp main
```

Untuk melakukan routing pada proyek agar dapat menjalani aplikasi `main`, kita dapat inlcude url pada aplikasi `main` pada `urls.py` pada direktori proyek supermarket_place dengan kode menyisipkan:
```
urlpatterns = [
...
path('', include('main.urls')),
...
]
```
Untuk membuat model pada aplikasi main dengan nama `Product` dan memiliki atribut `name`, `price`, `description` dan pada model saya ditambahkan atribut `stock`, `category`, `image`, `date_added` kita dapat menambahkannya ke dalam `models.py` seperti berikut:
```
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Untuk membuat fungsi pada `views.py`, saya memiliki 2 function yaitu `product_list` dan `product_details` yang keduanya diimplementasi sebagai berikut:
```
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
```
`product_detail` merupakan function yang mana akan merincikan detail suatu product yang dipilih

Untuk Membuat sebuah routing pada `urls.py` aplikasi `main` untuk memetakan fungsi yang telah dibuat pada `views.py` dilakukan seperti di bawah: 
```
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Pada baris paling akhir, ditambahkan static untuk handle pengambilan image.

Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat dilakukan dengan cara membuat project baru pada PWS yang kemudian kita tambahkan host PWS pada `settings.py` proyek sebagai berikut:
```
ALLOWED_HOSTS = [...., "pascal-hafidz-supermarketplace2.pbp.cs.ui.ac.id"]
```
Setelah itu kita bisa melakukan push pada direktori project django dengan menjalankan:
```
git remote add pws http://pbp.cs.ui.ac.id/pascal.hafidz/supermarketplace2
git branch -M master
git push pws master
```

## Bagan Alur Kerja Django
![image](https://github.com/user-attachments/assets/0001dbab-6ccd-4a84-9f7c-65ce6a6add86)
Mula-mula client mengirimkan request ke server yang akan diproses pertama oleh `urls.py`, yang tugasnya mencocokkan URL. Setelah menemukan URL yang cocok, forward request menuju `views.py` untuk menangani logika sesuai request.

View function pada `views.py` dapat berinteraksi dengan model jika diperlukan dan menentukan context untuk template HTML. `models.py` digunakan untuk berinteraksi dengan database. View function dapat menggunakan model untuk mengambil data dari database yang kemudian dikirim ke template HTML.

Templates digunakan untuk render data dan menghasilkan halaman web yang dikirim ke client browser.
## Fungsi Git
Git merupakan sistem version control yang memungkinkan developer untuk melakukan control version, kolaborasi bersama dengan developer lain, menyimpan riwayat perubahan, mmebuat branch untuk fitur baru/fix tanpa mempengaruhi main branch hingga menggabungkan perubahan tersebut dengan mudah.
## Django untuk Pemula
Django dipilih sebagai framework untuk pembelajaran pengembangan perangkat lunak adalah karena kemudahan penggunaan (Django menyediakan struktur yang jelas dan konvensi yang mudah diikuti) yang mana sudah banyak disediakan template untuk pembuatan website. Django juga mensupport interaksi front-end dan back-end dalam satu framework, sehingga pemula dapat mempelajari dengan lebih mudah. 
## Model Django sebagai ORM
Model Django disebut sebagai ORM dikarenakan model tersebut memungkinkan interaksi antara object python dan relational database menggunakan paradigma OOP. Dalam interaksi database konvensional, kita perlu menulis Query SQL untuk add, read, update, ataupun remove data. Hal ini kurang efisien karena Query SQL sulit beralih antar database, error-prone, dan rentan serangan injeksi SQL. 

Dengan menggunakan ORM Django, kita mampu mendefiniskan model menggunakan class python yang independen dari database yang mendasarinya. Selain itu, kita juga dengan mudah melakukan add, read, atau remove data tanpa Query.

# Tugas 3
## Checklist Implementation
Untuk membuat sebuah forms untuk dapat menambahkan objek model pada supermarket-place, mula-mula kita membuat file `forms.py` pada `main` dan mengisinya dengan kode:
```
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "stock", "category"]
```
Perlu dicatat bahwa, fields yang dimasukkan adalah attribute-attribute yang kita ingin isi sendiri.

Setelah ini, kita menambahkan fungsi baru `add_product` pada `views.py` yang akan digunakan untuk menambahkan Product ketika melakukan submit dari form.
```
from django.shortcuts import render, redirect    # Tambahkan redirect
from main.forms import ProductForm
...
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)
```
Kemudian, membuat fungsi `show_main` pada `views.py` yang menggantikan `product_list` dan `product_details` seperti berikut:
```
def show_main(request):
    product_entries = Product.objects.all()

    context = {
        'product_entries': product_entries
    }

    return render(request, "main.html", context)
```
`product_entries = Product.objects.all()` digunakan untuk mengambil seluruh instance object dari model yang telah disimpan pada database.

Setelah itu kita menambahkan url baru untuk path forms kita pada `urls.py` di `main`
```
from main.views import show_main, add_product

urlpatterns = [
    ...
    path('add_product/', add_product, name='add_product'),  # Add product page
```
Kemudian kita membuat templates yang akan menampilkan forms kita dan juga objek-objek yang sudah disimpan dengan membuat `base.html`, `main.html`, `add_product.html`.
`base.html`:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Supermarket-Place{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        nav {
            background-color: #343a40;
            padding: 1rem;
            text-align: center;
        }
        nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-size: 1.2rem;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .container {
            margin: 2rem;
        }
        h1 {
            color: #343a40;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{% url 'main:show_main' %}">Home</a>
        <a href="{% url 'main:add_product' %}">Add Product</a>
    </nav>

    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```
`main.html`:
```
{% extends 'base.html' %}

{% block title %}Product List{% endblock %}

{% block content %}
<h1>Available Products</h1>

{% if product_entries %}
    <ul>
        {% for product in product_entries %}
            <li style="margin-bottom: 2rem; list-style-type: none;">
                <strong style="font-size: 1.5rem;">{{ product.name }}</strong><br>
                Price: ${{ product.price }}<br>
                Stock: {{ product.stock }}<br>
                Category: {{ product.category }}<br>
                <p style="max-width: 400px;">{{ product.description }}</p>
            </li>
            <hr>
        {% endfor %}
    </ul>
{% else %}
    <p>No products available at the moment.</p>
{% endif %}
{% endblock %}
```
`add_product.html`:
```
{% extends 'base.html' %}

{% block title %}Add Product{% endblock %}

{% block content %}
<h1>Add a New Product</h1>

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Add Product</button>
</form>

<a href="{% url 'main:show_main' %}" style="display: inline-block; margin-top: 1rem;">Back to Products</a>
{% endblock %}
```

Kita dapat melihat objek model yang ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID. Untuk mendapatkan ID sebuah objek, kita bisa tambahkan attribut id pada `models.py` kita.
```
from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```
Selanjutnya kita bisa menambahkan fungsi `show_xml`, `show_json`, `show_xml_by_id`, `show_json_by_id` pada `views.py` untuk dapat melihat objek model yang telah kita tambahkan pada database.
```
...
from django.http import HttpResponse
from django.core import serializers
...
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```
Jangan lupa tambahkan path untuk setiap fungsi yang ditambahkan agar bisa diakses.
```
...
from main.views import show_main, add_product, show_xml, show_json, show_xml_by_id, show_json_by_id
...
urlpatterns = [
    ...
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]
```
## Mengapa perlu data delivery dalam pengimplementasian sebuah platform?
Data delivery krusial pada pengembangan sebuah platform dikarenakan data delivery berkaitan langsung dengan cara data dikirim dari server ke end-user. Data delivery memungkinkan pengiriman konten secara dinamis yang mana data berubah tergantung interkasi pengguna atau keadaan server. Dari segi keamanan, pengimplementasian data delivery yang baik juga penting dalam memastikan data yang ditransmisikan tidak dapat disalahgunakan oleh pihak ketiga.

## XML atau JSON?
Menurutku JSON lebih baik (juga lebih populer) dibandingkan XML karena JSON memiliki ukuran yang lebih kecil yang mana fakta ini didukung oleh sintaks JSON yang lebih sederhana. Selain itu, JSON lebih banyak didukung oleh bahasa pemrograman, terutama JavaScript yang merupakan bahasa yang ramai digunakan dalam web development.

## Fungsi method `is_valid()` pada form Django
Method `is_valid()` berfungsi untuk melakukan validasi input yang kita masukkan pada form, dan validasi yang dilakuakan disesuaikan ketentuan pada form tersebut. Kita membutuhkan fungsi ini untuk memeriksa apakah setiap field dalam form diisi dengan benar, membersihkan data yang 'valid', dan juga menangani error yang mungkin dihadapi ketika submit form.

## Kenapa diperlukan `csrf_token` saat membuat form Django?
csrf_token dibutuhkan untuk mencegah serangan CSRF (Cross-Site Request Forgery) yaitu serangan yang mana penyerang mencoba membuat user tanpa sadar melakukan hal yang tidak diinginkan. CSRF token memastikan setiap pengiriman form berasal dari halaman yang sah. Jika kita tidak menambahkan csrf_token, aplikasi yang kita buat menjadi rentan terhadap serangan csrf dan penyerang dapat melakukan hal tanpa sepengetahuan pengguna yang login ke dalam aplikasi. Penyerang dapat memanfaatkan serangan ini untuk melakukan hal-hal tergantung konteks aplikasi. Contohnya seperti mengubah informasi pribadi pengguna, melakukan pembelian online, melakukan transfer uang, dan lainnya tanpa sepengetahuan pengguna sahnya.

## Mengakses URL XML dan JSON melalui Postman
XML:
![image](https://github.com/user-attachments/assets/2518a025-2fbc-4519-bdb4-4759f228c171)

JSON:
![image](https://github.com/user-attachments/assets/987a8a3e-59a2-4ae7-8d9c-aa13a22892c1)

XML by id:
![image](https://github.com/user-attachments/assets/74816d86-2996-4654-ace1-129541c19187)

JSON by id:
![image](https://github.com/user-attachments/assets/115ca63d-a5a4-486c-96ae-fbe827bd0811)

# Tugas 3
## Checklist Implementation

Untuk mengimplementasikan fungsi registrasi, login, dan logout, bisa dimulai dengan pertama membuat fungsinya satu-satu pada `views.py`. Selain implementasi yang utama, juga diimplementasi cookies untuk menghandle session. Implementasi codenya adalah sebagai berikut:
```
...
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
...
@login_required(login_url='/login')    # Ditambahkan decorator ini sehingga page show_main hanya dapat diakses jika user sudah login
def show_main(request):
...
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
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```

Setelah fungsinya sudah dibuat, kita bisa langsung melakukan routing pada `urls.py` pada direktori `main`.
```
...
from main.views import register, login_user, logout_user  
...
urlpatterns = [
    ...
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
```

Setelah itu, lakukan modifikasi templates:
`base.html`:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Supermarket-Place{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        header {
            background-color: #343a40;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        nav {
            background-color: #495057;
            padding: 1rem;
            text-align: center;
        }
        nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-size: 1.2rem;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .container {
            margin: 2rem;
        }
        h1{
            margin: 0;
            color: black;
        }

        h2 {
            margin: 0;
            color: #f8f9fa;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <header>
        <h2>Supermarket-place</h2>
        <h2>Pascal Hafidz Fajri - 2306222746</h2>
    </header>
    
    <nav>
        <a href="{% url 'main:show_main' %}">Home</a>
        {% if user.is_authenticated %}
            <a href="{% url 'main:add_product' %}">Add Product</a>
            <a href="{% url 'main:logout' %}">Logout</a>
        {% endif %}
    </nav>

    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

`main.html`:
```
{% extends 'base.html' %}

{% block title %}Product List{% endblock %}

{% block content %}
<h1>Available Products</h1>

{% if product_entries %}
    <ul>
        {% for product in product_entries %}
            <li style="margin-bottom: 2rem; list-style-type: none;">
                <strong style="font-size: 1.5rem;">{{ product.name }}</strong><br>
                Price: ${{ product.price }}<br>
                Stock: {{ product.stock }}<br>
                Category: {{ product.category }}<br>
                <p style="max-width: 400px;">{{ product.description }}</p>
            </li>
            <hr>
        {% endfor %}
    </ul>
{% else %}
    <p>No products available at the moment.</p>
{% endif %}
<a href="{% url 'main:logout' %}">
    <button>Logout</button>
</a>
{% endblock %}
```

Tambahkan `login.html`:
```
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}
<div class="login">
  <h1>Login</h1>

  <form method="POST" action="">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input class="btn login_btn" type="submit" value="Login" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %} Don't have an account yet?
  <a href="{% url 'main:register' %}">Register Now</a>
</div>

{% endblock content %}
```

Tambahkan `register.html`:
```
{% extends 'base.html' %}

{% block meta %}
<title>Register</title>
{% endblock meta %}

{% block content %}

<div class="login">
  <h1>Register</h1>

  <form method="POST">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input type="submit" name="submit" value="Daftar" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

{% endblock content %}
```

Untuk membuat dua akun dan tiga dummy data pada masing-masing user di lokal, bisa jalankan [http://localhost:8000/](http://localhost:8000/). Kemudian pergi ke page registrasi untuk membuat 2 user. Setelah itu, login ke salah satu user dan tambahkan 3 dummy data. Lakukan hal yang sama untuk user satunya lagi. Contoh alur webpage-nya adalah sebagai berikut:
![image](https://github.com/user-attachments/assets/afb12d8f-46ed-44fb-baa8-9db0e49579be)

![image](https://github.com/user-attachments/assets/ba5ec6e7-fd8c-451c-addb-ac9b15bdbb35)

![image](https://github.com/user-attachments/assets/0bc8977b-2b48-490c-a71b-dde1248db23e)

Untuk menghubungkan model `Product` dengan `user` sehingga setiap entry pada product itu disesuaikan dengan setiap user, dilakukan perubahan pada `models.py` dan `views.py`. Pada `models.py` kita tambahkan attribute user dengan field `ForeignKey`.
```
from django.contrib.auth.models import User
...
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Selanjutnya pada `views.py`, kita tambahkan kode sehingga pada setiap entry `Product` yang dilakukan, akan disimpan juga user yang memasukkan entry tersebut, sehingga product yang ditampilakn juga akan difiler sesuai user yang sedang logged in.

```
...
def show_main(request):
    product_entries = Product.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        ...
    }
...
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)
```

Untuk menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti `last_login`, kita hanya perlu melakukan modifikasi ekstra pada tempalates `main.html`, karena sebelumnya sudah diimplementasikan cookies dan juga sudah mengimplementasikan user. 
Pada `main.html` tambahkan kode berikut:
```
{% extends 'base.html' %}

{% block title %}Product List{% endblock %}

<h1>Welcome, {{ user.username }}!</h1>
...
<a href="{% url 'main:logout' %}">
    <button>Logout</button>
</a>
<h5>Sesi terakhir login: {{ last_login }}</h5>
{% endblock %}
```
Dengan ini, kita dapat mengetahui informasi user yang sedang logged in seperti username dan last_login-nya

## Perbedaan HttpResponseRedirect() dan redirect()?
Biarpun keduanya berfungsi untuk pengalihan ke URL lain, mereka terdapat perbedaan dari sisi parameter yang bisa diterimanya. `HttpResponseRedirect()` hanya dapat menerima parameter berupa URL untuk melakukan pengaliahan URL, sedangkan `redirect` lebih fleksibel yang mana dapat menerima parameter berupa model, view, dan juga URL biarpun pada akhirnya akan mengembalikan sebuah `HttpResponseRedirect()` juga.

## Cara kerja penghubungan model Product dengan User
Untuk menghubungkan model Product dengan user, kita bisa menambahkan field `ForeignKey` pada model `Product`. Field ini berguna untuk membuat suatu relationship one-to-many (satu user bisa memiliki banyak product), dengan cara menghubungkan field tersebut dengan built in model `User` pada Django. Kodenya adalah sebagai berikut: `user = models.ForeignKey(User, on_delete=models.CASCADE)`. Belum selesai sampai situ, kita juga perlu menghubungkan entry product dengan user yang memasukannya, dan juga menampilkan product sesuai dengan user yang sedang logged in. 

Untuk menghubungkan entry product dengan user dilakukan seperti berikut:
```
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)
```

Untuk menampilkan product sesuai dengan user yang sedang logged in:
```
def show_main(request):
    product_entries = Product.objects.filter(user=request.user)    # filter Product yang ditampilkan

    context = {
        'name': request.user.username,
        'product_entries': product_entries,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)
```

# Bagaimana Django mengingat user yang logged in? Kegunaan lain cookies dan apakah semua cookies aman digunakan?
Django mengingat user yang sedang logged in dengan mengimplementasikan session cookies. Cara kerjanya adalah ketika user login, Django menciptakan sesi untuk user tersebut dan mengirimkan cookie khusus untuk browser user. Cookie ini berisi id unik yang disimpan pada pada server. Cookie ini tidak berisi informasi mengenai user, namun berperan sebagai kunci untuk mengakses session yang disimpan dalam server. Setiap kali user mengunjungi page baru, browser user mengirimkan cookie lagi ke server, sehingga menyimpan session user secara berkala. Dengan adanya sesi ini, Django bisa mengidentifikasi pengguna yang sedang login di setiap request menggunakan `request.user`. Saat user logout, Django menghapus cookie dari server dan membuatnya tidak valid lagi.

Selain menyimpan session, cookies juga berguna untuk melacak preferensi dan aktivitas user. Hal ini sangat berguna terutama untuk mendapatkan data mengenai halaman yang dikunjungi, atau produk yang dilihat user sehingga kita dapat menggunakan informasi itu untuk memberikan rekomendasi yang tepat kepada user tersebut. Selain itu, cookies juga dapat berperan sebagai penyimpan barang yang user tambahkan pada keranjang dalam kasus aplikasi e-commerce. 

Namun, cookies juga memiliki kerentanannya sendiri. Apabila kita tidak melakukan prosedur keamanan yang tepat, cookies kita bisa saja tidak aman digunakan. Jika cookies tidak menggunakan misalnya flag secure atau http only, cookie dapat lebih mudah diserang dan dicuri oleh attacker. Selain itu pada koneksi http, cookie dapat diserang dengan menggunakan teknik seperti man-in-the-middle attacks. Contoh lainnya, apabila tidak diimplementasi CSRF token, penyerang juga dapat mencuri dan menggunakan cookies valid dan melakukan request sensitif atas nama pengguna.


# Tugas 4
## Checklist Implementation 
Untuk implementasi fungsi untuk menghapus dan mengedit `Product`, bisa dilakukan dengan menambah fungsi-fungsi di bawah ini pada `views.py`: 
```
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
```
Kedua fungsi tersebut masing-masing akan mengedit atau menghapus Product. Setelah itu, lakukan routing pada `urls.py` dalam `main` app:
```
from main.views import *
...
urlpatterns = [
    ...
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
]
```

Selain itu, untuk melakukan kostumisasi design web page saya, saya banyak menggunakan tailwind CSS untuk mewujudkan tampilan simple-modern pada web page. Selain tampilan yang menarik, setiap page juga dibuat responsif, sehigga mudah digunakan pada segala device. Berikut code-nya:

Pada `base.html`, dilakukan template dasar web page dengan menggunakan Tailwind. Selain itu juga include `navbar.html`.
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Supermarket-Place{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
    {% include 'navbar.html' %}
    <div class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

`navbar.html` menginisialisasikan sebauh navigation bar yang responsif dengan fitur-fitur yang berbeda tergantung apakah user sudah login atau belum. Fitur responsif di sini adalah terdapat dropdown menu yang cukup standar pada device yang lebih sempit lebarnya. 

```
<nav class="bg-white shadow-md">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <!-- Logo and Home Link -->
        <div class="flex items-center space-x-8">
            <a class="text-xl font-semibold text-gray-800">Supermarket-Place</a>
            
            <!-- Home and Add Product links -->
            <div class="hidden sm:flex space-x-6">
                <a href="{% url 'main:show_main' %}" class="text-gray-600 hover:text-indigo-600 transition">Home</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'main:add_product' %}" class="text-gray-600 hover:text-indigo-600 transition">Add Product</a>
                {% endif %}
            </div>
        </div>

        <!-- User Profile Picture and Dropdown (for large screens) -->
        <div class="relative hidden sm:flex items-center space-x-4">
            {% if user.is_authenticated %}
                <div class="relative">
                    <button id="profile-menu-button" class="block h-10 w-10 rounded-full overflow-hidden border-2 border-gray-300 focus:outline-none">
                        <!-- Static Profile Image -->
                        <img class="h-full w-full object-cover" src="https://placehold.co/400" alt="User Profile">
                    </button>

                    <!-- Dropdown Menu -->
                    <div id="profile-dropdown" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5">
                        <div class="px-4 py-2 text-sm text-gray-700">Welcome, {{ user.username }}</div> <!-- User Greeting -->
                        <a href="{% url 'main:logout' %}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Logout</a>
                    </div>
                </div>
            {% endif %}
        </div>

        <!-- Mobile Menu Button and Profile Picture (for small screens) -->
        <div class="sm:hidden flex items-center space-x-2">
            <!-- Mobile Menu Button -->
            <button id="mobile-menu-button" class="text-gray-500 hover:text-indigo-600 transition">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            </button>

            <!-- User Profile Picture (for small screens) -->
            {% if user.is_authenticated %}
                <button id="mobile-profile-menu-button" class="block h-10 w-10 rounded-full overflow-hidden border-2 border-gray-300 focus:outline-none">
                    <img class="h-full w-full object-cover" src="https://placehold.co/400" alt="User Profile">
                </button>

                <!-- Dropdown Menu for Small Screens -->
                <div id="mobile-profile-dropdown" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5">
                    <div class="px-4 py-2 text-sm text-gray-700">Welcome, {{ user.username }}</div> <!-- User Greeting -->
                    <a href="{% url 'main:logout' %}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Logout</a>
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Mobile Menu, hidden by default -->
    <div class="sm:hidden hidden" id="mobile-menu">
        <div class="space-y-1 px-2 pb-3 pt-2">
            <a href="{% url 'main:show_main' %}" class="block rounded-md bg-gray-900 px-3 py-2 text-base font-medium text-white" aria-current="page">Home</a>
            {% if user.is_authenticated %}
                <a href="{% url 'main:add_product' %}" class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Add Product</a>
            {% endif %}
        </div>
    </div>
</nav>

<script>
    // Toggle mobile menu visibility
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    // Toggle profile dropdown visibility (large screens)
    const profileMenuButton = document.getElementById('profile-menu-button');
    const profileDropdown = document.getElementById('profile-dropdown');
    profileMenuButton.addEventListener('click', () => {
        profileDropdown.classList.toggle('hidden');
    });

    // Toggle profile dropdown visibility (small screens)
    const mobileProfileMenuButton = document.getElementById('mobile-profile-menu-button');
    const mobileProfileDropdown = document.getElementById('mobile-profile-dropdown');
    mobileProfileMenuButton.addEventListener('click', () => {
        mobileProfileDropdown.classList.toggle('hidden');
    });
</script>
```

Pada halaman daftar `Product` di `main.html`, telah diimplementasikan card design untuk setiap produk agar mudah dilihat pengguna. Jika belum ada Product yang terdaftar, maka akan muncul foto kucing sedih. Implementasi tampilan card design sendiri pun langsung dilakukan pada `main.html` dan terdapat fitur edit serta delete seperti berikut: 

```
{% extends 'base.html' %}
{% load static %}
{% block title %}Product List{% endblock %}

{% block content %}
<div class="text-center">
    <h1 class="text-3xl font-semibold mb-6">Available Products</h1>
</div>
{% if product_entries %}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {% for product in product_entries %}
        <div class="bg-white shadow-md rounded-lg overflow-hidden max-w-xs flex flex-col">  <!-- Use flex column layout -->
            <img class="w-full h-64 object-cover object-center" src="{{ product.image.url }}" alt="{{ product.name }}"> 
            <div class="p-2 flex-1">  <!-- Allow this div to grow and take available space -->
                <h2 class="text-lg font-semibold mb-2">{{ product.name }}</h2>
                <p class="text-gray-600 mb-2">Price: ${{ product.price }}</p>
                <p class="text-gray-600 mb-2">Stock: {{ product.stock }}</p>
                <p class="text-gray-600 mb-2">Category: {{ product.category }}</p>
                <p class="text-gray-500 text-sm">{{ product.description }}</p>
            </div>

            <!-- Add Edit and Delete buttons -->
            <div class="flex justify-between p-2"> 
                <a href="{% url 'main:edit_product' product.id %}" class="text-indigo-500 hover:text-indigo-600 font-medium">Edit</a>

                <form action="{% url 'main:delete_product' product.id %}" method="POST" onsubmit="return confirm('Are you sure you want to delete this product?');">
                    {% csrf_token %}
                    <button type="submit" class="text-red-500 hover:text-red-600 font-medium">Delete</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
{% else %}
    <div class="flex flex-col items-center justify-center min-h">
        <img src="{% static 'image/sad-cat.jpg' %}" alt="Sad Face" class="w-max h-32 mb-4">
        <p class="text-center text-gray-500 text-xl">No products available at the moment.</p>
    </div>
{% endif %}
{% endblock %}
```

Selain itu, berikut adalah kode untuk tampilan lain:

`register.html`:
```
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="flex items-start justify-center mt-16 bg-gray-100">
    <div class="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h1 class="text-2xl font-semibold text-gray-800 mb-6 text-center">Create an Account</h1>

        <form method="POST" action="" class="space-y-6">
            {% csrf_token %}
            <div>
                <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                <input type="text" name="username" id="username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Enter your username" required>
            </div>
            
            <div>
                <label for="password1" class="block text-sm font-medium text-gray-700">Password</label>
                <input type="password" name="password1" id="password1" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Enter your password" required>
                <p class="text-sm text-gray-500">Your password must contain at least 8 characters, not commonly used, and not entirely numeric.</p>
            </div>

            <div>
                <label for="password2" class="block text-sm font-medium text-gray-700">Confirm Password</label>
                <input type="password" name="password2" id="password2" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Confirm your password" required>
            </div>

            <div>
                <button type="submit" class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition">Register</button>
            </div>
        </form>

        {% if messages %}
        <div class="mt-4 text-red-600">
            <ul>
                {% for message in messages %}
                <li>{{ message }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}

        <p class="mt-4 text-sm text-center text-gray-600">
            Already have an account? 
            <a href="{% url 'main:login' %}" class="text-indigo-600 hover:text-indigo-500">Login Now</a>
        </p>
    </div>
</div>
{% endblock %}
```

`login.html`:
```
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="flex items-start justify-center mt-16 bg-gray-100">
    <div class="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h1 class="text-2xl font-semibold text-gray-800 mb-6 text-center">Login</h1>

        <form method="POST" action="" class="space-y-6">
            {% csrf_token %}
            <div>
                <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                <input type="text" name="username" id="username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Enter your username">
            </div>
            
            <div>
                <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                <input type="password" name="password" id="password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Enter your password">
            </div>

            <div>
                <button type="submit" class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition">Login</button>
            </div>
        </form>

        {% if messages %}
        <div class="mt-4 text-red-600">
            <ul>
                {% for message in messages %}
                <li>{{ message }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}

        <p class="mt-4 text-sm text-center text-gray-600">
            Don't have an account yet? 
            <a href="{% url 'main:register' %}" class="text-indigo-600 hover:text-indigo-500">Register Now</a>
        </p>
    </div>
</div>
{% endblock %}
```

`edit_product.html`:
```
{% extends 'base.html' %}

{% block title %}Edit Product{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto mt-10 bg-white p-8 shadow-md rounded-lg">
    <h1 class="text-2xl font-semibold mb-6 text-gray-800">Edit Product</h1>

    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        
        <!-- Loop through the form fields -->
        {% for field in form %}
            <div class="mb-4">
                <label for="{{ field.id_for_label }}" class="block text-gray-700 font-medium mb-2">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <p class="text-sm text-gray-500">{{ field.help_text }}</p>
                {% endif %}
                {% if field.errors %}
                    <p class="text-sm text-red-500">{{ field.errors }}</p>
                {% endif %}
            </div>
        {% endfor %}

        <div class="flex justify-end">
            <button type="submit" class="bg-indigo-500 text-white font-bold py-2 px-4 rounded-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                Save Changes
            </button>
        </div>
    </form>

    <a href="{% url 'main:show_main' %}" class="block mt-4 text-indigo-500 hover:text-indigo-600">
        Back to Products
    </a>
</div>
{% endblock %}
```

`delete_product.html`:
```
{% extends 'base.html' %}

{% block title %}Delete Product{% endblock %}

{% block content %}
<div class="max-w-xl mx-auto mt-10 bg-white p-8 shadow-md rounded-lg text-center">
    <h1 class="text-2xl font-semibold mb-6 text-gray-800">Delete Product</h1>
    <p class="mb-6 text-gray-600">Are you sure you want to delete the product <strong>{{ product.name }}</strong>?</p>

    <form method="POST">
        {% csrf_token %}
        <button type="submit" class="bg-red-500 text-white font-bold py-2 px-4 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500">
            Yes, Delete
        </button>
    </form>

    <a href="{% url 'main:show_main' %}" class="block mt-4 text-indigo-500 hover:text-indigo-600">
        Cancel
    </a>
</div>
{% endblock %}
```

`add_product.html`:
```
{% extends 'base.html' %}
{% load static %}

{% block title %}Add Product{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto mt-10 bg-white p-8 shadow-md rounded-lg">
    <h1 class="text-2xl font-semibold mb-6 text-gray-800">Add a New Product</h1>

    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {% for field in form %}
        <div class="mb-4">
            <label for="{{ field.id_for_label }}" class="block text-gray-700 font-medium mb-2">{{ field.label }}</label>
            <div class="border border-gray-300 rounded-md shadow-sm">
                {{ field }}
            </div>
            {% if field.help_text %}
                <p class="text-sm text-gray-500">{{ field.help_text }}</p>
            {% endif %}
            {% if field.errors %}
                <p class="text-sm text-red-500">
                    {{ field.label }}: {{ field.errors.as_text }}
                </p>
            {% endif %}
        </div>
        {% endfor %}


        <div class="flex justify-end">
            <button type="submit" class="bg-indigo-500 text-white font-bold py-2 px-4 rounded-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                Add Product
            </button>
        </div>
    </form>

    <a href="{% url 'main:show_main' %}" class="block mt-4 text-indigo-500 hover:text-indigo-600">
        Back to Products
    </a>
</div>
{% endblock %}
```

Di luar ini, saya mengembalikan ImageField untuk model `Product` pada `models.py`:
```
class Product(models.Model):
    ...
    image = models.ImageField(upload_to='products/')  # Images stored in 'media/products/'
    ...
```

Karena ditambahkan ImageField ini, maka ditambahkan `request.FILES` pada beberapa fungsi `views.py`:
```
...
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    ...

def edit_product(request, id):
    product = Product.objects.get(pk = id)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    ...
...
```

## Urutan Prioritas pengambilan CSS Selector untuk suatu elemen HTML
Terdapat urutan prioritas dalam penggunaan CSS selector untuk suatu HTML, urutannya adalah sebagai berikut dengan nomor 1 adalah yang paling diutamakan:
1. Inline styles
   Merupakan CSS yang langsung ditulis pada atribut elemen yang terkait
2. External and Internal Style Sheets
   External styles adalah file CSS yang terpisah dan internal styles adalah gaya yang didefinisikan dalam tag <style> di dalam dokumen HTML
3. Browser Default
   Browser default styles adalah styles bawaan yang diberikan oleh browser jika tidak ada CSS yang didefinisikan.

## Responsive Design pada pengembangan aplikasi web dan contohnya
Responsive Design merupakan konsep penting karena pada dasarnya kita akan menggunakan device beragam untuk mengakses internet dan web. Dengan adanya responsive design, setiap pengguna dengan device apapun dapat melihat aplikasi web kita dengan mudah. Contoh aplikasi yang sudah menerapkan responsive web design seperti Youtube, Instagram, LinkedIn, dll. Kebalikannya, aplikasi web yang belum responsive meliputi Craigslist.

## Apa itu margin, border, dan padding serta cara mengimplementasikannya
Margin adalah jarak antara elemen HTML dengan elemen lain di sekitarnya yang digunakan untuk memberikan ruang kosong di luar border elemen. Sifatnya adalah tidak memiliki warna, dan area ini sepenuhnya transparan. Cara implementasinya:
```
.element {
    margin: 10px;
}

.element {
    margin-top: 10px;
    margin-right: 25px;
    margin-bottom: 10px;
    margin-left: 25px;
}
```

Border adalah garis yang membungkus suatu elemen. Border terletak di antara margin dan padding. Sifatnya adalah bisa diberi warna, ukuran, serta jenis garis (solid, dashed, dotted, dll). Cara implementasinya adalah sebagai berikut:
```
.element {
    border: 4px solid black; /* Ukuran 4px, solid, warna hitam */
}
```

Padding adalah jarak antara konten elemen dengan border. Padding bisa diatur untuk semua sisi atau untuk masing-masing sisi. Cara implementasinya adalah sebagai berikut:
```
.element {
    padding: 25px;
}

.element {
    padding-top: 10px;
    padding-right: 10px;
    padding-bottom: 20px;
    padding-left: 20px;
}
```

## Apa itu Flex Box dan Grid Layout serta Kegunaannya
Flexbox merupakan model layout satu dimensi untuk mengatur elemen dalam satu baris atau kolom. Flexbox dirancang untuk tata letak yang dinamis dan fleksibel serta dengan mudah dapat menyesuaikan diri terhadap ukuran layar atau kontainer tanpa perlu pengaturan manual yang rumit.

Grid Layout adalah model layout dua dimensi yang memungkinkan kita mengatur elemen dalam bentuk baris dan kolom. Kita bisa mengatur elemen dalam dua arah (horizontal dan vertikal) secara bersamaan menggunakan grid. Grid digunakan bilamana kita membutuhkan sesuatu yang memberikan kontrol dengan presisi tinggi dalam membuat tata letak yang kompleks.
