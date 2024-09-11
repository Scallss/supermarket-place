# Supermarket-Place
Place to fulfill your daily grocery needs!

Tautan untuk melihat website pada [link ini](http://pascal-hafidz-supermarketplace2.pbp.cs.ui.ac.id)

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
