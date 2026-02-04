from django.urls import path
from . import views


urlpatterns=[

    path("customers/",views.customers),
    path("add_customer/",views.add_customer),
    path("save_customer/",views.save_customer),
    path("edit_customer/<cust_id>",views.edit_customer),
    path("update_customer/<cust_id>",views.update_customer),
    path("delete_customer/<cust_id>",views.delete_customer),

    path("measurements/",views.measurements),
    path('add_churidar_measurement/<cust_id>/', views.add_churidar_measurement,name='add_churidar_measurement'),
    path("save_ch_measure/",views.save_ch_measure,name="save_ch_measure"),
    path("edit_chmeasure/<cust_id>",views.edit_chmeasure),
    path("update_ch_measure/<cust_id>",views.update_ch_measure),
    path("delete_chmeasure/<cust_id>",views.delete_chmeasure),
    path('add_saree_measurement/<cust_id>/', views.add_saree_measurement, name='add_saree_measurement'),
    path("save_sr_measure/",views.save_sr_measure,name="save_sr_measure"),
    path("edit_srmeasure/<cust_id>",views.edit_srmeasure),
    path("update_sr_measure/<cust_id>",views.update_sr_measure),
    path("delete_srmeasure/<cust_id>",views.delete_srmeasure),
    path("export/churidar/csv/",views.export_churidar_csv,name="export_churidar_csv"),
    path("export/saree/csv/",views.export_saree_csv,name="export_saree_csv"),
    path("staff_details/",views.staff_details),
    path("add_staff/",views.add_staff),
    path("save_staff/",views.save_staff),


]