from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from BookQuestApp.models import *
from BookQuestApp.views import sendEmail
from BookQuestApp.book_models import *
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def dashboard(request):
    sendEmail()
    books = Book.objects.all()
    users = User.objects.filter(is_staff=False)
    data = {
        'books' : books,
        'users' : users
    }
    return render(request,"admin-dashboard.html",data)



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def getBooks(request):
    books = Book.objects.all()
    return render(request,"list-book.html",{'books':books})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def addBook(request):
    if request.method=="POST":
        form = BookForm(request.POST,request.FILES)
        form.instance.available_qty = form['copies'].value()
        if form.is_valid():
            form.save()
            messages.success(request,'Book Added Successfully..')
            return redirect("/BookQuest/book")
        else:
            messages.error(request,'Error..')
            return render(request,"add-new-book.html",{'book_form':form})
    else:
        id = "BQ" + str(datetime.now().strftime("%y%m%d%H%M%S"))
        book_form = BookForm(initial={'id':id})
        return render(request,"add-new-book.html",{'book_form':book_form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def updateBook(request,book_id):
    book = Book.objects.get(id=book_id)
    book_form = BookForm(instance=book)
    if request.method=="POST":
        form = BookForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Updated Successfully..')
            return redirect("/BookQuest/book")
        else:
            messages.error(request,'Failed')
            return redirect("/BookQuest/book")
        
    return render(request,"update-book.html",{'book_form':book_form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def removeBook(request,book_id):
    book_id = request.POST.get('id')
    book = Book.objects.get(id=book_id)
    book.pdf.delete()
    book.image.delete()
    book.delete()
    return redirect("/BookQuest/book")



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def getChapters(request,book_id):
    book = Book.objects.get(id=book_id)
    chapters = Chapter.objects.filter(book=book)
    sub_topics = Chapter_Topic.objects.filter(chapter__in=chapters)
    data = {
        'chapters':chapters,
        'sub_topics':sub_topics,
        'id':book_id,
        }
    return render(request,"list-chapter.html",data)



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def addChapter(request,book_id):
    book = Book.objects.get(id=book_id)
    if request.method=="POST":
        form = ChapterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request,'Chapter Added Successfully..')
            return redirect(f"/BookQuest/book/{book_id}/chapter/")
        else:
            messages.error(request,'Error..')
            return render(request,"add-new-book.html",{'chapter_form':form})
    else:
        form = ChapterForm(initial={'book':book})
        return render(request,"add-new-chapter.html",{'chapter_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def updateChapter(request,book_id,chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    form = ChapterForm(instance=chapter)
    if request.method=="POST":
        form = ChapterForm(request.POST,instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request,"Chapter Update Successfully..!")
            return redirect(f"/BookQuest/book/{book_id}/chapter")
        else:
            messages.error(request,"Error..")
            return render(request,"update-chapter.html",{'chapter_form':form})
    else:
        return render(request,"update-chapter.html",{'chapter_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def removeChapter(request,book_id,chapter_id):
    if request.method=="POST":
        chapter_id = request.POST.get('id')
        chapter = Chapter.objects.get(id=chapter_id)
        chapter.delete()
        messages.success(request,"Removed Successfully..")
        return redirect(f"/BookQuest/book/{book_id}/chapter")



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def addChapterTopic(request,book_id,chapter_id):
    chapter = Chapter_Topic.objects.get(id=chapter_id)
    if request.method=="POST":
        form = ChapterTopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Topic Added..")
            return redirect(f"/BookQuest/book/{book_id}/chapter/")
        else:
            messages.error(request,"Error..")
            return render(request,"add-new-chapter-subtopic.html",{'subtopic_form':form})
    else:
        form = ChapterTopicForm(initial={'chapter':chapter})
        return render(request,"add-new-chapter-subtopic.html",{'subtopic_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def updateChapterTopic(request,book_id,subtopic_id):
    subtopic = Chapter_Topic.objects.get(id=subtopic_id)
    if request.method=="POST":
        form = ChapterTopicForm(request.POST,instance=subtopic)
        if form.is_valid():
            form.save()
            messages.success(request,"Topic Updated Successfully..")
            return redirect(f"/BookQuest/book/{book_id}/chapter/")
        else:
            messages.error(request,"Error..")
            return render(request,"update-chapter-subtopic.html",{'subtopic_form':form})
    else:
        form = ChapterTopicForm(instance=subtopic)
        return render(request,"update-chapter-subtopic.html",{'subtopic_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def removeChapterTopic(request,book_id,subtopic_id):
    if request.method=="POST":
        id = request.POST.get('id')
        subtopic = Chapter_Topic.objects.get(id=id)
        subtopic.delete()
        messages.success(request,"Topic Removed Successfully..")
        return redirect(f"/BookQuest/book/{book_id}/chapter/")



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def getBookTransactions(request):
    sendEmail()
    if request.method=="POST":
        id = request.POST.get('id')
        book_transaction = BookTransaction.objects.get(id=id)
        book_transaction.return_status = "Returned"
        book_transaction.return_date = date.today()
        book = book_transaction.book
        book.available_qty = book.available_qty + 1
        book.save()
        book_transaction.save()
        messages.success(request,"Record Updated..")
        return redirect("/BookQuest/book-transaction")
    else:
        book_transactions = BookTransaction.objects.all()
        return render(request,"list-book-transaction.html",{'book_transactions':book_transactions})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def issueNewBook(request):
    if request.method=="POST":
        book_id = request.POST.get('book')
        user_id = request.POST.get('user')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')
        
        book = Book.objects.filter(id=book_id).exists()
        user = User.objects.filter(id=user_id).exists()
        
        if book:
            book = Book.objects.get(id=book_id)
        else:
            messages.error(request,"Book not found..")
            return redirect("/BookQuest/book-transaction/issue-book")
        
        if user:
            user = User.objects.get(id=user_id)
        else:
            messages.error(request,"User Not Found..")
            return redirect("/BookQuest/book-transaction/issue-book")

        if book.available_qty > 0:
            book.available_qty = book.available_qty - 1
            book.save()
            book_transaction = BookTransaction(book=book, user=user, issue_date=issue_date, due_date=due_date)
            book_transaction.save()
            messages.success(request,"Issued..")
            return redirect("/BookQuest/book-transaction/")
        else:
            messages.error(request,"Book not available..")
            return redirect("/BookQuest/book-transaction/issue-book")
        
    else:
        due_date = date.today() + relativedelta(days =+ 7)
        form = BookTransactionForm(initial={'issue_date':date.today(),'due_date':due_date})
        return render(request,"issue-new-book.html",{'issue_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def getReservedBooks(request):
    if request.method=="POST":
        reserved_id = request.POST.get('id')
        reserved_book = ReservedBook.objects.get(id=reserved_id)
        book_transaction = BookTransaction(
            book = reserved_book.book,
            user = reserved_book.user,
            issue_date = date.today(),
            due_date = date.today() + relativedelta(days =+ 7),
        )
        book_transaction.save()
        reserved_book.delete()
        messages.success(request,"Issued..")
        return redirect("/BookQuest/book-transaction")
    else:
        reserved_books = ReservedBook.objects.all()
        return render(request,"list-reserved-book.html",{'reserved_books':reserved_books})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def getDepartments(request):
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    data = {
        'departments' : departments,
        'subjects' : subjects
    }
    return render(request,"list-department.html",data)



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def addDepartment(request):
    if request.method=="POST":
        name = request.POST.get('name')
        department = Department(name=name)
        department.save()
        messages.success(request,"Department Added Successfully")
        return redirect("/BookQuest/department") 
    return render(request,"add-new-department.html")



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def updateDepartment(request,dept_id):
    department = Department.objects.get(id=dept_id)
    if request.method=="POST":
        name = request.POST.get('name')
        id = request.POST.get('id')
        department = Department(id=id)
        department.name = name
        department.save()
        messages.success(request,"Department Added Successfully")
        return redirect("/BookQuest/department")
    return render(request,"update-department.html",{'department':department})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def removeDepartment(request,dept_id):
    if request.method=="POST":
        id = request.POST.get('id')
        department = Department(id=id)
        department.delete()
        messages.success(request,"Department Added Successfully")
        return redirect("/BookQuest/department")



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def addSubject(request,dept_id):
    department = Department.objects.get(id=dept_id)
    if request.method=="POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Subject Updated..")
            return redirect("/BookQuest/department")
        else:
            messages.error(request,"Error..")
            return redirect("/BookQuest/department")
    form = SubjectForm(initial={'department':department})
    return render(request,"add-new-dept-subject.html",{'subject_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def updateSubject(request,dept_id,subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method=="POST":
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request,"Subject Updated..")
            return redirect("/BookQuest/department")
        else:
            messages.error(request,"Error..")
            return redirect("/BookQuest/department")
    form = SubjectForm(instance=subject)
    return render(request,"update-dept-subject.html",{'subject_form':form})



@login_required(login_url="/BookQuest/login")
@permission_required(perm="is_superuser",login_url="/BookQuest/login")
def removeSubject(request,dept_id,subject_id):
    if request.method=="POST":
        id = request.POST.get('id')
        subject = Subject.objects.get(id=id)
        subject.delete()
        messages.success(request,"Subject Removed..")
        return redirect("/BookQuest/department")
    


def login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect("/BookQuest/")
            else:
                messages.error(request,"Not authorized user")
                return redirect("/BookQuest/")
        else:
            messages.error(request,"Invalid Username & Password.")
            return redirect("/BookQuest/login")
    else:
        if request.user.is_authenticated:
            return redirect("/BookQuest")
        return render(request,"admin-login.html")


def logout(request):
    auth.logout(request)
    return redirect("/BookQuest")
