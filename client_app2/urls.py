from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("login/", views.check_signin, name="check_signin"),
    path("logout/", views.sign_out, name="logout"),
    path("index/",views.index, name="index"),
    path("new-order/<cust_id>/", views.new_order, name="new_order"),
    path("save-order/", views.save_order, name="save_order"),
    path("all-orders", views.all_orders, name="all_orders"),
    path("order-status/<order_id>/", views.update_order_status, name="update_order_status"),
    path("update_ongoing_status/<order_id>/", views.update_ongoing_status, name="update_ongoing_status"),
    path("export-orders-csv/", views.export_orders_csv, name="export_orders_csv"),
    path("ongoing-orders/", views.ongoing_orders, name="ongoing_orders"),
    path("stock/", views.stock, name="stock"),
    path("add-stock/", views.add_stock, name="add_stock"),
    path("save-stock/", views.save_stock, name="save_stock"),
    path("edit-stock/<stock_id>/", views.edit_stock, name="edit_stock"),
    path("update-stock/<stock_id>/", views.update_stock, name="update_stock"),
    path("delete-stock/<stock_id>/", views.delete_stock, name="delete_stock"),
    path("used-stock/<stock_id>/", views.used_stock, name="used_stock"),
    path("save-used-stock/<stock_id>/", views.save_used_stock, name="save_used_stock"),
    path("export-stock-csv/", views.export_stock_csv, name="export_stock_csv"),
    path("invoice/<inv_id>/", views.invoice, name="invoice"),
    path("profile/", views.profile, name="profile"),
    path("profile-settings/", views.profile_settings, name="profile_settings"),
    path("update_password/", views.update_password, name="update_password"),
    path("invoice/pdf/<int:pk>/", views.invoice_pdf, name="invoice_pdf"),

    path('account_type_adm', views.account_type_adm, name='account_type_adm'),
    path('edit_account_type_adm/<int:id>/', views.edit_account_type_adm, name='edit_account_type_adm'),
    path('delete_account_type_adm/<int:id>/', views.delete_account_type_adm, name='delete_account_type_adm'),

    path('account_br_adm/', views.account_br_adm, name='account_br_adm'),
    path('edit_account_adm/<id>/', views.edit_account_adm, name='edit_account_adm'),
    path("delete_account_adm/<int:id>/", views.delete_account_adm, name="delete_account_adm"),

    path('transaction_br_adm/', views.transaction_br_adm, name='transaction_br_adm'),

    path('ledger_br_adm/', views.ledger_br_adm, name='ledger_br_adm'),
    path("export_ledger_csv/", views.export_ledger_csv, name="export_ledger_csv"),
]
