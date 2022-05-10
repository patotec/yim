from django.contrib import admin
from .models import *



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username',  'email']
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',  'approve']

class KeyAdmin(admin.ModelAdmin):
    list_display = ['user',  'read']



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Plan)
admin.site.register(Profit)
admin.site.register(Join_Plan)
admin.site.register(Pay_method)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Wallet)
admin.site.register(Key,KeyAdmin)