from django.db import models

# Create your models here.
class Staffs(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    profile_picture = models.FileField(upload_to='profile_picture', null=True)
    attachment = models.FileField(upload_to='attachments', null=True)
    status = models.BooleanField(default=True)
    access = models.BooleanField(default=True)
    shift = models.CharField(max_length=20)

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = 'staffs'


class Expences(models.Model):
    Purchase = models.CharField(max_length=100)
    Remark = models.CharField(max_length=250)
    Amount = models.CharField(max_length=10)
    Date = models.DateField()

    def __str__(self):
        return self.Purchase

    class Meta:
        db_table = 'expenses'


class Returns(models.Model):
    Date = models.DateField()
    Staff  = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    Description = models.TextField()

    def __str__(self):
        return self.Date.isoformat()

    class Meta:
        db_table = 'Returns'


class Products(models.Model):
    name = models.CharField(max_length=100)
    sellingPrice = models.IntegerField()
    purchacePrice = models.IntegerField()
    vendor = models.CharField(max_length=25)

    def __str__(self):
        return self.name + ' ' + self.vendor
    
    class Meta:
        db_table = 'products'


class Sales(models.Model):
    Date = models.DateField()
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    NumberOfSales = models.IntegerField(null=True, blank=True)
    Total = models.IntegerField(null=True, blank=True)
    Discount = models.IntegerField(default=0, blank=True)
    Profit = models.IntegerField(null=True, blank=True)
    Staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.Total = (int(self.NumberOfSales) * int(self.Product.sellingPrice)) - int(self.Discount)
        self.Profit  = int(self.Total) -  (int(self.NumberOfSales) * int(self.Product.purchacePrice))
        super().save(*args, **kwargs)                            

    class Meta:
        db_table = 'Sales'

    def __str__(self):
        return self.Date.isoformat() + ' ' + self.Staff.firstName