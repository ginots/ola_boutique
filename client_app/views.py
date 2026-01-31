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

