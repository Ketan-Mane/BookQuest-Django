# Generated by Django 4.2.5 on 2023-12-09 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_options_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='USER',
        ),
    ]
