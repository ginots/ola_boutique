from django.urls import path
from . import views


urlpatterns=[

    path("customers/",views.customers, name="customers"),
    path("add_customer/",views.add_customer),
    path("save_customer/",views.save_customer),
    path("edit_customer/<cust_id>",views.edit_customer),
    path("update_customer/<cust_id>",views.update_customer),
    path("delete_customer/<cust_id>",views.delete_customer),

    path("measurements/",views.measurements, name="measurements"),
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
    path("staff_details/",views.staff_details, name="staff_details"),
    path("add_staff/",views.add_staff),
    path("save_staff/",views.save_staff),
    path("edit_staff/<stf_id>",views.edit_staff),
    path("update_staff/<stf_id>",views.update_staff),
    path("staff_emp/",views.staff_emp, name="staff_emp"),
    path("update_emp/",views.update_emp),
    path("salary_status/",views.salary_status, name="salary_status"),
    path("salary_generate/",views.salary_generate),
    path("generate_salary/",views.generate_salary),
    path("delete_salary/", views.delete_salary, name="delete_salary"),
    path("save_salary/",views.save_salary),
    path("toggle_salary_status/<sal_id>/", views.toggle_salary_status),
    path("add_overtime/<sal_id>",views.add_overtime),
    path("save_overtime/",views.save_overtime),
    path("delete_overtime/<sal_id>/", views.delete_overtime, name="delete_overtime"),
    path("edit_salary_status/<stf_id>/",views.edit_salary_status,name="edit_salary_status"),
    path("get_overtime_details/<salary_id>/",views.get_overtime_details,name="overtime_details"),
    path("salary_history/",views.salary_history, name="salary_history"),
    path("export-salary-csv/", views.export_salary_csv, name="export_salary_csv"),
    path("export-customers-csv/", views.export_customers_csv, name="export_customers_csv"),
    path("export_staff_details_csv/", views.export_staff_details_csv, name="export_staff_details_csv"),
    path("update_pay_status/<pay_id>", views.update_pay_status, name="update_pay_status"),
    path("add_pending/<sal_id>/",views.add_pending),
    path("save_pending/<sal_id>/", views.save_pending, name="save_pending"),
    path("add_advance/<int:sal_id>/", views.add_advance, name="add_advance"),
    path("save_advance/<int:sal_id>/", views.save_advance, name="save_advance"),



]