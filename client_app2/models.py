from django.db import models

# Create your models here.

class TableStock(models.Model):
    item = models.CharField(max_length=100, null=True)
    stock = models.FloatField(null=True)
    unit = models.CharField(max_length=100, null=True)
    low_stock = models.IntegerField(null=True)
    notes = models.TextField(null=True)

class Account_type(models.Model):
    account_type = models.CharField(max_length=20, null = True)


class Account(models.Model):
    name = models.CharField(max_length=100, null = True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, null = True)
    updated_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, null = True)
    acount_type = models.ForeignKey(Account_type, on_delete=models.CASCADE, null=True, related_name='account_to_ac_type')


    def __str__(self):
        return f"{self.name} ({self.acount_type})"


class Transaction(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="transactions")
    transaction_type = models.CharField(
        max_length=10,
        choices=[('debit', 'Debit (Money In)'), ('credit', 'Credit (Money Out)')],
        null=True
    )

    def __str__(self):
        return f"{self.date} | {self.description or 'Transaction'}"

    # ✅ Remove balance auto-adjust here
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


