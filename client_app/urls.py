from django.urls import path
from . import views


urlpatterns=[
    path("",views.index),
    path("customers/",views.customers),
    path("add_customer/",views.add_customer),
    path("save_customer/",views.save_customer),
    path("edit_customer/<cust_id>",views.edit_customer),
    path("update_customer/<cust_id>",views.update_customer),
    path("delete_customer/<cust_id>",views.delete_customer),
]