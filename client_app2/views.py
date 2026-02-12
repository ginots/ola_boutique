import csv
import datetime
from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders

from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

from client_app.models import TableOrders,TableCustomer,TableOrderImage, TableChuridar, TableSaree

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
        cloth_details = request.POST.get("cloth_from")
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
        images = request.FILES.getlist("images")
        date = request.POST.get("date")
        due_date = request.POST.get("due_date")
        stitching_charges = float(request.POST.get("stitching_charges") or 0)
        additional_charges = float(request.POST.get("additional_charges") or 0)
        total = round(stitching_charges + additional_charges, 2)
        advance_paid = float(request.POST.get("advance_paid") or 0)
        balance = round(total - advance_paid, 2)
        notes = request.POST.get("notes")
        status = "Ordered"

        order = TableOrders.objects.create( customer_id=customer_id, order_id=order_id, name=name,phone=phone,
                                    email=email, address=address,cloth_type=cloth_type, cloth_details=cloth_details,
                                   item=item, lining=lining, bottom=bottom,
                                   locking=locking, pattern=pattern, sareefall_type=sareefall_type,
                                   due_date=due_date, notes=notes, date=date,
                                    stitching_charges=stitching_charges, additional_charges=additional_charges,
                                    total=total, advance_paid=advance_paid,balance=balance,
                                    status=status)
        for img in images:
            TableOrderImage.objects.create(order=order, image=img)

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
def update_ongoing_status(request, order_id):
    if request.method == "POST":
        order = TableOrders.objects.get(id=order_id)
        order.status = request.POST.get("status")
        order.save()
    return redirect("ongoing_orders")

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

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "profile.html", {"user": user})

@login_required(login_url='/')
def update_password(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST.get("old_password", "")
        new_password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("profile")

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
            messages.success(request, "Password updated successfully.")
            return redirect("profile")

        return render(request, "profile.html", {"user": user})


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import pdfkit
from django.conf import settings
import os
# from .models import TableOrders, TableCustomer, TableChuridar, TableSaree

# WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# pdf_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

from django.conf import settings
import pdfkit

pdf_config = pdfkit.configuration(
    wkhtmltopdf=settings.WKHTMLTOPDF_PATH
)
@login_required(login_url='/')
def invoice_pdf(request, pk):
    order = get_object_or_404(TableOrders, pk=pk)
    customer = get_object_or_404(TableCustomer, custid=order.customer_id)


    churidar = None
    saree = None

    if order.cloth_type == "1":
        churidar = TableChuridar.objects.filter(customer=customer).last()

    if order.cloth_type == "2":
        saree = TableSaree.objects.filter(customer=customer).last()

    measurement = churidar or saree
    if not measurement:
        measurement = None

    items = []
    linings = []
    bottoms = []
    lockings = []
    patterns = []

    if order.item:
        items = [i.strip() for i in order.item.split(",")]

    if order.lining:
        linings = [i.strip() for i in order.lining.split(",")]

    if order.bottom:
        bottoms = [i.strip() for i in order.bottom.split(",")]

    if order.locking:
        lockings = [i.strip() for i in order.locking.split(",")]

    if order.pattern:
        patterns = [i.strip() for i in order.pattern.split(",")]

    image_paths = []
    for img in order.images.all():
        image_paths.append(
            os.path.join(settings.MEDIA_ROOT, img.image.name)
        )

    lady_path = finders.find("img/lady__outline.jpg")
    logo_path = finders.find("img/logo.jpg")

    context = {
        "order": order,
        "customer": customer,
        "measurement": measurement,
        "items": items,
        "linings": linings,
        "bottoms": bottoms,
        "lockings": lockings,
        "patterns": patterns,
        # "logo_path": os.path.join(settings.STATIC_ROOT, "img/logo.jpg"),
        # "lady_path": os.path.join(settings.STATIC_ROOT, "img/lady__outline.jpg"),
        "logo_path": logo_path,
        "lady_path": lady_path,
        "order_images": image_paths,
    }

    # Render HTML
    html = render_to_string("invoice_pdf.html", context)

    # PDF options (important for layout)
    options = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "margin-top": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
        "margin-right": "10mm",
        "enable-local-file-access": "",
    }

    pdf = pdfkit.from_string(
        html,
        False,
        configuration=pdf_config,
        options=options
    )

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{order.order_id}.pdf"'
    )

    return response

