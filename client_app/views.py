import csv
from datetime import date, datetime
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import *


# Create your views here.
def index(request):
    return render(request,"index.html")

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
        tab_stf.monthly_salary=request.POST.get("salary")
        tab_stf.status="active"
        tab_stf.save()
        return redirect("/staff_details/")

def edit_staff(request,stf_id):
    data=TableStaffs.objects.get(id=stf_id)
    return render(request,"edit_staff.html",{"data":data})

def update_staff(request,stf_id):
    if request.method == "POST":
        tab_stf = TableStaffs.objects.get(id=stf_id)
        tab_stf.name = request.POST.get("name")
        tab_stf.phone = request.POST.get("phone")
        tab_stf.role = request.POST.get("role")
        tab_stf.email = request.POST.get("email")
        tab_stf.address = request.POST.get("address")
        tab_stf.monthly_salary=request.POST.get("salary")
        tab_stf.save()
        return redirect("/staff_details/")

def staff_emp(request):
    data=TableStaffs.objects.all().order_by("-id")
    return render(request,"staff_emp.html",{"data":data})

def update_emp(request):
    if request.method=="POST":
        name= request.POST.get("name")
        status=request.POST.get("status")

        tab_stf=TableStaffs.objects.get(id=name)
        tab_stf.status=status
        tab_stf.save()
        return redirect("/staff_details/")


def salary_status(request):

    latest_salary = TableSalary.objects.order_by("-date").first()

    if latest_salary:
        month = latest_salary.date.month
        year = latest_salary.date.year

        sal = TableSalary.objects.filter(
            date__month=month,
            date__year=year
        ).order_by("-id")

    else:
        sal = TableSalary.objects.none()

    return render(request, "salary_status.html", {"sal": sal})


def salary_generate(request):
    return render(request,"salary_generate.html")



def generate_salary(request):

    if request.method == "POST":

        salary_date = request.POST.get("date")

        if not salary_date:
            messages.warning(request, "Please select a date.")
            return redirect("/salary_status/")

        from datetime import datetime

        salary_date = datetime.strptime(salary_date, "%Y-%m-%d")

        month = salary_date.month
        year = salary_date.year
        day= salary_date.day

        if not month or not year:
            messages.warning(request, "Please select month and year.")
            return redirect("/salary_status/")

        month = int(month)
        year = int(year)
        day=int(day)



        already_exists = TableSalary.objects.filter(
            date__month=month,
            date__year=year,
            date__day=day
        ).exists()

        if already_exists:
            messages.warning(request, "Salary already generated for this month.")
            return redirect("/salary_status/")

        staffs = TableStaffs.objects.filter(status__iexact="active")

        for staff in staffs:

            TableSalary.objects.create(
                staff=staff,
                date=date(year, month, day),
                fixed_salary=staff.monthly_salary,
                total_overtime=0,
                total_salary=staff.monthly_salary,
                status="paid"
            )

        messages.success(request, "Salary generated successfully.")
        return redirect("/salary_status/")

def delete_salary(request):

    if request.method == "POST":

        salary_month = request.POST.get("month")

        if not salary_month:
            messages.warning(request, "Please select a date.")
            return redirect("/salary_status/")

        salary_date = datetime.strptime(salary_month, "%Y-%m")

        month = salary_date.month
        year = salary_date.year

        salaries = TableSalary.objects.filter(
            date__month=month,
            date__year=year
        )

        if not salaries.exists():
            messages.warning(request, "No salary found for this month.")
            return redirect("/salary_status/")

        salaries.delete()

        messages.success(request, "Salary deleted successfully.")
        return redirect("/salary_status/")


def save_salary(request):
    if request.method=="POST":
        staff = request.POST.get("staff_id")
        staff_obj = TableStaffs.objects.get(id=staff)
        paymentdate = request.POST.get("date") or None
        fixed_salary = float(request.POST.get("salary") or 0)
        status=request.POST.get("status")
        tab_sal=TableSalary()
        tab_sal.staff=staff_obj
        tab_sal.date=paymentdate
        tab_sal.fixed_salary=fixed_salary
        tab_sal.total_salary=fixed_salary
        tab_sal.status=status
        tab_sal.save()
        return redirect("/salary_status/")

def toggle_salary_status(request, sal_id):
    if request.method == "POST":
        salary = TableSalary.objects.get(id=sal_id)

        if salary.status == "paid":
            salary.status = "pending"
        else:
            salary.status = "paid"

        salary.save()

    return redirect("/salary_status/")


