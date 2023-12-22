"""
URL configuration for BookQuest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard),
    path('book/', views.getBooks),
    path('book/add-book/', views.addBook),
    path('book/<str:book_id>/', views.updateBook),
    path('book/<str:book_id>/remove', views.removeBook),
    path("book/<str:book_id>/chapter/",views.getChapters),
    path("book/<str:book_id>/chapter/add-chapter/",views.addChapter),
    path("book/<str:book_id>/chapter/<int:chapter_id>/",views.updateChapter),
    path("book/<str:book_id>/chapter/<int:chapter_id>/delete",views.removeChapter),
    path("book/<str:book_id>/chapter/<int:chapter_id>/add-subtopic/",views.addChapterTopic),
    path("book/<str:book_id>/chapter/subtopic/<int:subtopic_id>/",views.updateChapterTopic),
    path("book/<str:book_id>/chapter/subtopic/<int:subtopic_id>/remove",views.removeChapterTopic),
    path("book-transaction/",views.getBookTransactions),
    path("book-transaction/",views.issueNewBook),
    path("book-transaction/issue-book",views.issueNewBook),
    path("reserved-book/",views.getReservedBooks),
    path("department/",views.getDepartments),
    path("department/add-department",views.addDepartment),
    path("department/<int:dept_id>/",views.updateDepartment),
    path("department/<int:dept_id>/remove",views.removeDepartment),
    path("department/<int:dept_id>/subject/add-subject",views.addSubject),
    path("department/<int:dept_id>/subject/<int:subject_id>/",views.updateSubject),
    path("department/<int:dept_id>/subject/<int:subject_id>/remove",views.removeSubject),
    path("login",views.login),
    path("logout",views.logout),
]
