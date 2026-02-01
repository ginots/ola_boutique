from django.urls import path
from . import views

urlpatterns = [
path("new-order/<cust_id>/", views.new_order, name="new_order"),
    path("save-order/", views.save_order, name="save_order"),
    path("all-orders", views.all_orders, name="all_orders"),
    path("order-status/<order_id>/", views.update_order_status, name="update_order_status"),
    path("export-orders-csv/", views.export_orders_csv, name="export_orders_csv"),
    path("ongoing-orders/", views.ongoing_orders, name="ongoing_orders"),


]
