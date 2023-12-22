from django.shortcuts import render,redirect
from .book_models import *
from payment.models import MemberShip
from payment.views import updateMemberShip
from datetime import date,datetime
from django.contrib import messages
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
def index(request):
    updateMemberShip()
    sendEmail()
    books = Book.objects.all()
    return render(request,'index.html',{'books':books})


def searchBook(request):
    if request.method == "POST":
        searchValue = request.POST['search'].strip()
        searchby = request.POST['searchby']
        if searchby:
                
            if searchby=="title":
                books = Book.objects.filter(Q(title__icontains=searchValue))
                return render(request,"search-book.html",{"books":books})
            
            elif searchby=="author":
                books = Book.objects.filter(Q(author__icontains=searchValue))
                return render(request,"search-book.html",{"books":books})
            
            elif searchby=="publication":
                books = Book.objects.filter(Q(publication__icontains=searchValue))
                return render(request,"search-book.html",{"books":books})
            
            elif searchby=="subject":
                subject = Subject.objects.get(Q(name__icontains=searchValue))
                books = Book.objects.filter(Q(subject=subject))
                return render(request,"search-book.html",{"books":books})
            
            elif searchby=="chapter":
                chapters = Chapter.objects.filter(name__icontains=searchValue)
                books = set({})
                for i in chapters:
                    books.add(i.book)
                return render(request,"search-book.html",{"books":books})
            
            elif searchby=="sub-topic":
                topic = Chapter_Topic.objects.filter(topic_name__icontains=searchValue)
                books = set({})
                for i in topic:
                    books.add(i.chapter.book)
                return render(request,"search-book.html",{"books":books})
            
        else:
            books = Book.objects.filter(Q(title__icontains=searchValue) | Q(author__icontains=searchValue) | Q(publication__icontains=searchValue))
            return render(request,"search-book.html",{"books":books})
    
    books = Book.objects.all()
    return render(request,'search-book.html',{'books':books})


def viewBook(request,id):
    member = False
    favourite = False
    reserved = False
    book = Book.objects.get(id=id)
    chapters = Chapter.objects.filter(book=book)
    chapter_topics = Chapter_Topic.objects.filter(chapter__in=chapters)
    if request.user.is_authenticated:   
        user = request.user
        member = MemberShip.objects.filter(user=user).exists()
        favourite = FavouriteBook.objects.filter(user=user,book=book).exists()
        reserved = ReservedBook.objects.filter(user=user,book=book).exists()
    if member:
        member = MemberShip.objects.get(user=user)
    
    context = {
        'book':book,
        'chapters':chapters,
        'chapter_topics':chapter_topics,
        'member':member,
        'favourite':favourite,
        'reserved':reserved
        }
    return render(request,'view-book.html',context=context)

# ! FAVOURITES
@login_required(login_url="/accounts/login")
def addFavourite(request):
    book_id = request.GET.get('book_id')
    user = request.user
    book = Book.objects.get(id=book_id)
    check_book_saved = FavouriteBook.objects.filter(user=user,book=book).exists()
    if check_book_saved:
        return redirect(f"../viewbook/{book_id}")
    else:
        add_favourite = FavouriteBook(user=user,book=book)
        add_favourite.save()
        messages.success(request,"Added to Favourite..!")
        return redirect(f"../view-book/{book_id}")


@login_required(login_url="/accounts/login")
def listFavourite(request):
    user = request.user
    favourite_books = FavouriteBook.objects.filter(user=user)
    return render(request,'favourite-book.html',{'favourite_books':favourite_books})


@login_required(login_url="/accounts/login")
def removeFavourite(request):
    book_id = request.GET.get('book_id')
    user = request.user
    book = Book.objects.get(id=book_id)
    favourite = FavouriteBook.objects.get(user=user,book=book)
    favourite.delete()
    messages.success(request,"Removed from Favourite..!")
    return redirect(f"../view-book/{book_id}")


@login_required(login_url="/accounts/login")
def reserveBook(request):
    book_id = request.GET.get("book_id")
    user = request.user
    book = Book.objects.get(id=book_id)
    date_time = datetime.now()
    if book.available_qty > 0:
        book.available_qty = book.available_qty - 1
        book.save()
        reserve_book = ReservedBook(book=book,user=user,status="Not issued",reserved_date_time=date_time)
        reserve_book.save()
        reserved_success_mail_msg = f'''Book reserved successfully\nTransaction Id : {reserve_book.id}'''
        reserve_book_mail = EmailMessage("Book Reservetion",reserved_success_mail_msg,to=[user.email])
        reserve_book_mail.send()
        messages.success(request,"Book Reserved..!")
        return redirect(f"../view-book/{book_id}")
    else:
        reserve_book = ReservedBook(book=book,user=user,status="Book Not Available",reserved_date_time=date_time)
        reserve_book.save()
        messages.info(request,mark_safe("Currently book is not available..!\nYou will be notified when available"))
        return redirect(f"../view-book/{book_id}")


@login_required(login_url="/accounts/login")
def listReservedBook(request):
    user = request.user
    reserved_books = ReservedBook.objects.filter(user=user)
    issued_books = BookTransaction.objects.filter(user=user)
    data = {
        "reserved_books" : reserved_books,
        'issued_books' : issued_books
    }
    return render(request,'reserved-book.html',data)


@login_required(login_url="/accounts/login")
def deleteReservedBook(request):
    reserved_book_id = request.GET.get('reserved_id')
    reserved_book = ReservedBook.objects.get(id=reserved_book_id)
    book = reserved_book.book
    book.available_qty = book.available_qty + 1
    book.save()
    reserved_book.delete()
    return redirect("/reserved-list")



# When book available and if some one requested for book email will be sent
def sendEmail():
    books = Book.objects.all()
    for i in range(len(books)):
        if books[i].available_qty > 0:
            reserved_book = ReservedBook.objects.filter(book=books[i],status="Book Not Available").order_by("reserved_date_time").first()
            if reserved_book != None:
                message = f'''Your request for book <strong>{reserved_book.book.title}</strong> now it is avaiable please collect in 2 days from the library.<br>
                            <h1>Book Details</h1>
                            <p>Book Id      : {reserved_book.book.id}</p>
                            <p>Book Title   : {reserved_book.book.title}</p>
                            <p>Book Author  : {reserved_book.book.author}</p>
                        '''
                
                send_mail = EmailMultiAlternatives("Book Available","",to=[reserved_book.user.email])
                send_mail.attach_alternative(message, "text/html")
                send_mail.send()
                reserved_book.status = "Notified"
                reserved_book.save()