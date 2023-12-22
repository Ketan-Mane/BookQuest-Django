# Generated by Django 4.2.5 on 2023-12-11 16:45

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
            name='Book',
            fields=[
                ('id', models.CharField(blank=True, max_length=40, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='', max_length=2000)),
                ('publication', models.CharField(blank=True, max_length=50)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='assets/uploads/images')),
                ('copies', models.IntegerField()),
                ('available_qty', models.IntegerField(blank=True)),
                ('type', models.CharField(choices=[('e-Book', 'E-Book'), ('Hard Copy', 'Hard Copy')], default='', max_length=30)),
                ('pdf', models.FileField(blank=True, default='', upload_to='assets/uploads/PDF')),
            ],
            options={
                'db_table': 'BOOK',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_no', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.book')),
            ],
            options={
                'db_table': 'CHAPTER',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'DEPARTMENT',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.department')),
            ],
            options={
                'db_table': 'SUBJECT',
            },
        ),
        migrations.CreateModel(
            name='ReservedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('reserved_date_time', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'RESERVED_BOOK',
            },
        ),
        migrations.CreateModel(
            name='FavouriteBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FAVOURITE_BOOK',
            },
        ),
        migrations.CreateModel(
            name='Chapter_Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=200)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.chapter')),
            ],
            options={
                'db_table': 'CHAPTER_TOPIC',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookQuestApp.subject'),
        ),
    ]