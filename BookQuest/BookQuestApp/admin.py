from typing import Any
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from datetime import datetime
from .models import *
from .book_models import *


class AdminBook(admin.ModelAdmin):
    exclude = ['available_qty']
    def get_form(self, request, obj = None,**kwargs):
        form = super(AdminBook,self).get_form(request, obj, **kwargs)
        form.base_fields['id'].disabled = True
        form.base_fields['id'].initial = "BQ"+str(datetime.now().strftime("%y%m%d%H%M%S"))
        return form
    
    def save_form(self, request, form, change):
        form.instance.available_qty = request.POST['copies']
        return super().save_form(request, form, change)



admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Book,AdminBook)
admin.site.register(Chapter)
admin.site.register(Chapter_Topic)
admin.site.register(FavouriteBook)
admin.site.register(ReservedBook)