from django.contrib import admin
from .models import Result
# Register your models here.


@admin.register(Result)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','company_name','email','website','contact1','contact2','city','state','pincode','address','fileurl','filename')