@login_required(login_url='/')
def account_type_adm(request):
    """List all account types + create new"""
    account_types = Account_type.objects.all().order_by('id')

    if request.method == "POST":
        atype = request.POST.get("account_type")
        if atype:
            Account_type.objects.create(account_type=atype)
            messages.success(request, "Account type added successfully!")
            return redirect('account_type_adm')
        else:
            messages.warning(request, "Account type cannot be empty.")

    return render(request, "account_type_adm.html", {
        "account_types": account_types,
    })

@login_required(login_url='/')
def edit_account_type_adm(request, id):
    """Edit existing account type"""
    account_type = get_object_or_404(Account_type, id=id)

    if request.method == "POST":
        new_name = request.POST.get("account_type")
        if new_name:
            account_type.account_type = new_name
            account_type.save()
            messages.success(request, "Account type updated successfully!")
            return redirect('account_type_adm')
        else:
            messages.warning(request, "Account type cannot be empty.")

    return render(request, "edit_account_type_adm.html", {
        "account_type": account_type,
    })

@login_required(login_url='/')
def delete_account_type_adm(request, id):
    """Delete account type"""
    account_type = get_object_or_404(Account_type, id=id)
    account_type.delete()
    messages.success(request, "Account type deleted successfully!")
    return redirect('account_type_adm')

@login_required(login_url='/')
def account_br_adm(request):
    """List, search, paginate, and add new Accounts"""
    # gtg = Branches.objects.get(id = id)
    query = request.GET.get("q", "")
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 10)

    # accounts = Account.objects.filter(acount_brch=gtg).order_by("id")
    accounts = Account.objects.all().order_by("id")
    if query:
        accounts = accounts.filter(
            Q(name__icontains=query) |
            Q(acount_type__account_type__icontains=query)
        )

    paginator = Paginator(accounts, per_page)  # 10 per page
    page_obj = paginator.get_page(page_number)

    account_types = Account_type.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        balance = request.POST.get("balance", 0)
        updated_balance = request.POST.get("updated_balance", balance)
        account_type_id = request.POST.get("acount_type")
        account_type_id = int(account_type_id)
        bb = Account_type.objects.get(id = account_type_id)

        if name and account_type_id:
            if Account.objects.filter(acount_type = bb,name = name).exists():
                messages.success(request, "Account already exists!")
                # redd = '/account_br_adm/' + str(gtg.id)
                # return redirect(redd)
                return redirect("account_br_adm")
            Account.objects.create(
                name=name,
                balance=balance,
                updated_balance = updated_balance,
                acount_type_id=account_type_id,
                # acount_brch_id = gtg.id
            )
            messages.success(request, "Account added successfully!")
            # redd = '/account_br_adm/'+str(gtg.id)
            # return redirect(redd)
            return redirect("account_br_adm")
        else:
            messages.warning(request, "All fields are required.")

    context = {
        "page_obj": page_obj,
        "query": query,
        "account_types": account_types,
        # "branches": branches,
        # 'gtg': gtg,
        "per_page": int(per_page),
    }
    return render(request, "account_br_adm.html", context)

@login_required(login_url='/')
def edit_account_adm(request, id):
    acc = get_object_or_404(Account, id=id)
    # gbg = int(acc.id)
    if request.method == 'POST':
        name = request.POST['name']
        # balance = request.POST['balance']
        acount_type_id = request.POST['acount_type']
        bb = Account_type.objects.get(id = acount_type_id)
        # gtg = Branches.objects.get(id = request.session['branch_admin'])
        if Account.objects.filter(acount_type = bb, name=name).exclude(id = id).exists():
            messages.success(request, "Account already exists!")
            # redd = '/account_br_adm/' + str(gtg.id)
            # return redirect(redd)
            return redirect("account_br_adm")
        acc.name = name
        # acc.balance = balance
        acc.acount_type = bb
        acc.save()
        return redirect('account_br_adm')
    return redirect('account_br_adm')

@login_required(login_url='/')
def delete_account_adm(request, id):
    account = get_object_or_404(Account, id=id)
    account.delete()
    messages.success(request, "Account deleted successfully.")
    return redirect('account_br_adm')

