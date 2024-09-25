# Supermarket-Place
Place to fulfill your daily grocery needs!

Tautan untuk melihat website pada [link ini](http://pascal-hafidz-supermarketplace2.pbp.cs.ui.ac.id)

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
