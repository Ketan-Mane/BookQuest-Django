from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "DEPARTMENT"


class Subject(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50)
    semester = models.IntegerField()
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "SUBJECT"
