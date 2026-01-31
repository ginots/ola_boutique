from django.urls import path
from . import views


urlpatterns=[
    path("",views.index),
    path("customers/",views.customers),
    path("add_customer/",views.add_customer),
]