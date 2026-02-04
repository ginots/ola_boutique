import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import *


# Create your views here.


def customers(request):
    cust=TableCustomer.objects.all().order_by("-id")
    q_searched=request.GET.get("search_general")

    if q_searched:
        cust=cust.filter(Q(name__icontains=q_searched)|
                         Q(custid__iexact=q_searched)|
                         Q(email__icontains=q_searched)|
                         Q(phone__icontains=q_searched))
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
    chd=TableChuridar.objects.all().order_by("-id")
    sar=TableSaree.objects.all().order_by("-id")

    search_chd=request.GET.get("search_chd")
    search_sar=request.GET.get("search_sar")

    if search_chd:
        chd = chd.filter(
            Q(customer__name__icontains=search_chd) |
            Q(customer__custid__icontains=search_chd) |
            Q(customer__email__icontains=search_chd) |
            Q(customer__phone__icontains=search_chd)
        ).distinct()

    if search_sar:
        sar = sar.filter(
            Q(customer__name__icontains=search_sar) |
            Q(customer__custid__icontains=search_sar) |
            Q(customer__email__icontains=search_sar) |
            Q(customer__phone__icontains=search_sar)
        ).distinct()

    return render(request,"measurements.html",{"chd":chd,"sar":sar})

def add_churidar_measurement(request,cust_id):
    cust=TableCustomer.objects.get(id=cust_id)
    return render(request,"add_churidar_measurement.html",{"cust":cust})

def save_ch_measure(request):
    if request.method=="POST":
        cid= request.POST.get("customer_id")

        customer= TableCustomer.objects.get(id=cid)

        tab_chd=TableChuridar()
        tab_chd.customer=customer
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

def edit_chmeasure(request,cust_id):
    data=TableChuridar.objects.get(id=cust_id)
    return render(request,"edit_chmeasure.html",{"data":data})

def update_ch_measure(request,cust_id):
    if request.method=="POST":

        tab_chd=TableChuridar.objects.get(id=cust_id)
        tab_chd.flength = request.POST.get("flength")
        tab_chd.point = request.POST.get("point")
        tab_chd.tuck = request.POST.get("tuck")
        tab_chd.yoke = request.POST.get("yoke")
        tab_chd.pw = request.POST.get("pw")
        tab_chd.slit = request.POST.get("slit")
        tab_chd.shoulder = request.POST.get("shoulder")
        tab_chd.sl = request.POST.get("sl")
        tab_chd.sr = request.POST.get("sr")
        tab_chd.muscle = request.POST.get("muscle")
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
        tab_chd.neckw = request.POST.get("neckw")
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

def delete_chmeasure(request,cust_id):
    data=TableChuridar.objects.get(id=cust_id)
    data.delete()
    return redirect("/measurements/")

def add_saree_measurement(request,cust_id):
    cust=TableCustomer.objects.get(id=cust_id)
    return render(request,"add_saree_measurement.html",{"cust":cust})

def save_sr_measure(request):
    if request.method == "POST":
        cid=request.POST.get("customer_id")
        customer = TableCustomer.objects.get(id=cid)
        tab_sr = TableSaree()
        tab_sr.customer= customer
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

def edit_srmeasure(request,cust_id):
    data=TableSaree.objects.get(id=cust_id)
    return render(request,"edit_srmeasure.html",{"data":data})

def update_sr_measure(request,cust_id):
    if request.method=="POST":

        tab_sr=TableSaree.objects.get(id=cust_id)
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

def delete_srmeasure(request,cust_id):
    data=TableSaree.objects.get(id=cust_id)
    data.delete()
    return redirect("/measurements/")


def export_churidar_csv(request):
    search = request.GET.get("search_chd", "").strip()

    qs = TableChuridar.objects.select_related("customer")

    if search:
        qs = qs.filter(
            Q(customer__name__icontains=search) |
            Q(customer__custid__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(customer__phone__icontains=search)
        ).distinct()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="churidar_measurements.csv"'

    writer = csv.writer(response)

    # 🔹 HEADER
    writer.writerow([
        "Customer Name", "Customer ID",
        "Full Length", "Point", "Tuck", "Yoke", "PW", "Slit",
        "Shoulder", "Sleeve Length", "Sleeve Round",
        "Muscle", "Arm Hole", "Arm Pit F", "Arm Pit B",
        "Chest", "Bust", "Waist", "Hip", "Seat",
        "Neck F", "Neck B", "Neck W",
        "Bottom Waist", "Length", "Width",
        "Knee L", "Knee R", "Thigh L", "Thigh R", "Down Flare"
    ])

    # 🔹 DATA
    for i in qs:
        writer.writerow([
            i.customer.name, i.customer.custid,
            i.flength, i.point, i.tuck, i.yoke, i.pw, i.slit,
            i.shoulder, i.sl, i.sr,
            i.muscle, i.ah, i.apf, i.apb,
            i.chest, i.bust, i.waist1, i.hip, i.seat,
            i.neckf, i.neckb, i.neckw,
            i.waist2, i.length, i.width,
            i.kneel, i.kneer, i.thighl, i.thighr, i.downf
        ])

    return response


def export_saree_csv(request):
    search = request.GET.get("search_sar", "").strip()

    qs = TableSaree.objects.select_related("customer")

    if search:
        qs = qs.filter(
            Q(customer__name__icontains=search) |
            Q(customer__custid__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(customer__phone__icontains=search)
        ).distinct()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="saree_measurements.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Customer Name", "Customer ID",
        "Full Length", "Point", "Tuck", "PW", "Shoulder",
        "Sleeve Length", "Sleeve Round", "Muscle",
        "Arm Hole", "Armpit F", "Armpit B",
        "Chest", "Bust", "Waist",
        "Neck F", "Neck B", "Neck W",
        "Underskirt Waist", "Length", "Down Width",
        "Knee L", "Knee R", "Seat",
        "RTW Waist", "RTW Length", "Pallu"
    ])

    for i in qs:
        writer.writerow([
            i.customer.name, i.customer.custid,
            i.flength, i.point, i.tuck, i.pw, i.shoulder,
            i.sl, i.sr, i.muscle,
            i.ah, i.apf, i.apb,
            i.chest, i.bust, i.waist1,
            i.neckf, i.neckb, i.neckw,
            i.waist2, i.length1, i.dwidth,
            i.kneel, i.kneer, i.seat,
            i.waist3, i.length2, i.pallu
        ])

    return response

def staff_details(request):
    staff=TableStaffs.objects.all()
    return render(request,"staff_details.html",{"staff":staff})

def add_staff(request):
    return render(request,"add_staff.html")

def save_staff(request):
    if request.method=="POST":
        tab_stf=TableStaffs()
        tab_stf.name=request.POST.get("name")
        tab_stf.phone=request.POST.get("phone")
        tab_stf.role=request.POST.get("role")
        tab_stf.email=request.POST.get("email")
        tab_stf.address=request.POST.get("address")
        tab_stf.status=request.POST.get("status")
        tab_stf.save()
        return redirect("/staff_details/")