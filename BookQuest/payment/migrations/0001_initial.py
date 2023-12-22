# Generated by Django 4.2.5 on 2023-12-11 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_charge', models.FloatField()),
                ('membership_duration', models.IntegerField(null=True)),
                ('membership_start_date', models.DateField(null=True)),
                ('membership_end_date', models.DateField(null=True)),
                ('membership_status', models.CharField(max_length=20, null=True)),
                ('total_amount', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'MEMBERSHIP',
            },
        ),
        migrations.CreateModel(
            name='MembershipPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(max_length=20)),
                ('charge_1', models.IntegerField()),
                ('charge_3', models.IntegerField()),
                ('charge_6', models.IntegerField()),
                ('charge_12', models.IntegerField()),
            ],
            options={
                'db_table': 'MEMBERSHIP_PLANS',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=30)),
                ('amount', models.FloatField()),
                ('payment_date_time', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.membership')),
            ],
            options={
                'db_table': 'PAYMENT',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='membership_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.membershipplans'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]