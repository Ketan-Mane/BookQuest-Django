from django import forms
from BookQuestApp.book_models import *
from datetime import date


class BookForm(forms.ModelForm):
    id = forms.CharField(widget=forms.TextInput(attrs={'readonly':True}))
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ['available_qty']

    
class ChapterForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(),label="",required=False)
    class Meta:
        model = Chapter
        fields = "__all__"


class ChapterTopicForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(),label="",required=False)
    class Meta:
        model = Chapter_Topic
        fields = "__all__"

    
class BookTransactionForm(forms.ModelForm):
    book = forms.CharField(widget=forms.TextInput(attrs={'value':"BQ"}))
    user = forms.IntegerField(widget=forms.NumberInput())
    issue_date = forms.DateField(widget=forms.DateInput(attrs={'readonly':True}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'readonly':True}))
    class Meta:
        model = BookTransaction
        exclude = ["return_date",'return_status']


class SubjectForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(),label="",required=False)
    class Meta:
        model = Subject
        fields = "__all__"