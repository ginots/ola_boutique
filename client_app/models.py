from django.db import models

# Create your models here.



class TableCustomer(models.Model):
    custid = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(max_length=50, null=True)
    address = models.TextField(null=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.custid:
            self.custid = f"OLA{self.id}"
            super().save(update_fields=["custid"])


class TableChuridar(models.Model):
    customer=models.ForeignKey(TableCustomer,on_delete=models.CASCADE,null=True)
    flength=models.CharField(max_length=100,null=True)
    point=models.CharField(max_length=100,null=True)
    tuck=models.CharField(max_length=100,null=True)
    yoke=models.CharField(max_length=100,null=True)
    pw=models.CharField(max_length=100,null=True)
    slit=models.CharField(max_length=100,null=True)
    shoulder=models.CharField(max_length=100,null=True)
    sl=models.CharField(max_length=100,null=True)
    sr=models.CharField(max_length=100,null=True)
    muscle=models.CharField(max_length=100,null=True)
    ah=models.CharField(max_length=100,null=True)
    apf=models.CharField(max_length=100,null=True)
    apb=models.CharField(max_length=100,null=True)
    chest=models.CharField(max_length=100,null=True)
    bust=models.CharField(max_length=100,null=True)
    waist1=models.CharField(max_length=100,null=True)
    hip=models.CharField(max_length=100,null=True)
    seat=models.CharField(max_length=100,null=True)
    neckf=models.CharField(max_length=100,null=True)
    neckb=models.CharField(max_length=100,null=True)
    neckw=models.CharField(max_length=100,null=True)
    waist2=models.CharField(max_length=100,null=True)
    length=models.CharField(max_length=100,null=True)
    width=models.CharField(max_length=100,null=True)
    kneel=models.CharField(max_length=100,null=True)
    kneer=models.CharField(max_length=100,null=True)
    thighl=models.CharField(max_length=100,null=True)
    thighr=models.CharField(max_length=100,null=True)
    downf=models.CharField(max_length=100,null=True)

class TableSaree(models.Model):
    customer = models.ForeignKey(TableCustomer, on_delete=models.CASCADE, null=True)
    flength = models.CharField(max_length=100, null=True)
    point = models.CharField(max_length=100, null=True)
    tuck = models.CharField(max_length=100, null=True)
    pw = models.CharField(max_length=100, null=True)
    shoulder = models.CharField(max_length=100, null=True)
    sl = models.CharField(max_length=100, null=True)
    sr = models.CharField(max_length=100, null=True)
    muscle = models.CharField(max_length=100, null=True)
    ah = models.CharField(max_length=100, null=True)
    apf = models.CharField(max_length=100, null=True)
    apb = models.CharField(max_length=100, null=True)
    chest = models.CharField(max_length=100, null=True)
    bust = models.CharField(max_length=100, null=True)
    waist1 = models.CharField(max_length=100, null=True)
    neckf = models.CharField(max_length=100, null=True)
    neckb = models.CharField(max_length=100, null=True)
    neckw = models.CharField(max_length=100, null=True)
    waist2 = models.CharField(max_length=100, null=True)
    length1 = models.CharField(max_length=100, null=True)
    dwidth = models.CharField(max_length=100, null=True)
    kneel = models.CharField(max_length=100, null=True)
    kneer = models.CharField(max_length=100, null=True)
    seat = models.CharField(max_length=100, null=True)
    waist3 = models.CharField(max_length=100, null=True)
    length2 = models.CharField(max_length=100, null=True)
    pallu = models.CharField(max_length=100, null=True)

class TableOrders(models.Model):
    customer_id = models.CharField(null=True)
    order_id = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(max_length=50,null=True)
    address = models.TextField(null=True)
    date = models.DateField(null=True, auto_now_add=True)
    due_date = models.DateField(null=True)
    cloth_type = models.CharField(max_length=100, null=True)
    item = models.CharField(max_length=100, null=True)
    lining = models.CharField(max_length=100, null=True)
    bottom = models.CharField(max_length=100, null=True)
    locking = models.CharField(max_length=100, null=True)
    pattern = models.CharField(max_length=100, null=True)
    sareefall_type = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, upload_to="media/")
    stitching_charges = models.IntegerField(null=True)
    additional_charges = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    advance_paid = models.IntegerField(null=True)
    balance = models.IntegerField(null=True)
    notes = models.TextField(null=True)
    status = models.CharField(max_length=100, null=True)

class TableStaffs(models.Model):
    staffid=models.CharField(max_length=20, unique=True, blank=True)
    name=models.CharField(max_length=100,null=True)
    role=models.CharField(max_length=200,null=True)
    phone=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    address=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=20,null=True)
    monthly_salary = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.staffid:
            self.staffid = f"STAFF{self.id}"
            super().save(update_fields=["staffid"])

class TableSalary(models.Model):
    staff = models.ForeignKey(TableStaffs, on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    salary_month = models.DateField(null=True, blank=True)
    fixed_salary = models.FloatField(null=True)
    total_overtime = models.FloatField(default=0)
    total_salary = models.FloatField(null=True)
    status = models.CharField(max_length=20,choices=[('pending', 'Pending'), ('paid', 'Paid')],default='pending')

class TableOvertime(models.Model):
    staff = models.ForeignKey(TableStaffs, on_delete=models.CASCADE,null=True)
    ot_date = models.DateField(null=True)
    extra_hours = models.FloatField(null=True)
    ot_amount = models.FloatField(null=True)
    salary = models.ForeignKey(TableSalary,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

class TableExtra(models.Model):
    salary=models.ForeignKey(TableSalary,on_delete=models.CASCADE,null=True)
    advance=models.FloatField(null=True,default=0)
    pending=models.FloatField(null=True,default=0)


