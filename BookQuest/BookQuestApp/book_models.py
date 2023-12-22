from django.db import models
from .models import Subject
import os
from django.contrib.auth import get_user_model
User = get_user_model()


def change_filename(instance,filename):
    ext = filename.split(".")[-1]
    if ext == "pdf":
        path = "assets/uploads/PDF"
        filename = f"{instance}.{ext}"
        return os.path.join(path,filename)
    else:
        path = "assets/uploads/images"
        filename = f"{instance}.{ext}"
        return os.path.join(path,filename)
    

class Book(models.Model):
    type = [('e-Book','E-Book'),('Hard Copy','Hard Copy')]
    id = models.CharField(primary_key=True,max_length=40,blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    description = models.TextField(max_length=2000,default="",blank=True)
    publication = models.CharField(max_length=50,blank=True)
    add_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=change_filename)
    copies = models.IntegerField()
    available_qty = models.IntegerField(blank=True)
    type = models.CharField(max_length=30,choices=type,default="")
    pdf = models.FileField(upload_to=change_filename,default="",blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return self.id
    class Meta:
        db_table = "BOOK"


class Chapter(models.Model):
    chapter_no = models.IntegerField()
    name = models.CharField(max_length=150)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "CHAPTER"


class Chapter_Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    def __str__(self):
        return self.topic_name
    class Meta:
        db_table = "CHAPTER_TOPIC"


class FavouriteBook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = "FAVOURITE_BOOK"


class ReservedBook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    reserved_date_time = models.DateTimeField()
    class Meta:
        db_table = "RESERVED_BOOK"


class BookTransaction(models.Model):
    book = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True,null=True)
    return_status = models.CharField(default="Not return",blank=True,max_length=30)
    class Meta:
        db_table = "BOOK_TRANSACTION"