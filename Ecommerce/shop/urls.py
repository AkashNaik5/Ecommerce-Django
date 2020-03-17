from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='track'),
    path('about/', views.about, name='AboutUs'),
    path('products/<int:myid>', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank/<int:order_id>/', views.thank, name='thank'),
    path('handlerequest/', views.handlerequest, name='handlerequest')

]