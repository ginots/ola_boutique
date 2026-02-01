import csv
import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from client_app.models import TableOrders


# Create your views here.

def new_order(request, cust_id):
    data = TableCustomer.objects.get(id=cust_id)
    return render(request,"new_order.html",{"data":data})

def save_order(request):
    if request.method == "POST":
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

        TableOrders.objects.create( customer_id=customer_id,name=name,phone=phone,
                                    email=email, address=address,cloth_type=cloth_type,
                                   item=item, lining=lining, bottom=bottom,
                                   locking=locking, pattern=pattern, sareefall_type=sareefall_type,
                                   image=image, due_date=due_date, notes=notes,
                                    stitching_charges=stitching_charges, additional_charges=additional_charges,
                                    total=total, advance_paid=advance_paid,balance=balance,
                                    status=status)

        return redirect("all_orders")

from django.db.models import Q

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
            Q(phone__icontains=q_search)
        )

    if q_status:
        orders = orders.filter(status=q_status)

    if q_purchase:
        orders = orders.filter(date=q_purchase)

    if q_due:
        orders = orders.filter(due_date=q_due)

    return render(request, "all_orders.html", {"orders": orders})


def update_order_status(request, order_id):
    if request.method == "POST":
        order = TableOrders.objects.get(id=order_id)
        order.status = request.POST.get("status")
        order.save()
    return redirect("all_orders")

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
    writer.writerow(["Customer ID","Order Date","Due Date","Customer", "Email", "Phone Number", "Address", "Item", "Lining",
                    "Bottom", "Locking", "Pattern", "Sareefall Type", "Stitching Charge", "Additional Charge",
                    "Total","Advance Paid", "Balance to Pay", "Notes", "Order Status"])

    for i in orders:
        writer.writerow(
            [
                i.customer_id,
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

def ongoing_orders(request):
    orders = TableOrders.objects.filter(status="Ordered").order_by("-id")
    return render(request, "ongoing_orders.html", {"orders": orders})
