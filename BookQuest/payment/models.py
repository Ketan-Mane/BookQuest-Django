from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class MembershipPlans(models.Model):
    membership_type = models.CharField(max_length=20)
    month_1 = models.IntegerField()
    month_3 = models.IntegerField()
    month_6 = models.IntegerField()
    month_12 = models.IntegerField()
    class Meta:
        db_table = "MEMBERSHIP_PLANS"


class MemberShip(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    membership_type = models.ForeignKey(MembershipPlans,on_delete=models.SET_NULL,null=True)
    membership_charge = models.FloatField()
    membership_duration = models.IntegerField(null=True)
    membership_start_date = models.DateField(null=True)
    membership_end_date = models.DateField(null=True)
    membership_status = models.CharField(max_length=20,null=True)
    total_amount = models.FloatField(default=0.0)
    class Meta:
        db_table = "MEMBERSHIP"
    

class Payment(models.Model):
    transaction_id = models.CharField(max_length=200)
    status = models.CharField(max_length=30)
    amount = models.FloatField()
    payment_date_time = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(MemberShip,on_delete=models.CASCADE)
    class Meta:
        db_table = "PAYMENT"