from django.db import transaction as db_transaction
@login_required(login_url='/')
def transaction_br_adm(request):
    """List, search, paginate, add, edit, and delete Transactions"""
    # branch = get_object_or_404(Branches, id=id)
    query = request.GET.get("q", "")
    page_number = request.GET.get("page", 1)

    transactions = Transaction.objects.all().order_by("-date", "-id")

    if query:
        transactions = transactions.filter(
            Q(description__icontains=query) |
            Q(account__name__icontains=query) |
            Q(account__acount_type__account_type__icontains=query)
        )

    paginator = Paginator(transactions, 10)
    page_obj = paginator.get_page(page_number)

    accounts = Account.objects.all()

    # ============================
    # DELETE TRANSACTION
    # ============================
    if request.method == "POST" and request.POST.get("delete_id"):
        delete_id = request.POST.get("delete_id")
        delete_mode = request.POST.get("delete_mode", "no_effect")

        with db_transaction.atomic():
            transaction_obj = get_object_or_404(Transaction, id=delete_id)
            account = transaction_obj.account
            amount = transaction_obj.amount or Decimal('0.00')

            if delete_mode == "with_effect":
                if transaction_obj.transaction_type == 'debit':
                    Account.objects.filter(id=account.id).update(
                        updated_balance=F('updated_balance') - amount
                    )
                elif transaction_obj.transaction_type == 'credit':
                    Account.objects.filter(id=account.id).update(
                        updated_balance=F('updated_balance') + amount
                    )

            transaction_obj.delete()

        messages.success(
            request,
            "Transaction deleted and account balance updated!"
            if delete_mode == "with_effect"
            else "Transaction deleted (no effect on account)."
        )

        return redirect('transaction_br_adm')

    # ============================
    # ADD / EDIT TRANSACTION
    # ============================
    if request.method == "POST" and not request.POST.get("delete_id"):
        transaction_id = request.POST.get("transaction_id")
        description = request.POST.get("description")
        amount = Decimal(request.POST.get("amount", 0))
        account_id = request.POST.get("account")
        transaction_type = request.POST.get("transaction_type")

        if not all([amount, account_id, transaction_type]):
            messages.warning(request, "All fields are required.")
            return redirect('transaction_br_adm')

        account = get_object_or_404(Account, id=account_id)

        if transaction_id:  # EDIT EXISTING TRANSACTION
            transaction = get_object_or_404(Transaction, id=transaction_id)

            if (str(transaction.transaction_type) == str(transaction_type)) and (float(amount) == float(transaction.amount)):
                transaction.description = description
                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('transaction_br_adm')

            if (str(transaction.transaction_type) == str(transaction_type)) and (float(amount) != float(transaction.amount)):
                amt = float(transaction.amount) - float(amount)
                transaction.amount = Decimal(amount)
                if (str(transaction_type) == 'debit') and (amt > 0):
                    amt = Decimal(amt)
                    account.updated_balance -= amt
                if (str(transaction_type) == 'debit') and (amt < 0):
                    amt = abs(amt)
                    amt = Decimal(amt)
                    account.updated_balance += amt
                if (str(transaction_type) == 'credit') and (amt > 0):
                    amt = Decimal(amt)
                    account.updated_balance += amt
                if (str(transaction_type) == 'credit') and (amt < 0):
                    amt = abs(amt)
                    amt = Decimal(amt)
                    account.updated_balance -= amt
                account.save()
                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('transaction_br_adm')

            if (str(transaction.transaction_type) != str(transaction_type)) and (float(amount) == float(transaction.amount)):
                transaction.transaction_type = str(transaction_type)
                if str(transaction_type) == 'debit':
                    amount = abs(float(amount))
                    amount = amount + float(transaction.amount)
                    amount = Decimal(amount)
                    account.updated_balance += amount
                if str(transaction_type) == 'credit':
                    amount = abs(float(amount))
                    amount = amount + float(transaction.amount)
                    amount = Decimal(amount)
                    account.updated_balance -= amount
                account.save()
                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('transaction_br_adm')

            if (str(transaction.transaction_type) != str(transaction_type)) and (float(amount) != float(transaction.amount)):
                ammt = float(transaction.amount)
                transaction.transaction_type = str(transaction_type)
                transaction.amount = Decimal(amount)
                if str(transaction_type) == 'debit':
                    amt = float(ammt) + float(amount)
                    amount = Decimal(amt)
                    account.updated_balance += amount
                if str(transaction_type) == 'credit':
                    amt = float(ammt) + float(amount)
                    amount = Decimal(amt)
                    account.updated_balance -= amount
                account.save()
                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('transaction_br_adm')


        else:  # ADD NEW TRANSACTION
            new_transaction = Transaction.objects.create(
                description=description,
                amount=amount,
                account=account,
                transaction_type=transaction_type,
            )

            # Adjust balance for new transaction
            if transaction_type == 'debit':
                account.updated_balance += amount
            elif transaction_type == 'credit':
                account.updated_balance -= amount
            account.save()

            messages.success(request, "Transaction added successfully!")

        return redirect('transaction_br_adm')


    entries = request.GET.get("entries", 10)
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # Apply date filters
    if from_date:
        transactions = transactions.filter(date__gte=from_date)

    if to_date:
        transactions = transactions.filter(date__lte=to_date)

    # Pagination with dynamic entries
    paginator = Paginator(transactions, entries)
    page_obj = paginator.get_page(page_number)


    # ============================
    # RENDER PAGE
    # ============================
    context = {
        "accounts": accounts,
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "transaction_br_adm.html", context)

