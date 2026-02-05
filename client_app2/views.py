import csv
import datetime
from datetime import date
from django.contrib.auth.decorators import login_required


from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

from client_app.models import TableOrders,TableCustomer

from .models import *


# Create your views here.
@login_required(login_url='/')
def index(request):
    today = timezone.localdate()
    year = today.year

    daily_orders = TableOrders.objects.filter(date=today).count()
    deliveries = TableOrders.objects.filter(due_date=today).count()
    today_total = TableOrders.objects.filter(date=today, status__in=["Ordered", "Completed"]).aggregate(total=Sum("total"))["total"] or 0
    month_total = TableOrders.objects.filter(date__year=year, date__month=today.month, status__in=["Ordered", "Completed"]).aggregate(total=Sum("total"))["total"] or 0

    all_months = [date(year, m, 1) for m in range(1, 13)]
    month_labels = [m.strftime("%b") for m in all_months]

    monthly_totals = (
        TableOrders.objects.filter(date__year=year, status__in=["Ordered", "Completed"])
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("total"), advance=Sum("advance_paid"))
    )

    # Map month -> total / advance
    total_map = {m["month"].month: m["total"] or 0 for m in monthly_totals}
    advance_map = {m["month"].month: m["advance"] or 0 for m in monthly_totals}

    totals = [total_map.get(m, 0) for m in range(1, 13)]
    advance_data = [advance_map.get(m, 0) for m in range(1, 13)]

    invoice = TableOrders.objects.all().order_by("-id")[:5]

    context = {
        "daily_orders": daily_orders,
        "deliveries": deliveries,
        "today_total": today_total,
        "month_total": month_total,
        "months": month_labels,
        "totals": totals,
        "advance_data": advance_data,
        "invoice": invoice,
    }

    return render(request, "index.html", context)


@login_required(login_url='/')
def new_order(request, cust_id):
    data = TableCustomer.objects.get(id=cust_id)
    return render(request,"new_order.html",{"data":data})

