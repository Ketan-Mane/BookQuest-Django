# Generated by Django 4.2.5 on 2023-12-11 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membershipplans',
            old_name='charge_1',
            new_name='month_1',
        ),
        migrations.RenameField(
            model_name='membershipplans',
            old_name='charge_12',
            new_name='month_12',
        ),
        migrations.RenameField(
            model_name='membershipplans',
            old_name='charge_3',
            new_name='month_3',
        ),
        migrations.RenameField(
            model_name='membershipplans',
            old_name='charge_6',
            new_name='month_6',
        ),
    ]