@login_required(login_url='/')
def ledger_br_adm(request):
    # branch = get_object_or_404(Branches, id=branch_id)

    account_id = request.GET.get("account")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    query = request.GET.get("q", "")
    entries = int(request.GET.get("entries", 25))

    accounts = Account.objects.all().order_by("-id")

    ledger_transactions = Transaction.objects.none()
    opening_balance = Decimal("0.00")
    selected_account = None

    if account_id:
        selected_account = get_object_or_404(Account, id=account_id)

        ledger_transactions = Transaction.objects.filter(
            account=selected_account
        ).order_by("date", "id")

        # ---- DATE FILTER ----
        if from_date:
            ledger_transactions = ledger_transactions.filter(date__gte=from_date)
        if to_date:
            ledger_transactions = ledger_transactions.filter(date__lte=to_date)

        # ---- SEARCH FILTER ----
        if query:
            ledger_transactions = ledger_transactions.filter(
                Q(description__icontains=query)
            )

        # ---- OPENING BALANCE ----
        opening_balance = selected_account.balance

        # ---- RUNNING BALANCE CALC ----
        running_total = opening_balance
        calculated = []

        for t in ledger_transactions:
            if t.transaction_type == "debit":
                running_total += t.amount
            else:
                running_total -= t.amount

            calculated.append({
                "date": t.date,
                "description": t.description,
                "debit": t.amount if t.transaction_type == "debit" else "",
                "credit": t.amount if t.transaction_type == "credit" else "",
                "balance": running_total
            })

        ledger_transactions = calculated

    # PAGINATION
    paginator = Paginator(ledger_transactions, entries)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "accounts": accounts,
        "page_obj": page_obj,
        "selected_account": selected_account,
        "opening_balance": opening_balance,
        "query": query,
        "from_date": from_date,
        "to_date": to_date,
        "entries": entries,

    }

    return render(request, "ledger_br_adm.html", context)

@login_required(login_url='/')
def export_ledger_csv(request):
    account_id = request.GET.get("account")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    query = request.GET.get("q", "")
    entries = int(request.GET.get("entries", 25))

    accounts = Account.objects.all().order_by("-id")

    ledger_transactions = Transaction.objects.none()
    opening_balance = Decimal("0.00")
    selected_account = None

    if account_id:
        selected_account = get_object_or_404(Account, id=account_id)

        ledger_transactions = Transaction.objects.filter(
            account=selected_account
        ).order_by("date", "id")

        # ---- DATE FILTER ----
        if from_date:
            ledger_transactions = ledger_transactions.filter(date__gte=from_date)
        if to_date:
            ledger_transactions = ledger_transactions.filter(date__lte=to_date)

        # ---- SEARCH FILTER ----
        if query:
            ledger_transactions = ledger_transactions.filter(
                Q(description__icontains=query)
            )

        # ---- OPENING BALANCE ----
        opening_balance = selected_account.balance

        # ---- RUNNING BALANCE CALC ----
        running_total = opening_balance
        calculated = []

        for t in ledger_transactions:
            if t.transaction_type == "debit":
                running_total += t.amount
            else:
                running_total -= t.amount

            calculated.append({
                "date": t.date,
                "description": t.description,
                "debit": t.amount if t.transaction_type == "debit" else "",
                "credit": t.amount if t.transaction_type == "credit" else "",
                "balance": running_total
            })

        ledger_transactions = calculated

    today = datetime.date.today().strftime('%Y-%m-%d')
    order_file = f"ledger_{today}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={order_file}'
    writer = csv.writer(response)
    writer.writerow(
        [
            "DATE","DESCRIPTION","DEBIT","CREDIT","BALANCE"
        ])

    for i in ledger_transactions:
        writer.writerow(
            [
                i["date"],
                i["description"],
                i["debit"],
                i["credit"],
                i["balance"],
            ]
        )
    return response
