from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def index(request):
    return render(request,"index.html")

def customers(request):
    cust=TableCustomer.objects.all()
    return render(request,"customers.html",{"cust":cust})

def add_customer(request):
    return render(request,"add_customer.html")

def save_customer(request):

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")

        tab_cust=TableCustomer()
        tab_cust.name=name
        tab_cust.phone=phone
        tab_cust.email=email
        tab_cust.address=address
        tab_cust.save()
        return redirect("/customers/")

def edit_customer(request,cust_id):
    data=TableCustomer.objects.get(id=cust_id)
    return render(request,"edit_customer.html",{"data":data})

def update_customer(request,cust_id):
    if request.method == "POST":
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")

        tab_cust=TableCustomer.objects.get(id=cust_id)
        tab_cust.name=name
        tab_cust.phone=phone
        tab_cust.email=email
        tab_cust.address=address
        tab_cust.save()
        return redirect("/customers/")

def delete_customer(request,cust_id):
    data=TableCustomer.objects.get(id=cust_id)
    data.delete()
    return redirect("/customers/")


def measurements(request):
    chd=TableChuridar.objects.all()
    sar=TableSaree.objects.all()
    return render(request,"measurements.html",{"chd":chd,"sar":sar})

def add_churidar_measurement(request,cust_id):
    cust=TableCustomer.objects.get(id=cust_id)
    return render(request,"add_churidar_measurement.html",{"cust":cust})

def save_ch_measure(request):
    if request.method=="POST":

        customer_name= request.POST.get("customer_name")
        tab_chd=TableChuridar()
        tab_chd.customer_name=customer_name
        tab_chd.flength = request.POST.get("flength")
        tab_chd.point =request.POST.get("point")
        tab_chd.tuck = request.POST.get("tuck")
        tab_chd.yoke = request.POST.get("yoke")
        tab_chd.pw = request.POST.get("pw")
        tab_chd.slit = request.POST.get("slit")
        tab_chd.shoulder = request.POST.get("shoulder")
        tab_chd.sl = request.POST.get("sl")
        tab_chd.sr = request.POST.get("sr")
        tab_chd.muscle =request.POST.get("muscle")
        tab_chd.ah = request.POST.get("ah")
        tab_chd.apf = request.POST.get("armf")
        tab_chd.apb = request.POST.get("armb")
        tab_chd.chest = request.POST.get("chest")
        tab_chd.bust = request.POST.get("bust")
        tab_chd.waist1 = request.POST.get("waist1")
        tab_chd.hip = request.POST.get("hip")
        tab_chd.seat = request.POST.get("seat")
        tab_chd.neckf = request.POST.get("neckf")
        tab_chd.neckb = request.POST.get("neckb")
        tab_chd.neckw =request.POST.get("neckw")
        tab_chd.waist2 = request.POST.get("waist2")
        tab_chd.length = request.POST.get("length")
        tab_chd.width = request.POST.get("width")
        tab_chd.kneel = request.POST.get("kneel")
        tab_chd.kneer = request.POST.get("kneer")
        tab_chd.thighl = request.POST.get("thl")
        tab_chd.thighr = request.POST.get("thr")
        tab_chd.downf = request.POST.get("dfl")
        tab_chd.save()
        return redirect("/measurements/")


def add_saree_measurement(request,cust_id):
    cust=TableCustomer.objects.get(id=cust_id)
    return render(request,"add_saree_measurement.html",{"cust":cust})

def save_sr_measure(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        tab_sr = TableSaree()
        tab_sr.customer_name = customer_name
        tab_sr.flength = request.POST.get("flength")
        tab_sr.point = request.POST.get("point")
        tab_sr.tuck = request.POST.get("tuck")
        tab_sr.pw = request.POST.get("pw")
        tab_sr.shoulder = request.POST.get("shoulder")
        tab_sr.sl = request.POST.get("sl")
        tab_sr.sr = request.POST.get("sr")
        tab_sr.muscle = request.POST.get("muscle")
        tab_sr.ah = request.POST.get("ah")
        tab_sr.apf = request.POST.get("armf")
        tab_sr.apb = request.POST.get("armb")
        tab_sr.chest = request.POST.get("chest")
        tab_sr.bust = request.POST.get("bust")
        tab_sr.waist1 = request.POST.get("waist1")
        tab_sr.neckf = request.POST.get("neckf")
        tab_sr.neckb = request.POST.get("neckb")
        tab_sr.neckw = request.POST.get("neckw")
        tab_sr.waist2 = request.POST.get("waist2")
        tab_sr.length1 = request.POST.get("length1")
        tab_sr.dwidth = request.POST.get("dwidth")
        tab_sr.kneel = request.POST.get("kneel")
        tab_sr.kneer = request.POST.get("kneer")
        tab_sr.seat = request.POST.get("seat")
        tab_sr.waist3 = request.POST.get("waist3")
        tab_sr.length2 = request.POST.get("length2")
        tab_sr.pallu = request.POST.get("pallu")
        tab_sr.save()
        return redirect("/measurements/")

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

def all_orders(request):
    orders = TableOrders.objects.all().order_by("-id")
    return render(request,"all_orders.html", {"orders":orders})

def update_order_status(request, order_id):
    if request.method == "POST":
        order = TableOrders.objects.get(id=order_id)
        order.status = request.POST.get("status")
        order.save()
    return redirect("all_orders")

