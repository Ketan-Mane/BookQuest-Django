from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(MembershipPlans)
admin.site.register(MemberShip)
admin.site.register(Payment)