from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()
from .models import *
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your views here.

@login_required(login_url="/accounts/login")
def selectMembership(request):
    if request.method == "POST":
        selected_membership = MembershipPlans.objects.get(membership_type = request.POST.get("plan_type"))
        return render(request, "membership-duration.html",{"membership": selected_membership})
    else:
        return render(request, "select-membership.html")


@login_required(login_url="/accounts/login")
def membershipDuration(request):
    if request.method == "POST":
        membership_type = request.POST["selected_plan"]
        duration = int(request.POST["duration"])
        charge = int(request.POST["charge"])
        total = duration * charge
        context = {
                    "membership_type": membership_type,
                    "membership_duration": duration,
                    "membership_charge": charge,
                    "total_amount": total
                }
        return render(request,"payment.html",context=context)


@login_required(login_url="/accounts/login")
def payment(request):
    if request.method == "POST":
        membership_type = request.POST["membership_type"]
        duration = request.POST["membership_duration"]
        charge = request.POST["membership_charge"]
        total_amount = request.POST["total_amount"]
        transaction_id = request.POST["transaction_id"]
        status = request.POST["status"]
        amount = request.POST["amount"]
        start_date = date.today()
        end_date = date.today() + relativedelta(months =+int(duration))
        
        user = User.objects.get(username=request.user)
        membership_type = MembershipPlans.objects.get(membership_type=membership_type)
        member_ship = MemberShip.objects.filter(user=user).exists()

        if member_ship:
            member_ship = MemberShip.objects.get(user=user)
            member_ship.membership_type = membership_type
            member_ship.membership_duration = duration
            member_ship.membership_charge = charge
            member_ship.membership_start_date = start_date
            member_ship.membership_end_date = end_date
            member_ship.membership_status = "Active"
            member_ship.total_amount = total_amount
        else:
            member_ship = MemberShip(
                user=user,
                membership_type = membership_type,
                membership_duration = duration,
                membership_charge = charge,
                membership_start_date = start_date,
                membership_end_date = end_date,
                membership_status = "Active",
                total_amount = total_amount
            )
            
        member_ship.save()
        pay = Payment(transaction_id=transaction_id, status = status, amount = amount, member = member_ship)
        pay.save()
        return render(request, "payment-success.html")


#  Updating membership if expired
def updateMemberShip():
    memberships = MemberShip.objects.all()
    for member in memberships:
        if member.membership_status == "Active":
            end_date = member.membership_end_date
            if date.today() > end_date:
                member.membership_status = "Expired"
                member.save()