def add_overtime(request,sal_id):
    data=TableSalary.objects.get(id=sal_id)
    return render(request,"add_overtime.html",{"data":data})

def save_overtime(request):
    if request.method == "POST":

        salary_id = request.POST.get("salary_id")
        salary_obj = TableSalary.objects.get(id=salary_id)

        staff_obj = salary_obj.staff

        ot_date = request.POST.get("ot_date")
        ot_hours = float(request.POST.get("ot_hours") or 0)
        ot_rate = float(request.POST.get("ot_amount") or 0)
        ot_status = request.POST.get("ot_status")

        # Calculate OT payment
        ot_pay = ot_hours * ot_rate

        # ---- Save overtime record ----
        tab_ot=TableOvertime()
        tab_ot.staff=staff_obj
        tab_ot.salary=salary_obj
        tab_ot.ot_date=ot_date
        tab_ot.extra_hours=ot_hours
        tab_ot.ot_amount=ot_rate
        tab_ot.status=ot_status
        tab_ot.save()

        salary_obj.total_overtime += ot_pay
        salary_obj.total_salary = salary_obj.fixed_salary + salary_obj.total_overtime
        salary_obj.save()

        return redirect("/salary_status/")


def delete_overtime(request, sal_id):

    salary = TableSalary.objects.get(id=sal_id)

    overtime_records = TableOvertime.objects.filter(salary=salary)

    if not overtime_records.exists():
        messages.warning(request, "No overtime found.")
        return redirect("/salary_status/")

    # delete overtime records
    overtime_records.delete()

    # reset salary overtime values
    salary.total_overtime = 0
    salary.total_salary = salary.fixed_salary
    salary.save()

    messages.success(request, "Overtime deleted successfully.")

    return redirect("/salary_status/")


def edit_salary_status(request,stf_id):
    if request.method == "POST":
        salary = TableSalary.objects.get(id=stf_id)
        salary.status = request.POST.get("status")
        salary.save()
        return redirect("/salary_status/")

def get_overtime_details(request, salary_id):

    overtime_records = TableOvertime.objects.filter(
        salary_id=salary_id
    ).order_by("ot_date")

    data = []

    for ot in overtime_records:
        data.append({
            "date": ot.ot_date.strftime("%Y-%m-%d") if ot.ot_date else "N/A",
            "hours": ot.extra_hours or 0
        })

    return JsonResponse(data, safe=False)

from django.db.models import Q

def salary_history(request):

    data = TableSalary.objects.all().order_by("-id")

    search_staff = request.GET.get("search_staff")
    search_status = request.GET.get("search_status")
    search_month = request.GET.get("search_month")


    # 🔍 Staff search
    if search_staff:
        data = data.filter(
            Q(staff__staffid__icontains=search_staff) |
            Q(staff__name__icontains=search_staff)
        )

    # 🔍 Status filter
    if search_status:
        data = data.filter(status=search_status)

    # 🔍 Month filter (IMPORTANT FIX)
    if search_month:
        data = data.filter(date__startswith=search_month)

    return render(request, "salary_history.html", {"data": data})


def export_salary_csv(request):

    data = TableSalary.objects.all().order_by("-id")

    search_staff = request.GET.get("search_staff")
    search_status = request.GET.get("search_status")
    search_month = request.GET.get("search_month")

    # Apply filters
    if search_staff:
        data = data.filter(
            Q(staff__staffid__icontains=search_staff) |
            Q(staff__name__icontains=search_staff)
        )

    if search_status:
        data = data.filter(status=search_status)

    if search_month:
        try:
            selected_date = datetime.strptime(search_month, "%Y-%m")
            data = data.filter(
                date__year=selected_date.year,
                date__month=selected_date.month
            )
        except:
            pass

    # ✅ Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="salary_history.csv"'

    writer = csv.writer(response)

    # Header row
    writer.writerow([
        "Staff ID",
        "Staff Name",
        "Date",
        "Fixed Salary",
        "Overtime",
        "Total Salary",
        "Status"
    ])

    # Data rows
    for row in data:
        writer.writerow([
            row.staff.staffid if row.staff else "",
            row.staff.name if row.staff else "",
            row.date,
            row.fixed_salary,
            row.total_overtime,
            row.total_salary,
            row.status
        ])

    return response