@login_required(login_url='/')
@transaction.atomic
def save_order(request):
    if request.method == "POST":
        year = timezone.now().year

        last_order = (
            TableOrders.objects
            .filter(order_id__startswith=f"ORD-{year}")
            .order_by("-id")
            .first()
        )

        if last_order:
            last_number = int(last_order.order_id.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        order_id = f"ORD-{year}-{new_number:04d}"

        sareefall_type = None
        item = ""
        lining = ""
        bottom = ""
        locking = ""
        pattern = ""
        customer_id = request.POST.get("customer_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        cloth_type = request.POST.get("cloth_type")
        if cloth_type == "1":
            item = ", ".join(request.POST.getlist("item"))
            lining = ", ".join(request.POST.getlist("lining"))
            bottom = ", ".join(request.POST.getlist("bottom"))
            locking = ", ".join(request.POST.getlist("locking"))
            pattern = ", ".join(request.POST.getlist("pattern"))

        elif cloth_type == "2":
            item = ", ".join(request.POST.getlist("item"))
            lining = ", ".join(request.POST.getlist("lining"))
            locking = ", ".join(request.POST.getlist("locking"))
            if "Sareefall" in locking:
                sareefall_type = request.POST.get("sareefall_type")
            pattern = ", ".join(request.POST.getlist("pattern"))
        image = request.FILES.get("image")
        due_date = request.POST.get("due_date")
        stitching_charges = float(request.POST.get("stitching_charges") or 0)
        additional_charges = float(request.POST.get("additional_charges") or 0)
        total = round(stitching_charges + additional_charges, 2)
        advance_paid = float(request.POST.get("advance_paid") or 0)
        balance = round(total - advance_paid, 2)
        notes = request.POST.get("notes")
        status = "Ordered"

        TableOrders.objects.create( customer_id=customer_id, order_id=order_id, name=name,phone=phone,
                                    email=email, address=address,cloth_type=cloth_type,
                                   item=item, lining=lining, bottom=bottom,
                                   locking=locking, pattern=pattern, sareefall_type=sareefall_type,
                                   image=image, due_date=due_date, notes=notes,
                                    stitching_charges=stitching_charges, additional_charges=additional_charges,
                                    total=total, advance_paid=advance_paid,balance=balance,
                                    status=status)

        return redirect("all_orders")
    return redirect("all_orders")

@login_required(login_url='/')
def all_orders(request):
    orders = TableOrders.objects.all().order_by("-id")

    q_search = request.GET.get('search_general')
    q_status = request.GET.get('status')
    q_purchase = request.GET.get('purchase_date')
    q_due = request.GET.get('due_date')

    if q_search:
        orders = orders.filter(
            Q(name__icontains=q_search) |
            Q(customer_id__iexact=q_search) |
            Q(phone__icontains=q_search) |
            Q(order_id__icontains=q_search)
        )

    if q_status:
        orders = orders.filter(status=q_status)

    if q_purchase:
        orders = orders.filter(date=q_purchase)

    if q_due:
        orders = orders.filter(due_date=q_due)

    paginator = Paginator(orders, 10)  # 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "all_orders.html", {"orders": page_obj,"page_obj":page_obj})

@login_required(login_url='/')
def update_order_status(request, order_id):
    if request.method == "POST":
        order = TableOrders.objects.get(id=order_id)
        order.status = request.POST.get("status")
        order.save()
    return redirect("all_orders")

@login_required(login_url='/')
def export_orders_csv(request):
    orders = TableOrders.objects.all().order_by("-id")

    q_search = request.GET.get('search_general')
    q_status = request.GET.get('status')
    q_purchase = request.GET.get('purchase_date')
    q_due = request.GET.get('due_date')

    if q_search:
        orders = orders.filter(
            Q(name__icontains=q_search) |
            Q(customer_id__iexact=q_search) |
            Q(phone__icontains=q_search)
        )

    if q_status:
        orders = orders.filter(status=q_status)

    if q_purchase:
        orders = orders.filter(date=q_purchase)

    if q_due:
        orders = orders.filter(due_date=q_due)

    today = datetime.date.today().strftime('%Y-%m-%d')
    order_file = f"orders_{today}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={order_file}'
    writer = csv.writer(response)
    writer.writerow(["Customer ID","Order ID","Order Date","Due Date","Customer", "Email", "Phone Number", "Address", "Item", "Lining",
                    "Bottom", "Locking", "Pattern", "Sareefall Type", "Stitching Charge", "Additional Charge",
                    "Total","Advance Paid", "Balance to Pay", "Notes", "Order Status"])

    for i in orders:
        writer.writerow(
            [
                i.customer_id,
                i.order_id,
                i.date,
                i.due_date,
                i.name,
                i.email,
                i.phone,
                i.address,
                i.item,
                i.lining,
                i.bottom,
                i.locking,
                i.pattern,
                i.sareefall_type,
                i.stitching_charges,
                i.additional_charges,
                i.total,
                i.advance_paid,
                i.balance,
                i.notes,
                i.status,
            ]
        )
    return response

@login_required(login_url='/')
def ongoing_orders(request):
    orders = TableOrders.objects.filter(status="Ordered").order_by("-id")
    order_count = orders.count()
    money = orders.aggregate(
        total_sum=Sum("total"),
        advance_sum=Sum("advance_paid"),
        balance_sum=Sum("balance")
    )
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "ongoing_orders.html", {"orders": page_obj, "page_obj":page_obj,
                                                   "order_count":order_count,"total":money["total_sum"] or 0,
                                                   "advance": money["advance_sum"] or 0,
                                                   "balance": money["balance_sum"] or 0,})

@login_required(login_url='/')
def stock(request):
    sto = TableStock.objects.all().order_by("-id")
    q_search = request.GET.get('search_item')
    if q_search:
        sto = sto.filter(item__icontains=q_search)

    paginator = Paginator(sto, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "stock.html",{"sto": page_obj, "page_obj":page_obj})

@login_required(login_url='/')
def export_stock_csv(request):
    sto = TableStock.objects.all().order_by("-id")
    q_search = request.GET.get('search_item')
    if q_search:
        sto = sto.filter(item__icontains=q_search)

    today = datetime.date.today().strftime('%Y-%m-%d')
    order_file = f"stock_{today}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={order_file}'
    writer = csv.writer(response)
    writer.writerow(
        [
            "ITEM","STOCK","UNIT","LOW STOCK THRESHOLD","NOTES"
        ])

    for i in sto:
        writer.writerow(
            [
                i.item,
                i.stock,
                i.unit,
                i.low_stock,
                i.notes
            ]
        )
    return response

@login_required(login_url='/')
def add_stock(request):
        return render(request, "add_stock.html")

@login_required(login_url='/')
def save_stock(request):
    if request.method == "POST":
        item = request.POST.get("item")
        stock = request.POST.get("stock")
        unit = request.POST.get("unit")
        low_stock = request.POST.get("low_stock")
        notes = request.POST.get("notes")
        TableStock.objects.create(item=item, stock=stock, unit=unit, notes=notes, low_stock=low_stock)
        return redirect("stock")
    return redirect("stock")

@login_required(login_url='/')
def edit_stock(request, stock_id):
    sto = TableStock.objects.get(id=stock_id)
    return render(request, "edit_stock.html", {"sto": sto})

@login_required(login_url='/')
def update_stock(request, stock_id):
    if request.method == "POST":
        item = request.POST.get("item")
        stock = request.POST.get("stock")
        unit = request.POST.get("unit")
        low_stock = request.POST.get("low_stock")
        notes = request.POST.get("notes")

        tab_obj = TableStock.objects.get(id=stock_id)
        tab_obj.item = item
        tab_obj.stock = stock
        tab_obj.unit = unit
        tab_obj.low_stock = low_stock
        tab_obj.notes = notes
        tab_obj.save()
        return redirect("stock")
    return redirect("stock")

@login_required(login_url='/')
def delete_stock(request, stock_id):
    tab_obj = TableStock.objects.get(id=stock_id)
    tab_obj.delete()
    return redirect("stock")

@login_required(login_url='/')
def used_stock(request, stock_id):
    sto = TableStock.objects.get(id=stock_id)
    return render(request, "used_stock.html", {"sto": sto})

@login_required(login_url='/')
def save_used_stock(request, stock_id):
    if request.method == "POST":
        used_stock = float(request.POST.get("used_stock"))
        tab_obj = TableStock.objects.get(id=stock_id)
        tab_obj.stock = tab_obj.stock - used_stock
        tab_obj.save()
        return redirect("stock")
    return redirect("stock")

@login_required(login_url='/')
def invoice(request, inv_id):
    data = TableOrders.objects.get(id=inv_id)
    return render(request, "invoice.html", {"data": data})

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect

def login_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "login.html")

def check_signin(request):
    if request.method == "POST":
        username = request.POST.get("user_name", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}")
            return redirect("index")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("/")
    return redirect("/")

def sign_out(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/')
def profile(request):
    return render(request, "profile.html")

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required(login_url="/")
def profile_settings(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.username = request.POST.get("username", "").strip()
        user.email = request.POST.get("email", "").strip()

        new_password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if new_password:
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters.")
                return redirect("profile")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("profile")

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "profile.html", {"user": user})
