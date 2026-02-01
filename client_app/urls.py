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
    path("measurements/",views.measurements),
    path('add_churidar_measurement/<cust_id>/', views.add_churidar_measurement,name='add_churidar_measurement'),
    path("save_ch_measure/",views.save_ch_measure,name="save_ch_measure"),
    path('add_saree_measurement/<cust_id>/', views.add_saree_measurement, name='add_saree_measurement'),
    path("save_sr_measure/",views.save_sr_measure,name="save_sr_measure"),
]