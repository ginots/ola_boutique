from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def customers(request):
    return render(request,"customers.html")

def add_customer(request):
    return render(request,"add_customer.html")